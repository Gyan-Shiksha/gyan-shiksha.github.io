"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "..");
const questions = require(path.join(root,"assets/js/quick-quiz.js"));
assert.deepEqual(Object.keys(questions).sort(), ["10","12"]);
for (const grade of ["10","12"]) {
  assert(questions[grade].length >= 10, grade + " must have 10 practice questions");
  const stems = new Set();
  for (const [stem,opts,correct,why] of questions[grade]) {
    assert(typeof stem === "string" && stem.length >= 9);
    assert(Array.isArray(opts) && opts.length === 4, "four options");
    assert.equal(new Set(opts).size, 4, "options must be different");
    assert(Number.isInteger(correct) && correct>=0 && correct<4);
    assert(typeof why === "string" && why.length > 10, "explanation required");
    assert(!stems.has(stem),"duplicate question");
    stems.add(stem);
  }
}
const quiz = fs.readFileSync(path.join(root,"quiz.html"),"utf8");
const local = fs.readFileSync(path.join(root,"quick-quiz.html"),"utf8");
assert(quiz.includes('href="quick-quiz.html"'),"main quiz must offer an independent route");
assert(quiz.includes("https://script.google.com/macros/s/"),"original Apps Script backend must remain reachable");
for (const id of ["quick-quiz-app","quick-grade","quick-start","quick-play","quick-question","quick-options","quick-feedback","quick-next","quick-finish","quick-score","quick-retry"]) {
  assert(local.includes('id="'+id+'"'),"missing functional quiz hook: "+id);
}
assert(local.includes('assets/js/quick-quiz.js'),"in-browser logic must load");
console.log("PASS: grade 10 and 12 standalone quiz banks, answer indices, original Quiz Saathi launcher and interactive HTML hooks.");
