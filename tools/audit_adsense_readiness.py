#!/usr/bin/env python3
"""Read-only AdSense preflight: factual repository checks, NOT an approval score."""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit


def audit(root: Path) -> tuple[dict, list]:
    catalogue = json.loads((root / 'data/materials.json').read_text(encoding='utf-8'))
    if not isinstance(catalogue, list):
        raise ValueError('materials.json must contain a list')
    html_pages = list(root.glob('*.html'))
    articles = list((root / '_posts').glob('*.md'))
    counts = Counter(x.get('category', '(missing)') for x in catalogue)
    bad_urls = []
    needs_review = []
    rows = []
    delivery_hosts = Counter()
    missing_original_sources = 0
    for idx, item in enumerate(catalogue, 1):
        url = str(item.get('url', '')).strip()
        title = str(item.get('title', '')).strip()
        p = urlsplit(url)
        delivery_hosts[p.hostname or '(missing)'] += 1
        if p.scheme != 'https' or p.hostname not in {'drive.google.com','docs.google.com','mega.nz','mega.io'}:
            bad_urls.append(idx)
        # A hosting link or an existing rights_verified flag does not identify
        # the original government publication or grant redistribution rights.
        source_url = str(item.get('original_official_source_url') or item.get('source_url') or '').strip()
        if not source_url:
            missing_original_sources += 1
        needs_review.append(idx)
        rows.append({
            'catalogue_row': idx,
            'title': title,
            'standard': item.get('standard', ''),
            'subject': item.get('subject', ''),
            'year': item.get('year', ''),
            'category': item.get('category', ''),
            'file_url': url,
            'file_host': p.hostname or '',
            'original_official_source_url': source_url,
            'publisher_board_or_department': item.get('publisher', ''),
            'official_copyright_policy_url': item.get('copyright_policy_url', ''),
            'right_to_link_or_redistribute': '',
            'external_link_or_uploaded_copy': '',
            'third_party_copyright_exception_checked': '',
            'rights_verified_flag': item.get('rights_verified', False),
            'independent_rights_evidence': 'PENDING HUMAN REVIEW',
            'source_owner_or_license': '',
            'review_decision': 'PENDING',
            'review_date': '',
            'reviewer': '',
        })
    required = ['about.html','contact.html','privacy.html','terms.html',
                'disclaimer.html','editorial-policy.html','robots.txt','sitemap.xml']
    missing = [name for name in required if not (root / name).is_file()]
    sitemap = (root / 'sitemap.xml').read_text(encoding='utf-8') if (root / 'sitemap.xml').exists() else ''
    site = {'html_source_pages': len(html_pages), 'jekyll_articles': len(articles),
            'materials_total': len(catalogue), 'material_categories': dict(counts),
            'rights_flags_true': sum(item.get('rights_verified') is True for item in catalogue),
            'hosting_domains_not_original_publishers': dict(delivery_hosts),
            'entries_without_recorded_official_source_url': missing_original_sources,
            'independent_rights_reviews_still_required': len(needs_review),
            'catalogue_non_allowlisted_urls': len(bad_urls),
            'missing_required_pages': missing,
            'sitemap_has_blog_template': '{% for post in site.posts %}' in sitemap,
            'adsense_code_seen_in_source_html': any('adsbygoogle.js' in p.read_text(encoding='utf-8')
                                                  for p in html_pages),
            'checks_not_possible_in_repo': [
                'Google AdSense account eligibility or approval',
                'actual GSC indexing / real search traffic',
                'PDF original official publishing page, copyright terms, and any third-party rights exceptions',
                'third-party PDF/MEGA public access',
                'production device performance and student privacy handling',
            ],
            'recommendation': 'HOLD APPLICATION pending rights evidence and live QA',
            'not_an_official_google_score': True}
    return site, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--rights-csv', type=Path, help='Optional owner rights-review checklist file')
    args = parser.parse_args()
    summary, rows = audit(args.root)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.rights_csv:
        args.rights_csv.parent.mkdir(parents=True, exist_ok=True)
        with args.rights_csv.open('w', encoding='utf-8-sig', newline='') as f:
            out = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else
                                 ['catalogue_row','title','standard','subject','year','category','file_url',
                                  'file_host','original_official_source_url','publisher_board_or_department',
                                  'official_copyright_policy_url','right_to_link_or_redistribute',
                                  'external_link_or_uploaded_copy','third_party_copyright_exception_checked',
                                  'rights_verified_flag','independent_rights_evidence','source_owner_or_license',
                                  'review_decision','review_date','reviewer'])
            out.writeheader()
            out.writerows(rows)
        print(f'Owner review checklist generated: {args.rights_csv} ({len(rows)} rows)')

if __name__ == '__main__':
    main()
