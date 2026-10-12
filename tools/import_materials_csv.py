#!/usr/bin/env python3
"""Validate and import many individually shared, authorized educational files.

Example: python3 tools/import_materials_csv.py /path/to/approved_files.csv

The input CSV is private editorial source data; NEVER commit it to the public
GitHub repository. The program commits nothing automatically.
"""
import argparse
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

from add_material import KINDS, allowed_file_url

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "data/materials.json"
REQUIRED = {
    "title", "standard", "subject", "category", "description",
    "url", "rights_confirmed", "viewer_checked", "rights_basis"
}
BASIS = {"original", "written_permission", "open_license", "public_domain", "authorized_link"}
BOARDS = {"", "SSC", "HSC", "GSEB", "GSBSTB", "GSET", "Other"}


def clean(value):
    return " ".join(str(value or "").split()).strip()


def process(csv_path, output_path):
    if not csv_path.is_file() or csv_path.stat().st_size > 3_000_000:
        raise ValueError("CSV must exist and be at most 3 MB.")
    existing = json.loads(output_path.read_text(encoding="utf-8"))
    if not isinstance(existing, list):
        raise ValueError("Existing materials.json is not an array.")
    seen = {r.get("url") for r in existing if isinstance(r, dict)}
    draft = []
    errors = []
    duplicates = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED.issubset(set(reader.fieldnames)):
            raise ValueError("Missing CSV columns: " + ", ".join(sorted(REQUIRED-set(reader.fieldnames or []))))
        for row_number, row in enumerate(reader, start=2):
            if row_number > 3001:
                raise ValueError("At most 3,000 material entries per batch.")
            title = clean(row.get("title"))
            standard = clean(row.get("standard"))
            subject = clean(row.get("subject"))
            category = clean(row.get("category"))
            desc = clean(row.get("description"))
            url = clean(row.get("url"))
            license_basis = clean(row.get("rights_basis")).lower()
            allowed = clean(row.get("rights_confirmed")).lower() in {"yes", "true"}
            viewable = clean(row.get("viewer_checked")).lower() in {"yes", "true"}
            board = clean(row.get("board"))
            year = clean(row.get("year"))
            problems = []
            if not 8 <= len(title) <= 180:
                problems.append("title must be 8–180 characters")
            if not 1 <= len(standard) <= 60 or not 1 <= len(subject) <= 80:
                problems.append("standard and subject must be provided")
            if category not in KINDS:
                problems.append("invalid category")
            if not 20 <= len(desc) <= 500:
                problems.append("description must be 20–500 characters")
            if not allowed_file_url(url):
                problems.append("not an individual Drive/Docs/MEGA HTTPS file link")
            if not allowed or not viewable:
                problems.append("requires rights_confirmed=yes and viewer_checked=yes")
            if license_basis not in BASIS:
                problems.append("rights_basis must identify actual reuse authorization")
            if board not in BOARDS:
                problems.append("unsupported board label")
            if year and not re.fullmatch(r"20\d{2}", year):
                problems.append("year must be 20XX or blank")
            if any("<" in value or ">" in value for value in (title, standard, subject, desc)):
                problems.append("HTML must not be included")
            # A textbook hosted on MEGA is not automatically licensed to be republished
            # just because its PDF can be found on the Internet.
            if category == "Textbook" and license_basis == "authorized_link" and "mega.nz" in url:
                problems.append("for rehosted MEGA textbooks, confirm a license or written permission")
            if problems:
                errors.append(f"row {row_number} ({title[:45]}): " + "; ".join(problems))
                continue
            if url in seen:
                duplicates += 1
                continue
            seen.add(url)
            item = {
                "title": title,
                "standard": standard,
                "subject": subject,
                "category": category,
                "description": desc,
                "url": url,
                "updated_at": date.today().isoformat(),
                "status": "Approved",
                "rights_verified": True,
            }
            if board:
                item["board"] = board
            if year:
                item["year"] = year
            draft.append(item)
    if errors:
        raise ValueError("Batch not published. Correct all errors first:\n" + "\n".join(errors[:80]))
    if draft:
        output_path.write_text(json.dumps(draft + existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(draft), duplicates


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=Path, help="Private CSV with individually authorized file URLs")
    parser.add_argument("--output", type=Path, default=DEFAULT_JSON, help="Output JSON, default data/materials.json")
    args = parser.parse_args()
    try:
        added, skipped = process(args.csv_file, args.output)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"IMPORT REJECTED: {exc}") from exc
    print(f"PASS: added {added} individually approved files; skipped {skipped} duplicate URLs.")
    print("Review data/materials.json and site QA; publish through a separate Pull Request.")


if __name__ == "__main__":
    main()
