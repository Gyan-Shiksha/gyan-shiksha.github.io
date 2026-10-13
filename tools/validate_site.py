from pathlib import Path
import os
import re
from urllib.parse import urlparse

ROOT = Path(os.environ.get("GYAN_SITE_ROOT", Path(__file__).resolve().parents[1])).resolve()
errors = []
SITE_ORIGIN = "https://gyanshiksha.in"
OLD_SITE_ORIGIN = "https://adhyapak-saathi.github.io/Gyanshiksha"
html_pages = [p for p in ROOT.glob("*.html") if not re.fullmatch(r"google[0-9a-f]{16}\.html", p.name)]
# Jekyll posts have no HTML file in the source tree, only after the build.
# Validate those source links against _posts here; the rendered pass checks real files.
post_urls = { "blog-" + m.group(1) + ".html" for p in (ROOT / "_posts").glob("*.md") if (m := re.fullmatch(r"\d{4}-\d{2}-\d{2}-(.+)\.md", p.name)) }
rendered_root = bool(os.environ.get("GYAN_SITE_ROOT"))

def get_meta(text, name):
    m = re.search(rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"', text, re.I)
    return m.group(1) if m else ""

def robots_for(text):
    return get_meta(text, "robots").lower()

def is_indexable(text):
    return "noindex" not in robots_for(text)

indexable = set()
noindex = set()

for page in html_pages:
    text = page.read_text(encoding="utf-8")
    if page.name == "study-plan.html":
        # Intentional noindex redirect stub; full page metadata is unnecessary.
        if OLD_SITE_ORIGIN in text:
            errors.append(f"{page.name}: stale old-domain URL")
        continue
    robots = robots_for(text)
    if OLD_SITE_ORIGIN in text:
        errors.append(f"{page.name}: stale old-domain URL")
    if "noindex" not in robots:
        canonical = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', text, re.I)
        if canonical and not canonical.group(1).startswith(SITE_ORIGIN + "/"):
            errors.append(f"{page.name}: canonical is not on the primary domain")
        og_url = re.search(r'<meta\s+property="og:url"\s+content="([^"]+)"', text, re.I)
        if og_url and not og_url.group(1).startswith(SITE_ORIGIN + "/"):
            errors.append(f"{page.name}: og:url is not on the primary domain")
    (noindex if "noindex" in robots else indexable).add(page.name)

    if os.environ.get("GYAN_SITE_ROOT") and page.name not in {"quiz-player.html", "study-plan.html"}:
        if text.count('<header class="site-header">') != 1:
            errors.append(f"{page.name}: expected a single rendered shared header")
        if text.count('<footer class="site-footer">') != 1:
            errors.append(f"{page.name}: expected a single rendered shared footer")
    if "<title>" not in text:
        errors.append(f"{page.name}: missing title")
    if page.name != "404.html" and not get_meta(text, "description"):
        errors.append(f"{page.name}: missing meta description")
    if 'rel="manifest"' not in text:
        errors.append(f"{page.name}: manifest link missing")

    # Exactly one H1 is expected on every HTML page, including utility pages.
    h1_count = len(re.findall(r"<h1\b", text, re.I))
    if h1_count != 1:
        errors.append(f"{page.name}: expected exactly one h1, found {h1_count}")

    # Internal HTML links.
    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith(("mailto:", "#", "javascript:", "tel:")):
            continue
        if href.startswith(("http://", "https://")):
            continue
        clean = href.split("#", 1)[0].split("?", 1)[0]
        if clean.endswith(".html"):
            # Static root-relative links are valid in Jekyll-generated posts.
            target = (ROOT / clean.lstrip("/") if clean.startswith("/") else page.parent / clean).resolve()
            jekyll_post_will_build = (not rendered_root and clean.lstrip("/") in post_urls)
            if not target.is_relative_to(ROOT) or (not target.is_file() and not jekyll_post_will_build):
                errors.append(f"{page.name}: broken internal link -> {href}")

    # Production indexable pages must not expose development placeholders or ads.
    if is_indexable(text):
        for forbidden in ["Coming Soon", "Library structure ready", "<time>Demo</time>"]:
            if forbidden in text:
                errors.append(f"{page.name}: production placeholder -> {forbidden}")
        if 'class="ad-wrap' in text or 'data-ad-slot=' in text:
            errors.append(f"{page.name}: pre-approval ad placeholder still present")

        # Indexable pages need canonical + social metadata.
        if 'rel="canonical"' not in text:
            errors.append(f"{page.name}: canonical missing")
        for token in ['property="og:image"', 'content="image/png"', 'name="twitter:card"']:
            if token not in text:
                errors.append(f"{page.name}: social metadata missing -> {token}")

    # target=_blank requires noopener/noreferrer.
    for tag in re.findall(r'<a\b[^>]*target="_blank"[^>]*>', text, re.I):
        if 'rel="noopener' not in tag and 'rel="noreferrer' not in tag:
            errors.append(f"{page.name}: target=_blank without noopener")

    # External content images should reserve layout space and have alt text.
    for tag in re.findall(r'<img\b[^>]*>', text, re.I):
        src_m = re.search(r'src="([^"]+)"', tag)
        src = src_m.group(1) if src_m else ""
        if src.startswith("http"):
            if 'width="' not in tag or 'height="' not in tag:
                errors.append(f"{page.name}: external image missing width/height -> {src}")
            if 'alt="' not in tag:
                errors.append(f"{page.name}: external image missing alt -> {src}")

    # CSP should be least-privilege for framing.
    if page.name in {"quiz.html", "quiz-player.html"}:
        if "frame-src https://script.google.com https://script.googleusercontent.com;" not in text:
            errors.append(f"{page.name}: Google Apps Script frame permission missing")
    elif page.name in {"contact.html", "study-material.html"}:
        # These forms also allow the dedicated Googleusercontent subdomain.
        if "frame-src https://script.google.com https://script.googleusercontent.com https://*.googleusercontent.com;" not in text:
            errors.append(f"{page.name}: approved form frame permission missing")
    else:
        if "frame-src 'none';" not in text:
            errors.append(f"{page.name}: frame-src should be none")

    # Unsplash preconnect should exist only where rendered assets use it.
    has_preconnect = 'rel="preconnect" href="https://images.unsplash.com"' in text
    if page.name in {"index.html"}:
        if not has_preconnect:
            errors.append(f"{page.name}: Unsplash preconnect missing")
    elif has_preconnect:
        errors.append(f"{page.name}: unnecessary Unsplash preconnect")

# Specific content-integrity checks.
index_text = (ROOT / "index.html").read_text(encoding="utf-8")
for stale in ["Model Papers", "Latest Updates"]:
    if stale in index_text:
        errors.append(f"index.html: stale/unavailable feature claim -> {stale}")

app_js = (ROOT / "assets/js/app.js").read_text(encoding="utf-8")
if "Model Paper" in app_js:
    errors.append("assets/js/app.js: stale Model Paper search suggestion")

terms = (ROOT / "terms.html").read_text(encoding="utf-8")
if 'meta name="robots" content="index,follow,max-image-preview:large"' not in terms:
    errors.append("terms.html: explicit robots meta missing")

for article in [
    "blog-board-study-plan.html", "blog-smart-revision.html", "blog-self-test.html",
    "blog-answer-writing.html", "blog-math-practice.html", "blog-exam-week.html"
]:
    text = (ROOT / article).read_text(encoding="utf-8")
    if 'class="breadcrumbs"' not in text:
        errors.append(f"{article}: breadcrumbs missing")
    if 'class="related-guides"' not in text:
        errors.append(f"{article}: related guides missing")
    if 'meta name="author"' not in text:
        errors.append(f"{article}: author meta missing")

# Sitemap consistency.
sitemap_path = ROOT / "sitemap.xml"
if sitemap_path.exists():
    sitemap = sitemap_path.read_text(encoding="utf-8")
    sitemap_files = set()
    for loc in re.findall(r"<loc>(.*?)</loc>", sitemap):
        path = urlparse(loc).path
        name = "index.html" if path.endswith("/") else path.split("/")[-1]
        sitemap_files.add(name)

    for name in noindex:
        if name in sitemap_files:
            errors.append(f"sitemap includes noindex page -> {name}")
    for name in indexable:
        if name == "404.html":
            continue
        if name not in sitemap_files:
            errors.append(f"sitemap missing indexable page -> {name}")
else:
    errors.append("sitemap.xml missing")

# Verify the custom domain and sitemap sources.
if (ROOT / "CNAME").read_text(encoding="utf-8").strip() != "gyanshiksha.in":
    errors.append("CNAME must be gyanshiksha.in")
if sitemap_path.exists():
    sitemap_source = sitemap_path.read_text(encoding="utf-8")
    if OLD_SITE_ORIGIN in sitemap_source:
        errors.append("sitemap: stale old-domain URL")
    for link in re.findall(r"<loc>([^{}<>]+)</loc>", sitemap_source):
        if not link.startswith(SITE_ORIGIN + "/"):
            errors.append(f"sitemap: external canonical URL -> {link}")

# Main navigation must not promote noindex/development pages.
for page in html_pages:
    text = page.read_text(encoding="utf-8")
    nav = re.search(r'<nav id="main-nav".*?</nav>', text, re.S)
    if not nav:
        continue
    for href in re.findall(r'href="([^"]+\.html)"', nav.group(0)):
        if href in noindex:
            errors.append(f"{page.name}: main nav links to noindex page -> {href}")

# Required root/security/PWA assets.
for required in [
    "robots.txt", "site.webmanifest", "security.txt", ".well-known/security.txt",
    "security.html", "assets/img/icon-180.png", "assets/img/icon-192.png", "assets/img/icon-512.png",
    "assets/img/og-cover.png"
]:
    if not (ROOT / required).exists():
        errors.append(f"{required} missing")

# Manifest should reference raster icons.
manifest = (ROOT / "site.webmanifest").read_text(encoding="utf-8")
for icon in ["assets/img/icon-192.png", "assets/img/icon-512.png"]:
    if icon not in manifest:
        errors.append(f"manifest missing icon -> {icon}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print(f"Professional QA validation passed: {len(html_pages)} HTML pages, {len(indexable)} indexable, {len(noindex)} noindex.")
