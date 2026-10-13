#!/usr/bin/env python3
"""Add a human-approved, file-specific educational resource to Gyan Shiksha.

Called by the owner-only manual GitHub Actions workflow. All website data is public:
do not include passwords, student names, private notes or folder links.
"""
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/materials.json"
KINDS = {
    "Textbook", "Notes", "Question Paper", "Worksheet", "PDF",
    "Image", "Presentation", "Video", "Audio", "Other"
}


def clean(key, limit, minimum=1):
    value = " ".join(os.environ.get(key, "").split()).strip()
    if len(value) < minimum or len(value) > limit:
        raise SystemExit(f"{key}: expected between {minimum} and {limit} characters")
    if "<" in value or ">" in value:
        raise SystemExit(f"{key}: HTML is not accepted")
    return value


def allowed_file_url(value):
    try:
        u = urlsplit(value)
        if u.scheme != "https" or u.username or u.password:
            return False
        host, path = (u.hostname or "").lower(), u.path
        drive = host == "drive.google.com" and (
            re.fullmatch(r"/file/d/[A-Za-z0-9_-]+(?:/.*)?", path)
            or (path == "/open" and re.fullmatch(
                r"[A-Za-z0-9_-]+", parse_qs(u.query).get("id", [""])[0]))
        )
        docs = host == "docs.google.com" and re.fullmatch(
            r"/(?:document|spreadsheets|presentation)/d/[A-Za-z0-9_-]+(?:/.*)?", path)
        mega = host in {"mega.nz", "mega.io"} and re.fullmatch(
            r"/file/[A-Za-z0-9_-]+(?:/.*)?", path)
        return bool(drive or docs or mega)
    except (TypeError, ValueError, IndexError):
        return False


def main():
    if os.environ.get("GITHUB_REPOSITORY", "").lower() != "gyan-shiksha/gyan-shiksha.github.io":
        raise SystemExit("This publisher is only for the official Gyan Shiksha repository")
    if os.environ.get("INPUT_RIGHTS_CONFIRMED", "").lower() != "true":
        raise SystemExit("You must explicitly confirm ownership/copyright and incognito viewer access")

    title = clean("INPUT_TITLE", 180, 8)
    standard = clean("INPUT_STANDARD", 60)
    subject = clean("INPUT_SUBJECT", 80)
    category = clean("INPUT_CATEGORY", 30)
    description = clean("INPUT_DESCRIPTION", 500, 20)
    board = clean("INPUT_BOARD", 8, 0)
    year = clean("INPUT_YEAR", 4, 0)
    url = clean("INPUT_URL", 900, 20)

    if board not in {"", "GSEB", "GSBSTB", "HSC", "SSC", "GSET", "Other"}:
        raise SystemExit("INPUT_BOARD: choose GSEB, GSBSTB, HSC, SSC, GSET, Other or leave blank")
    if year and not re.fullmatch(r"20\d{2}", year):
        raise SystemExit("INPUT_YEAR: use an edition year from 2000–2099 or leave blank")

    if category not in KINDS:
        raise SystemExit("Unsupported material category")
    if not allowed_file_url(url):
        raise SystemExit("Use an HTTPS link to an individual Drive/Docs/MEGA FILE, never a folder")
    try:
        records = json.loads(DATA.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError("expected a JSON list")
    except (OSError, ValueError) as e:
        raise SystemExit(f"Cannot read existing catalogue: {e}")
    if any(isinstance(r, dict) and r.get("url") == url for r in records):
        raise SystemExit("This individual file URL already exists in the catalogue")

    record = {
        "title": title,
        "standard": standard,
        "subject": subject,
        "category": category,
        "description": description,
        "url": url,
        **({"board": board} if board else {}),
        **({"year": year} if year else {}),
        "updated_at": date.today().isoformat(),
        "status": "Approved",
        "rights_verified": True
    }
    records.insert(0, record)
    DATA.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} approved file entries; no folder links included.")


if __name__ == "__main__":
    main()
