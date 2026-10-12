#!/usr/bin/env python3
"""No-network tests: editorial import must fail closed and preserve published data."""
import csv
from datetime import date
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from import_editorial_csv import prepare, convert

TODAY = date(2026, 10, 12)
NEWS_HEADER = ["date","title","category","summary","source_url","pdf_url","status","editorial_notes","last_verified"]
JOBS_HEADER = ["date","title","category","summary","source_url","pdf_url","deadline","status","editorial_notes","last_verified"]

def make_csv(path, header, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def news_row(**extra):
    row = {"date":"2026-10-12","title":"અભ્યાસ માટે સત્તાવાર નમૂનાની જાણકારી",
           "category":"Board Exam",
           "summary":"આ માત્ર સ્થાનિક પરીક્ષણ માટેનું ઉદાહરણ છે. તેમાં વિદ્યાર્થીઓ માટે તારીખ, પગલાં અને મૂળ સત્તાવાર સ્રોત અલગથી સમજાવવામાં આવ્યા છે.",
           "source_url":"https://www.gseb.org/","pdf_url":"","status":"Approved",
           "editorial_notes":"","last_verified":"2026-10-12"}
    row.update(extra)
    return row

def run():
    with TemporaryDirectory() as dirname:
        root = Path(dirname)
        news = root/"News.csv"
        target = root/"news.json"
        target.write_text("[]\n",encoding="utf-8")
        make_csv(news,NEWS_HEADER,[news_row(status="Draft"), news_row(status="Review")])
        assert prepare("news",news,target,today=TODAY)==(0,0)
        assert json.loads(target.read_text())==[]
        make_csv(news,NEWS_HEADER,[news_row()])
        assert prepare("news",news,target,today=TODAY)==(1,1)
        assert json.loads(target.read_text())==[],"Dry run must not change file"
        assert prepare("news",news,target,write=True,today=TODAY)==(1,1)
        assert prepare("news",news,target,write=True,today=TODAY)==(1,1)
        assert len(json.loads(target.read_text()))==1,"Publishing must be idempotent"
        for invalid in [
            news_row(last_verified=""),
            news_row(last_verified="2026-01-01"),
            news_row(source_url="http://example.com/notice"),
            news_row(date="2026-11-20"),
            news_row(summary="ટૂંકું"),
            news_row(title="<script>લિંક</script>"),
        ]:
            make_csv(news,NEWS_HEADER,[invalid])
            try:
                convert("news",news,today=TODAY)
                raise AssertionError(f"Invalid row accepted: {invalid}")
            except ValueError:
                pass
        make_csv(news,NEWS_HEADER,[news_row(status="Draft"),news_row(source_url="https://gseb.org/")])
        assert len(convert("news",news,today=TODAY))==1
        jobs = root/"Jobs.csv"
        make_csv(jobs,JOBS_HEADER,[{**news_row(), "deadline":"2026-10-11"}])
        assert convert("jobs",jobs,today=TODAY)==[],"Expired jobs cannot be published"
        make_csv(jobs,JOBS_HEADER,[{**news_row(), "deadline":"2026-11-01"}])
        assert len(convert("jobs",jobs,today=TODAY))==1
        print("PASS: approved-only publishing, dated verification, expiry, no public drafts, idempotence and dry run")

if __name__=="__main__":
    run()
