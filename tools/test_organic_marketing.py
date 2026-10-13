#!/usr/bin/env python3
"""Safety checks for voluntary WhatsApp shares and organic SEO home links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, parse_qs, unquote
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="a" and a.get("href"):
            self.links.append((a["href"],a))
def get(page):
    p=Links()
    p.feed((ROOT/page).read_text(encoding="utf-8"))
    return p.links
expected={
  "quiz.html":"site_share_quiz",
  "games.html":"site_share_games",
  "blog.html":"site_share_blog",
}
for name,slug in expected.items():
    pairs=get(name)
    share=[(url,a) for url,a in pairs if url.startswith("https://wa.me/?text=")]
    assert len(share)==1, name+": exactly one voluntary WhatsApp share CTA"
    raw,a=share[0]
    assert a.get("rel")=="noopener noreferrer" and a.get("target")=="_blank",name+": sharing link security"
    text=unquote(parse_qs(urlsplit(raw).query)["text"][0])
    assert "https://gyanshiksha.in/"+name+"?" in text,name+": share must land on the same Gyan Shiksha page"
    link=text.rsplit("https://",1)[-1]
    params=parse_qs(urlsplit("https://"+link).query)
    for key,value in {"utm_source":"whatsapp","utm_medium":"social","utm_campaign":"oct2026_students","utm_content":slug}.items():
        assert params.get(key)==[value],name+": "+key+" misconfigured"
    assert "ad click" not in text.lower(),name+": no ad-click incentive"
original=(ROOT/"quiz.html").read_text(encoding="utf-8")
assert "https://script.google.com/macros/s/AKfycbxM88Z2cZ1gVuXFU22R1ebiKmZywSqxPyr_VY669V_scB0eEdahGdSsRJn4AVzqQY4LXQ/exec" in original
home={x for x,_ in get("index.html")}
for path in (
    "blog-std10-quadratic-practice.html","blog-std10-chemical-equations.html",
    "blog-std10-english-grammar-practice.html","blog-std12-derivatives-practice.html",
    "blog-std12-current-electricity-circuits.html","blog-std12-english-email-writing.html"):
    assert path in home, "missing priority subject link on homepage: "+path
    # Grade articles are compiled by Jekyll from Markdown; the rendered link validator tests existence.
print("PASS: WhatsApp voluntary share links with UTM tags; six subject links on homepage; original Quiz preserved.")
