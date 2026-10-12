#!/usr/bin/env python3
"""Safely prepare verified News/Jobs feed entries from a PRIVATE editorial CSV.

Export only an appropriate tab of the restricted Google Sheet to a local CSV.
Never publish the source CSV or Google credentials to this public repository.
Usage:
  python3 tools/import_editorial_csv.py --feed news --csv /private/News.csv
  python3 tools/import_editorial_csv.py --feed news --csv /private/News.csv --write
The default is DRY RUN; --write updates local data/news.json for a reviewed PR.
"""
import argparse
import csv
from datetime import date, timedelta
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = {
    "news": {"date","title","category","summary","source_url","pdf_url","status","last_verified"},
    "jobs": {"date","title","category","summary","source_url","pdf_url","deadline","status","last_verified"},
}

def clean(value):
    return " ".join(str(value or "").split()).strip()

def parse_date(value, field, row):
    text = clean(value)
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
            raise ValueError()
        return date.fromisoformat(text)
    except ValueError:
        raise ValueError(f"row {row}: {field} must be YYYY-MM-DD (real date)") from None

def safe_url(value, row, field, required=True):
    value = clean(value)
    if not value and not required:
        return ""
    u = urlsplit(value)
    if (u.scheme != "https" or not u.hostname or u.username or u.password or
            any(x in value for x in ('<','>','"')) or len(value) > 1200):
        raise ValueError(f"row {row}: {field} must be a valid HTTPS official-source URL")
    if u.hostname.lower() in {"localhost", "127.0.0.1"}:
        raise ValueError(f"row {row}: local source URL not permitted")
    return value

def convert(feed, input_csv, today=None):
    today = today or date.today()
    if not input_csv.is_file() or input_csv.stat().st_size > 1_500_000:
        raise ValueError("Private CSV must exist and be at most 1.5 MB")
    records = []
    seen = set()
    with input_csv.open(encoding="utf-8-sig", newline="") as stream:
        rows = csv.DictReader(stream)
        expected = COLUMNS[feed]
        if not rows.fieldnames or not expected.issubset(set(rows.fieldnames)):
            raise ValueError("Missing Sheet columns: " + ", ".join(sorted(expected-set(rows.fieldnames or []))))
        for n, r in enumerate(rows, start=2):
            if n > 1002:
                raise ValueError("At most 1,000 editorial rows per batch")
            status = clean(r.get("status"))
            if status not in {"Approved", "Published"}:
                continue  # Draft, Review, rejected, or incomplete rows never go public.
            title, category, summary = [clean(r.get(x)) for x in ("title", "category", "summary")]
            if not 12 <= len(title) <= 170 or not 3 <= len(category) <= 60:
                raise ValueError(f"row {n}: add a clear original title and valid category")
            if not 80 <= len(summary) <= 900 or any(c in title+summary for c in "<>"):
                raise ValueError(f"row {n}: write original Gujarati summary (80–900 chars), no HTML")
            date_value = parse_date(r.get("date"), "date", n)
            checked = parse_date(r.get("last_verified"), "last_verified", n)
            if date_value > today + timedelta(days=1) or checked > today:
                raise ValueError(f"row {n}: publication/review date cannot be in the future")
            if checked < today - timedelta(days=45):
                raise ValueError(f"row {n}: editorial verification older than 45 days, recheck official source")
            source = safe_url(r.get("source_url"), n, "source_url")
            pdf = safe_url(r.get("pdf_url"), n, "pdf_url", required=False)
            record = {"date":date_value.isoformat(),"title":title,"category":category,
                      "summary":summary,"source_url":source,"status":"Approved"}
            if pdf:
                record["pdf_url"] = pdf
            if feed == "jobs":
                deadline = clean(r.get("deadline"))
                if deadline:
                    due = parse_date(deadline, "deadline", n)
                    if due < today:
                        continue  # Expired vacancy is not newly published.
                    record["deadline"] = due.isoformat()
            key = (source, title.casefold())
            if key not in seen:
                seen.add(key)
                records.append(record)
    return records

def prepare(feed, csv_path, json_path, write=False, today=None):
    incoming = convert(feed, csv_path, today=today)
    existing = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(existing, list):
        raise ValueError(f"{json_path}: existing feed is not a list")
    # Do not silently delete previously published information. Updating the
    # same title/source with a newly reviewed summary is allowed.
    combined = {(r.get("source_url"), str(r.get("title","")).casefold()):r for r in existing}
    for row in incoming:
        combined[(row["source_url"],row["title"].casefold())] = row
    result = sorted(combined.values(), key=lambda r:(str(r.get("date","")),str(r.get("title",""))),reverse=True)
    if write:
        json_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return len(incoming), len(result)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--feed",choices=("news","jobs"),required=True)
    p.add_argument("--csv",type=Path,required=True,help="Restricted local Google Sheet export (never commit)")
    p.add_argument("--write",action="store_true",help="Actually update public JSON file; default dry-run")
    args=p.parse_args()
    path=ROOT/"data"/(args.feed+".json")
    try:
        added,total=prepare(args.feed,args.csv,path,write=args.write)
    except (OSError,ValueError,TypeError,json.JSONDecodeError) as e:
        raise SystemExit("EDITORIAL PUBLISH REJECTED: "+str(e))
    print(f"{'PREPARED' if args.write else 'DRY RUN'}: {added} validated input entries; {total} published/retained entries in {args.feed}.")
    print("Review official notices and Git diff. Only a QA-passed PR may deploy; no Sheet credentials used.")

if __name__=="__main__":
    main()
