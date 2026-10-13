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
  assert.equal(rows.length, 144, "All 144 current records should be audited");
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
  assert.equal(status.textContent, "પેજ 1 / 24");
  assert.equal(prev.disabled, true);
  assert.equal(next.disabled, false);
  assert.match(field("material-summary").textContent, /144/);
  assert.equal(results.children[0].children.length, 5, "Card title, description, compact metadata and open link");
  assert.equal(results.children[0].children[4].target, "_blank");
  assert.equal(results.children[0].children[4].rel, "noopener noreferrer nofollow");

  next.click();
  assert.equal(status.textContent, "પેજ 2 / 24", "Next works");
  assert.equal(prev.disabled, false);
  prev.click();
  assert.equal(status.textContent, "પેજ 1 / 24", "Previous works");
  const last = pageBtns.children.find(x => x.textContent === "24");
  assert.ok(last, "Direct final-page number should exist");
  last.click();
  assert.equal(status.textContent, "પેજ 24 / 24", "Direct numbered page works");
  assert.equal(next.disabled, true);
  assert.equal(results.children.length, 6);

  standard.value = "12";
  standard.change();
  assert.equal(status.textContent, "પેજ 1 / 7", "Grade 12: 40 entries / 6 per page = 7 pages");
  assert.equal(results.children.length, 6);
  for (let i = 0; i < 6; i++) next.click();
  assert.equal(status.textContent, "પેજ 7 / 7");
  assert.equal(results.children.length, 4, "Last Grade 12 page should show 4 cards");
  assert.equal(next.disabled, true);
  assert.ok(year.children.some(x => x.value === "2024"), "Grade 12 should offer 2024");
  assert.ok(!year.children.some(x => x.value === "2026"), "Do not offer unrelated years for selected grade");

  standard.value = "10";
  standard.change();
  assert.ok(year.children.some(x => x.value === "2024"));
  assert.ok(year.children.some(x => x.value === "2026"));
  year.value = "2026";
  year.change();
  assert.equal(results.children.length, 5, "Grade 10 year 2026 returns only its five books");
  assert.equal(nav.hidden, true, "No pager when <= 6 results");

  standard.value = "2";
  standard.change();
  assert.equal(results.children.length, 3);
  assert.equal(year.value, "", "Irrelevant year selection clears on grade switch");
  assert.equal(yearLabel.hidden, true, "Hide year dropdown when no year in grade");
  assert.equal(nav.hidden, true);
  assert.ok(subject.children.some(x => x.value === "વિષયની પુષ્ટિ બાકી"),
    "Do not silently hide unverified metadata; report separately");

  standard.value = "12";
  standard.change();
  subject.value = "ભૂગોળ";
  subject.change();
  assert.equal(results.children.length, 1);
  assert.equal(yearLabel.hidden, true, "Hide year filter when subject has no dated records");

  categories.find(x => x.dataset.materialKind === "Question Paper").click();
  assert.equal(subject.value, "", "Category change clears incompatible subject");
  assert.equal(status.textContent, "પેજ 1 / 2", "Grade 12 question papers = 12 entries");
  assert.ok(!subject.children.some(x => x.value === "ભૂગોળ"), "Subject list is category-aware");
  categories.find(x => x.dataset.materialKind === "").click();

  field("material-search").value = "not-a-match-0000";
  field("material-search").input();
  assert.equal(results.children.length, 0);
  assert.equal(field("material-empty").hidden, false);
  assert.equal(nav.hidden, true);
  field("material-reset").click();
  assert.equal(status.textContent, "પેજ 1 / 24", "Reset restores the full catalogue");
  assert.equal(results.children.length, 6);
  assert.equal(field("material-empty").hidden, true);
  assert.equal(standard.value, "");
  assert.equal(subject.value, "");
  assert.equal(year.value, "");

  console.log("PASS: 144 real records, no URL duplicates, 24 numbered pages, forward/back, last-page bounds, grade 12 (40), grade 10 years, grade 2, cascading subject/year/category, search/reset and safe external links.");
}
main().catch(e => { console.error(e); process.exitCode = 1; });
