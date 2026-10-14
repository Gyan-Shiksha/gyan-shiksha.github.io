#!/usr/bin/env python3
"""Validate public Gyan Shiksha news, jobs, and material feeds.

Publishing is editorially controlled. Google Sheets is private; only reviewed
non-personal entries may be copied to these PUBLIC GitHub JSON files.
"""
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []


def https_url(value, context):
    try:
        u = urlsplit(str(value or "").strip())
        if u.scheme != "https" or not u.hostname or u.username or u.password:
            raise ValueError("requires HTTPS with no credentials")
        if u.hostname in {"localhost", "127.0.0.1"}:
            raise ValueError("local link")
        return u
    except Exception:
        errors.append(f"{context}: invalid HTTPS link")
        return None


def valid_date(value, context):
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(value)):
            raise ValueError("format")
        date.fromisoformat(str(value))
    except Exception:
        errors.append(f"{context}: expected real YYYY-MM-DD")


def direct_resource(url, context):
    u = https_url(url, context)
    if not u:
        return
    host = u.hostname.lower().removeprefix("www.")
    path = u.path
    from urllib.parse import parse_qs
    drive = host == "drive.google.com" and (
        re.fullmatch(r"/file/d/[A-Za-z0-9_-]+(?:/.*)?", path) or
        (path == "/open" and re.fullmatch(r"[A-Za-z0-9_-]+", parse_qs(u.query).get("id", [""])[0]))
    )
    docs = host == "docs.google.com" and re.fullmatch(
        r"/(?:document|spreadsheets|presentation)/d/[A-Za-z0-9_-]+(?:/.*)?", path
    )
    mega = host in {"mega.nz", "mega.io"} and re.fullmatch(
        r"/file/[A-Za-z0-9_-]+(?:/.*)?", path
    )
    if not (drive or docs or mega):
        errors.append(f"{context}: use individual Google Drive/Docs/MEGA file links only, not folder links")


def load_feed(name):
    path = ROOT / "data" / f"{name}.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        errors.append(f"{path.name}: expected a JSON array")
        return []
    return value


for feed in ("news", "jobs", "materials"):
    for idx, entry in enumerate(load_feed(feed), 1):
        ctx = f"data/{feed}.json item {idx}"
        if not isinstance(entry, dict):
            errors.append(f"{ctx}: expected an object")
            continue
        if entry.get("status") != "Approved":
            errors.append(f"{ctx}: do not commit non-Approved data publicly")
        if len(str(entry.get("title") or "").strip()) < 8:
            errors.append(f"{ctx}: meaningful title required")
        if not entry.get("category"):
            errors.append(f"{ctx}: category required")
        if feed == "materials":
            # Universal catalogue: any grade, board, college, teacher or other category.
            if not str(entry.get("standard") or "").strip():
                errors.append(f"{ctx}: standard/category required")
            if not str(entry.get("subject") or "").strip():
                errors.append(f"{ctx}: subject required")
            if not 20 <= len(str(entry.get("description") or "").strip()) <= 500:
                errors.append(f"{ctx}: add a real 20–500 character description for students")
            if entry.get("rights_verified") is not True:
                errors.append(f"{ctx}: rights_verified must be true (owner/copyright reviewed)")
            material_types = {"Textbook", "Notes", "Question Paper", "Worksheet", "PDF",
                              "Image", "Presentation", "Video", "Audio", "Other"}
            if entry.get("category") not in material_types:
                errors.append(f"{ctx}: unsupported material type; use {', '.join(sorted(material_types))}")
            if entry.get("year") and not re.fullmatch(r"20\d{2}", str(entry["year"])):
                errors.append(f"{ctx}: year must be 20XX")
            if entry.get("board") and entry["board"] not in {"SSC", "HSC", "GSEB", "GSBSTB", "GSET", "Other"}:
                errors.append(f"{ctx}: unknown board")
            valid_date(entry.get("updated_at"), ctx)
            direct_resource(entry.get("url"), ctx)
        else:
            valid_date(entry.get("date"), ctx)
            # Concise verified exam notices can be meaningful below 55 characters.
            # Keep a substantive minimum without requiring editors to pad notices.
            if len(str(entry.get("summary") or "").strip()) < 30:
                errors.append(f"{ctx}: add original, meaningful Gujarati summary (30+ characters)")
            https_url(entry.get("source_url"), ctx)
            if entry.get("pdf_url"):
                https_url(entry["pdf_url"], ctx)
            if feed == "jobs" and entry.get("deadline"):
                valid_date(entry["deadline"], ctx)

study = (ROOT / "study-material.html").read_text(encoding="utf-8")
if re.search(r"https://(?:drive\.google\.com/drive/folders/|mega\.(?:nz|io)/folder/)", study):
    errors.append("study-material.html: master folder URL must never appear on the public page")

if errors:
    raise SystemExit("Public feed safety check failed:\n" + "\n".join(errors))
print("PASS: all public feeds are curated; no publicly linked master folders")
