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
    drive = host == "drive.google.com" and re.fullmatch(r"/file/d/[A-Za-z0-9_-]+(?:/.*)?", path)
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
            if str(entry.get("standard")) not in ("10", "12"):
                errors.append(f"{ctx}: this curated library currently prioritises standards 10 and 12")
            if not entry.get("subject"):
                errors.append(f"{ctx}: subject required")
            valid_date(entry.get("updated_at"), ctx)
            direct_resource(entry.get("url"), ctx)
        else:
            valid_date(entry.get("date"), ctx)
            if len(str(entry.get("summary") or "").strip()) < 55:
                errors.append(f"{ctx}: add original, meaningful Gujarati summary (55+ characters)")
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
