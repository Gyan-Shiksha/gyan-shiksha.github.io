from pathlib import Path
from xml.sax.saxutils import escape
import re

BASE_URL = "https://gyanshiksha.in"
ROOT = Path(__file__).resolve().parents[1]

pages = []
for p in sorted(ROOT.glob("*.html")):
    if p.name == "404.html" or re.fullmatch(r"google[0-9a-f]{16}\.html", p.name):
        continue
    text = p.read_text(encoding="utf-8")
    robots = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', text, re.I)
    if robots and "noindex" in robots.group(1).lower():
        continue
    pages.append(p.name)

lines = ['---', 'layout: null', '---', '<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for name in pages:
    url = BASE_URL + ("/" if name == "index.html" else f"/{name}")
    lines.append(f"  <url><loc>{escape(url)}</loc></url>")
lines.append("  {% for post in site.posts %}")
lines.append("  <url><loc>{{ site.url }}{{ post.url }}</loc></url>")
lines.append("  {% endfor %}")
lines.append("</urlset>")

(ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Generated sitemap for {len(pages)} indexable pages.")
