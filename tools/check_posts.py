#!/usr/bin/env python3
"""Editorial quality gate for original Gujarati Jekyll article sources."""
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
issues=[]
posts=sorted((ROOT/"_posts").glob("*.md"))
reserved={p.name for p in ROOT.glob("blog-*.html")}
paths=set()
for path in posts:
    m=re.fullmatch(r"(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md",path.name)
    if not m:
        issues.append(f"{path.name}: use YYYY-MM-DD-english-slug.md")
        continue
    date_text,slug=m.groups()
    try:
        date.fromisoformat(date_text)
    except ValueError:
        issues.append(f"{path.name}: invalid calendar date")
    url="blog-"+slug+".html"
    if url in reserved or url in paths:
        issues.append(f"{path.name}: URL collides with existing article")
    paths.add(url)
    source=path.read_text(encoding="utf-8")
    if not source.startswith("---\n") or "\n---\n" not in source:
        issues.append(f"{path.name}: missing front matter")
        continue
    front,body=source[4:].split("\n---\n",1)
    meta={}
    for line in front.splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k,v=line.split(":",1)
            meta[k.strip()]=v.strip().strip("\"'")
    for key in ("title","description","summary","date","category","image"):
        if not meta.get(key):
            issues.append(f"{path.name}: missing {key}")
    if meta.get("date")!=date_text or meta.get("layout")!="post":
        issues.append(f"{path.name}: date must match filename and layout must be post")
    if len(body.strip())<2000 or len(re.findall(r"(?m)^## ",body))<3:
        issues.append(f"{path.name}: substantive original lesson with at least 3 sections required")
    if not re.search(r"(?i)જાતે કરો|પ્રેક્ટિસ|સ્વઅભ્યાસ|example|ઉદાહરણ",body):
        issues.append(f"{path.name}: must contain worked example or actionable practice")
    if re.search(r"<\s*(?:script|iframe|form)\b",body,re.I):
        issues.append(f"{path.name}: embedded scripts/iframes/forms are not allowed")
    if "adhyapak-saathi.github.io/Gyanshiksha" in source:
        issues.append(f"{path.name}: old host")
    image=meta.get("image","")
    if not image.startswith("/assets/img/") or not (ROOT/image.lstrip("/")).is_file():
        issues.append(f"{path.name}: image must exist under site assets/img")
    if len(meta.get("description",""))>200:
        issues.append(f"{path.name}: keep SEO description under 200 characters")
if issues:
    raise SystemExit("Article quality QA FAILED:\n"+"\n".join(issues))
print(f"PASS: {len(posts)} substantive educational Markdown posts with metadata, images and practice.")
