#!/usr/bin/env node
"use strict";
// Real-data Study Material UI functional test (no external MEGA downloads).
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");
const assert = require("node:assert/strict");
const ROOT = path.resolve(__dirname, "..");

class Element {
  constructor(tag = "div") {
    this.tagName = tag;
    this.children = [];
    this.handlers = {};
    this.attrs = {};
    this.dataset = {};
    this.className = "";
    this.value = "";
    this.hidden = false;
    this.disabled = false;
    this.classes = new Set();
    this.classList = {
      add: name => this.classes.add(name),
      contains: name => this.classes.has(name),
      toggle: (name, on) => on ? this.classes.add(name) : this.classes.delete(name)
    };
  }
  get textContent() { return this._text || ""; }
  set textContent(value) { this._text = String(value); this.children = []; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  setAttribute(name, val) { this.attrs[name] = String(val); }
  addEventListener(name, callback) { this.handlers[name] = callback; }
  click() { if (this.handlers.click) this.handlers.click(); }
  change() { if (this.handlers.change) this.handlers.change(); }
  input() { if (this.handlers.input) this.handlers.input(); }
  focus() { this.focused = true; }
  scrollIntoView() { this.scrolled = true; }
}
async function main() {
  const ids = [
    "material-results", "material-summary", "material-browse-controls",
    "material-standard", "material-subject", "material-year", "material-year-label",
    "material-search", "material-reset", "material-empty", "material-empty-title",
    "material-empty-message", "material-error", "material-pagination",
    "material-page-numbers", "material-prev-page", "material-next-page",
    "material-page-status"
  ];
  const fields = Object.fromEntries(ids.map(x => [x, new Element()]));
  const categories = ["", "Textbook", "Question Paper", "PDF"].map(x => {
    const node = new Element("button");
    node.dataset.materialKind = x;
    return node;
  });
  const document = {
    getElementById: id => fields[id] || null,
    querySelectorAll: () => categories,
    createElement: tag => new Element(tag)
  };
  const rows = JSON.parse(fs.readFileSync(path.join(ROOT, "data/materials.json"), "utf8"));
  assert.ok(rows.length >= 144, "Do not lose any of the 144 catalogued baseline entries");
  const totalPages = Math.ceil(rows.length / 6);
  const grade12Total = rows.filter(x => x.standard === "12" && x.status === "Approved").length;
  const grade12Pages = Math.ceil(grade12Total / 6);
  const grade2Total = rows.filter(x => x.standard === "2" && x.status === "Approved").length;
  const grade10Year2026 = rows.filter(x => x.standard === "10" && x.year === "2026" && x.status === "Approved").length;
  const grade12QuestionPapers = rows.filter(x =>
    x.standard === "12" && x.category === "Question Paper" && x.status === "Approved").length;
  assert.equal(new Set(rows.map(x => x.url)).size, rows.length, "No duplicate file URLs");

  const script = fs.readFileSync(path.join(ROOT, "assets/js/material-library-v317.js"), "utf8");
  vm.runInNewContext(script, { document, URL,
    fetch: async () => ({ ok: true, json: async () => rows })
  });
  for (let i = 0; i < 16; i++) await Promise.resolve();

  const field = id => fields[id];
  const results = field("material-results");
  const nav = field("material-pagination");
  const status = field("material-page-status");
  const next = field("material-next-page");
  const prev = field("material-prev-page");
  const pageBtns = field("material-page-numbers");
  const year = field("material-year");
  const yearLabel = field("material-year-label");
  const standard = field("material-standard");
  const subject = field("material-subject");

  assert.equal(field("material-browse-controls").hidden, false);
  assert.equal(results.children.length, 6, "Only six cards should render");
  assert.equal(status.textContent, "પેજ 1 / " + totalPages);
  assert.equal(prev.disabled, true);
  assert.equal(next.disabled, false);
  assert.ok(field("material-summary").textContent.includes("કુલ " + rows.length + " સામગ્રી"), "Summary must reflect dynamic record total");
  assert.equal(results.children[0].children.length, 5, "Card title, description, compact metadata and open link");
  assert.equal(results.children[0].children[4].target, "_blank");
  assert.equal(results.children[0].children[4].rel, "noopener noreferrer nofollow");

  next.click();
  assert.equal(status.textContent, "પેજ 2 / " + totalPages, "Next works");
  assert.equal(prev.disabled, false);
  prev.click();
  assert.equal(status.textContent, "પેજ 1 / " + totalPages, "Previous works");
  const last = pageBtns.children.find(x => x.textContent === String(totalPages));
  assert.ok(last, "Direct final-page number should exist");
  last.click();
  assert.equal(status.textContent, "પેજ " + totalPages + " / " + totalPages, "Direct numbered page works");
  assert.equal(next.disabled, true);
  assert.equal(results.children.length, rows.length % 6 || 6);

  standard.value = "12";
  standard.change();
  assert.equal(status.textContent, "પેજ 1 / " + grade12Pages, "Grade 12 page count");
  assert.equal(results.children.length, 6);
  for (let i = 1; i < grade12Pages; i++) next.click();
  assert.equal(status.textContent, "પેજ " + grade12Pages + " / " + grade12Pages);
  assert.equal(results.children.length, grade12Total % 6 || 6, "Last Grade 12 page remains bounded");
  assert.equal(next.disabled, true);
  assert.ok(year.children.some(x => x.value === "2024"), "Grade 12 should offer 2024");
  const grade12Years = new Set(rows.filter(x => x.standard === "12" && x.status === "Approved")
    .map(x => x.year).filter(Boolean));
  assert.deepEqual(new Set(Array.from(year.children, x => x.value).filter(Boolean)), grade12Years,
    "Grade 12 year selector lists only available years, including new 2026 papers");

  standard.value = "10";
  standard.change();
  assert.ok(year.children.some(x => x.value === "2024"));
  assert.ok(year.children.some(x => x.value === "2026"));
  year.value = "2026";
  year.change();
  assert.equal(results.children.length, grade10Year2026, "Grade 10 year filter matches actual records");
  assert.equal(nav.hidden, true, "No pager when <= 6 results");

  standard.value = "2";
  standard.change();
  assert.equal(results.children.length, grade2Total);
  assert.equal(year.value, "", "Irrelevant year selection clears on grade switch");
  assert.equal(yearLabel.hidden, true, "Hide year dropdown when no year in grade");
  assert.equal(nav.hidden, true);

  standard.value = "12";
  standard.change();
  // Restrict to textbooks first: adding HSC Geography papers should not
  // make a textbook-only Geography search include those question papers.
  categories.find(x => x.dataset.materialKind === "Textbook").click();
  subject.value = "ભૂગોળ";
  subject.change();
  const geographyTextbooks = rows.filter(x =>
    x.category === "Textbook" && x.standard === "12" && x.subject === "ભૂગોળ");
  assert.equal(results.children.length, geographyTextbooks.length);
  assert.equal(yearLabel.hidden,
    !geographyTextbooks.some(x => /^20\d{2}$/.test(x.year || "")),
    "Year filter visibility follows matching textbook editions");

  categories.find(x => x.dataset.materialKind === "Question Paper").click();
  assert.deepEqual(Array.from(standard.children, x => x.value), ["", "12"],
    "Question Paper grade selector must show only Std 12, not GSET or Teacher");
  assert.equal(standard.value, "12", "Preserve a grade if it has relevant material");
  assert.equal(subject.value, "ભૂગોળ", "Category change preserves a subject when papers in that subject exist");
  assert.ok(subject.children.some(x => x.value === "ભૂગોળ"), "Geography must appear among HSC 2024 paper subjects");
  subject.value = ""; subject.change();
  assert.equal(status.textContent, "પેજ 1 / " + Math.ceil(grade12QuestionPapers / 6), "Question paper page count");

  // HSC old papers must be browseable by year without mixing years.
  const hsc2026 = rows.filter(x => x.category === "Question Paper" && x.standard === "12" && x.year === "2026");
  const hsc2025 = rows.filter(x => x.category === "Question Paper" && x.standard === "12" && x.year === "2025");
  const hsc2024 = rows.filter(x => x.category === "Question Paper" && x.standard === "12" && x.year === "2024");
  const hsc2023 = rows.filter(x => x.category === "Question Paper" && x.standard === "12" && x.year === "2023");
  assert.equal(hsc2026.length, 9, "Expect nine HSC 2026 board papers");
  assert.equal(hsc2025.length, 16, "Expect exactly 16 new HSC 2025 papers");
  assert.ok(hsc2024.length >= 17, "At least 17 HSC 2024 papers expected");
  assert.ok(hsc2023.length >= 12, "Keep all pre-existing HSC 2023 papers");
  assert.ok(year.children.some(x => x.value === "2023"), "2023 remains available");
  assert.ok(year.children.some(x => x.value === "2024"), "2024 is offered for the HSC papers");
  assert.ok(year.children.some(x => x.value === "2025"), "2025 is offered for the HSC papers");
  assert.ok(year.children.some(x => x.value === "2026"), "2026 is offered for the new HSC papers");
  year.value = "2026"; year.change();
  assert.equal(status.textContent, "પેજ 1 / " + Math.ceil(hsc2026.length / 6), "HSC 2026 paper page count");
  assert.equal(results.children.length, 6, "First 2026 paper page renders only six");
  next.click();
  assert.equal(status.textContent, "પેજ 2 / 2", "HSC 2026 next page works");
  assert.equal(results.children.length, 3, "HSC 2026 has three results on its last page");
  assert.equal(next.disabled, true, "2026 next disabled on last page");
  prev.click();
  assert.equal(status.textContent, "પેજ 1 / 2", "HSC 2026 back button works");
  year.value = "2025"; year.change();
  assert.equal(status.textContent, "પેજ 1 / " + Math.ceil(hsc2025.length / 6), "HSC 2025 year count");
  assert.equal(results.children.length, 6, "First HSC 2025 page bounded to six cards");
  for (let page = 1; page < Math.ceil(hsc2025.length / 6); page++) next.click();
  assert.equal(results.children.length, hsc2025.length % 6 || 6, "Last HSC 2025 page bounded correctly");
  year.value = "2024"; year.change();
  assert.equal(status.textContent, "પેજ 1 / " + Math.ceil(hsc2024.length / 6), "HSC 2024 paper page count");
  assert.equal(results.children.length, 6, "First HSC 2024 page bounded to 6");
  for (let page = 1; page < Math.ceil(hsc2024.length / 6); page++) next.click();
  assert.equal(results.children.length, hsc2024.length % 6 || 6, "Last HSC 2024 paper page");
  year.value = "2023"; year.change();
  assert.equal(status.textContent, "પેજ 1 / " + Math.ceil(hsc2023.length / 6), "2023 year remains independently filterable");
  year.value = ""; year.change();

  // Changing a category from an incompatible grade must reset the grade
  // rather than silently return zero results.
  standard.value = "2";
  standard.change();
  categories.find(x => x.dataset.materialKind === "Question Paper").click();
  assert.equal(standard.value, "", "Switching Std 2 -> Question Paper resets grade");
  assert.deepEqual(Array.from(standard.children, x => x.value), ["", "12"]);

  categories.find(x => x.dataset.materialKind === "PDF").click();
  const pdfStandards = [...new Set(rows.filter(x => x.category === "PDF").map(x => x.standard))];
  assert.deepEqual(Array.from(standard.children, x => x.value).slice(1), pdfStandards,
    "Other PDF offers only its real study programme(s)");
  assert.equal(standard.value, "", "Switch to PDF clears unrelated grade");
  assert.ok(!standard.children.some(x => x.value === "12"));

  categories.find(x => x.dataset.materialKind === "Textbook").click();
  const textbookStandards = new Set(rows.filter(x => x.category === "Textbook").map(x => x.standard));
  assert.deepEqual(new Set(Array.from(standard.children, x => x.value).filter(Boolean)),
    textbookStandards, "Textbook offers only grades/programmes with textbooks");
  assert.ok(!standard.children.some(x => x.value === "GSET / સ્પર્ધાત્મક પરીક્ષા"),
    "No GSET option under Textbook");

  categories.find(x => x.dataset.materialKind === "").click();
  assert.ok(standard.children.some(x => x.value === "GSET / સ્પર્ધાત્મક પરીક્ષા"),
    "All restores every grade/programme");
  standard.value = "";
  standard.change();

  field("material-search").value = "not-a-match-0000";
  field("material-search").input();
  assert.equal(results.children.length, 0);
  assert.equal(field("material-empty").hidden, false);
  assert.equal(nav.hidden, true);
  field("material-reset").click();
  assert.equal(status.textContent, "પેજ 1 / " + totalPages, "Reset restores the full catalogue");
  assert.equal(results.children.length, 6);
  assert.equal(field("material-empty").hidden, true);
  assert.equal(standard.value, "");
  assert.equal(subject.value, "");
  assert.equal(year.value, "");

  console.log("HSC 2026 nine papers across two pages; 2023, 2024 and 2025 remain independently filterable.");
  console.log("PASS: " + rows.length + " real records, no URL duplicates, " + totalPages + " numbered pages, forward/back, last-page bounds, grade 12 (" + grade12Total + "), grade 10 years, grade 2, cascading subject/year/category, search/reset and safe external links.");
}
main().catch(e => { console.error(e); process.exitCode = 1; });
