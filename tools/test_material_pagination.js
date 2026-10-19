#!/usr/bin/env node
// Browser-free smoke test for bounded material pagination and filter resets.
"use strict";
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const path = require("node:path");

const ids = [
  "material-results", "material-summary", "material-browse-controls",
  "material-standard", "material-subject", "material-year", "material-year-label",
  "material-search", "material-reset", "material-empty", "material-empty-title",
  "material-empty-message", "material-error", "material-pagination",
  "material-page-numbers", "material-prev-page", "material-next-page",
  "material-page-status"
];

class Element {
  constructor(tag = "div") {
    this.tagName = tag;
    this.children = [];
    this.listeners = {};
    this.attrs = {};
    this.dataset = {};
    this.value = "";
    this.hidden = false;
    this.disabled = false;
    this.className = "";
    this._text = "";
    this.classes = new Set();
    this.classList = {
      add: name => this.classes.add(name),
      toggle: (name, on) => on ? this.classes.add(name) : this.classes.delete(name),
      contains: name => this.classes.has(name)
    };
  }
  get textContent() { return this._text; }
  set textContent(value) { this._text = String(value); this.children = []; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  setAttribute(key, value) { this.attrs[key] = String(value); }
  addEventListener(event, handler) { this.listeners[event] = handler; }
  click() { if (this.listeners.click) this.listeners.click(); }
  change() { if (this.listeners.change) this.listeners.change(); }
  input() { if (this.listeners.input) this.listeners.input(); }
  focus() { this.focused = true; }
  scrollIntoView() { this.scrolled = true; }
}

async function test() {
  const fields = Object.fromEntries(ids.map(id => [id, new Element()]));
  const kinds = ["", "Textbook", "PDF"].map(kind => {
    const node = new Element("button");
    node.dataset.materialKind = kind;
    return node;
  });
  const document = {
    getElementById: id => fields[id] || null,
    querySelectorAll: () => kinds,
    createElement: tag => new Element(tag)
  };
  const rows = Array.from({ length: 31 }, (_, i) => ({
    title: "ધોરણ " + (i < 10 ? "5" : "4") + " — પાઠ્યપુસ્તક " + (i + 1),
    standard: i < 10 ? "5" : "4",
    subject: i % 2 ? "ગણિત" : "ગુજરાતી",
    category: "Textbook",
    description: "પાઠ્યપુસ્તકનું યોગ્ય ગુજરાતી વર્ણન અને શૈક્ષણિક માહિતી.",
    url: "https://mega.nz/file/TestFile" + i + "#PublicFileKey" + i,
    updated_at: "2026-10-13", status: "Approved", rights_verified: true
  }));
  const script = fs.readFileSync(
    path.join(__dirname, "../assets/js/material-library-v317.js"), "utf8");
  vm.runInNewContext(script, {
    document, URL, URLSearchParams,
    // Provide the browser location used for optional ?material= deep links.
    window: { location: { search: "", pathname: "/study-material.html" } },
    fetch: async () => ({ ok: true, json: async () => rows })
  });
  // Allow the async fetch and catalogue initialization to settle.
  for (let i = 0; i < 12; i++) await Promise.resolve();

  const result = fields["material-results"];
  const pages = fields["material-pagination"];
  const next = fields["material-next-page"];
  const prev = fields["material-prev-page"];
  const pageStatus = fields["material-page-status"];
  const summary = fields["material-summary"];
  assert.equal(result.children.length, 6, "Initially display only six cards");
  assert.equal(pages.hidden, false, "Pagination appears for more than six items");
  assert.match(summary.textContent, /1–6/);
  assert.equal(prev.disabled, true, "Previous disabled on first page");
  assert.equal(next.disabled, false);

  for (let i = 0; i < 5; i++) next.click();
  assert.equal(result.children.length, 1, "Last page shows remaining item only");
  assert.equal(pageStatus.textContent, "પેજ 6 / 6");
  assert.equal(next.disabled, true, "Next disabled on final page");
  assert.equal(result.focused, true, "Pagination returns focus to results");
  assert.equal(result.scrolled, true, "Pagination scrolls to results");

  fields["material-standard"].value = "5";
  fields["material-standard"].change();
  assert.equal(result.children.length, 6, "Changing grade resets to first page");
  assert.equal(pageStatus.textContent, "પેજ 1 / 2");

  fields["material-subject"].value = "ગણિત";
  fields["material-subject"].change();
  assert.equal(result.children.length, 5, "Subject and grade filters compose");
  assert.equal(pages.hidden, true, "Hide pagination for six or fewer results");

  fields["material-search"].value = "અસ્તિત્વમાં-નથી";
  fields["material-search"].input();
  assert.equal(result.children.length, 0, "No-match search renders no cards");
  assert.equal(fields["material-empty"].hidden, false);
  assert.equal(pages.hidden, true);

  fields["material-reset"].click();
  assert.equal(result.children.length, 6, "Reset restores the bounded first page");
  assert.equal(pageStatus.textContent, "પેજ 1 / 6");
  assert.equal(fields["material-empty"].hidden, true);

  console.log("PASS: pagination stays within 6 cards, supports all pages, resets on filters/search and handles empty matches.");
}

test().catch(error => { console.error(error); process.exitCode = 1; });
