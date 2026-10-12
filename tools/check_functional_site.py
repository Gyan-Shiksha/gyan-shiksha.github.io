#!/usr/bin/env python3
"""Check built-site local links, anchors, scripts and functional HTML hooks.

Does NOT send form submissions or assert the availability of external services.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import os
import re
import sys

ROOT = Path(os.environ.get("GYAN_SITE_ROOT", "_site")).resolve()
HOSTS = {"gyanshiksha.in", "www.gyanshiksha.in"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.refs = []
        self.attrs = []
        self.scripts = []
        self.forms = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.attrs.append((tag, a))
        if a.get("id"):
            self.ids.add(a["id"])
        key = "src" if tag in ("img", "script", "iframe", "source") else "href"
        if tag in ("a", "link", "img", "script", "iframe", "source") and a.get(key):
            self.refs.append((tag, a[key]))
        if tag == "script" and a.get("src"):
            self.scripts.append(a["src"])
        if tag == "form" and "data-gyan-form" in a:
            self.forms += 1


def check():
    errors = []
    parsed = {}
    for path in sorted(ROOT.rglob("*.html")):
        raw = path.read_text(encoding="utf-8")
        if raw.startswith("google-site-verification:"):
            continue
        parser = Page()
        parser.feed(raw)
        parsed[path.resolve()] = parser

    if not parsed:
        raise SystemExit("Missing rendered HTML pages in " + str(ROOT))

    def check_asset(page, tag, link):
        url = urlsplit(link)
        if url.scheme in ("mailto", "tel"):
            return
        if url.scheme not in ("", "http", "https"):
            errors.append(f"{page.name}: unsafe {tag} URL scheme: {link}")
            return
        if url.netloc and url.netloc.lower() not in HOSTS:
            return  # Third-party URL: existence must be checked separately.
        if url.scheme == "http" and url.netloc.lower() in HOSTS:
            errors.append(f"{page.name}: use HTTPS for {link}")
        relative = unquote(url.path)
        if not relative:
            target = page
        elif relative.startswith("/"):
            target = ROOT / relative.lstrip("/")
        else:
            target = page.parent / relative
        target = target.resolve()
        if not target.is_relative_to(ROOT):
            errors.append(f"{page.name}: link escapes site root: {link}")
            return
        if target.is_dir():
            target = target / "index.html"
        if not target.is_file():
            errors.append(f"{page.name}: missing {tag} target: {link}")
        elif url.fragment and target.suffix.lower() == ".html":
            other = parsed.get(target)
            if other is not None and unquote(url.fragment) not in other.ids:
                errors.append(f"{page.name}: missing #{url.fragment} target in {target.name}")

    checked = 0
    for path, page in parsed.items():
        for tag, link in page.refs:
            check_asset(path, tag, link)
            checked += 1

    def require(page_name, hooks, script=None, min_forms=0):
        page = parsed.get((ROOT / page_name).resolve())
        if page is None:
            errors.append(f"Missing {page_name}")
            return
        found = {key for _, attrs in page.attrs for key in attrs if key.startswith("data-")}
        for hook in hooks:
            if hook not in found:
                errors.append(f"{page_name}: missing {hook}")
        if script and not any(s.endswith(script) for s in page.scripts):
            errors.append(f"{page_name}: missing {script}")
        if page.forms < min_forms:
            errors.append(f"{page_name}: expected {min_forms} forms, found {page.forms}")

    require("index.html", ["data-site-search-form", "data-site-search-results"], "assets/js/app.js")
    require("games.html", ["data-learning-game", "data-game-start", "data-game-options",
                           "data-game-mode", "data-game-question", "data-game-restart"], "assets/js/games.js")
    require("contact.html", ["data-gyan-form", "data-send", "data-status"], "assets/js/forms-v316.js", 2)
    require("study-material.html", ["data-gyan-form", "data-send", "data-status"], "assets/js/forms-v316.js", 2)
    quiz = parsed.get((ROOT / "quiz.html").resolve())
    if quiz and not any(x.startswith("https://script.google.com/macros/s/") and x.endswith("/exec")
                        for _, x in quiz.refs):
        errors.append("quiz.html: missing external live Quiz link")
    material = parsed.get((ROOT / "study-material.html").resolve())
    if material:
        # Only approved file-level results may link to third-party files.
        # Public master-folder links would expose unrelated content.
        if not any(s.endswith("assets/js/material-library-v317.js") for s in material.scripts):
            errors.append("study-material.html: filterable material library script missing")
        for required in ("material-results", "material-search", "material-standard",
                         "material-category", "material-provider", "material-empty", "material-reset"):
            if required not in material.ids:
                errors.append(f"study-material.html: missing material library element #{required}")
        if any("drive.google.com/drive/folders/" in x or "mega.nz/folder/" in x
               for _, x in material.refs):
            errors.append("study-material.html: must not link directly to public master folders")

    # Material should be discoverable even with JavaScript disabled.
    for name in ("index.html", "blog.html", "quiz.html", "games.html", "contact.html"):
        page = parsed.get((ROOT / name).resolve())
        if page and not any(tag == "a" and link == "study-material.html" for tag, link in page.refs):
            errors.append(f"{name}: Material nav missing without JavaScript")

    if errors:
        print("\n".join(errors[:100]), file=sys.stderr)
        raise SystemExit(f"FAILED: {len(errors)} built HTML smoke-check issues")
    print(f"PASS: {len(parsed)} rendered HTML pages; {checked} link/asset references checked.")
    print("Structural checks passed for Quiz, Games, Forms, Study Material, navigation.")
    print("External services were NOT interacted with or submitted to.")


if __name__ == "__main__":
    check()
