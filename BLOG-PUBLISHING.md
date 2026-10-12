# Gyan Shiksha: publishing a new Blog article

1. In the NEW Gyan-Shiksha repository, create a Markdown file in _posts/ named YYYY-MM-DD-english-slug.md (example: 2026-10-12-healthy-study-habits.md).
2. Start the file with YAML front matter; layout: post is mandatory. Write original Gujarati content below it.
3. Commit the Markdown file to main. GitHub Pages/Jekyll automatically creates the HTML page and a card on blog.html. The sitemap includes new post URLs automatically.
4. Existing seven manually authored blog HTML pages retain their original URLs. Do not reuse a previous blog slug.
5. Do not add a .nojekyll file: Jekyll is required for this publishing workflow.

Example source (copy, then edit and publish):

~~~markdown
---
layout: post
title: "અભ્યાસમાં સુધારવા માટે પાંચ સારી ટેવો"
description: "ગુજરાતી માધ્યમના વિદ્યાર્થીઓ માટે આયોજન અને પુનરાવર્તન અંગે માર્ગદર્શન."
category: "અભ્યાસ માર્ગદર્શન"
summary: "પ્રેક્ટિસ, પુનરાવર્તન અને અભ્યાસ આયોજનની ઉપયોગી રીતો."
date: 2026-10-12
---

## પહેલી ટેવ

અહીં તમારું મૂળ લખાણ ઉમેરો.

## બીજી ટેવ

અહીં પ્રેક્ટિકલ ઉદાહરણ ઉમેરો.
~~~

The example is NOT published automatically. Save it as _posts/YYYY-MM-DD-your-slug.md to publish.

Example URL: https://gyanshiksha.in/blog-healthy-study-habits.html

Template: _layouts/post.html (shared design, navigation, metadata and GA4).
Blog index: blog.html (new posts automatically shown before legacy posts).
Sitemap: sitemap.xml (Jekyll adds new post URLs on deployment).
Local SEO check: python tools/build_sitemap.py && python tools/validate_site.py

Security: never insert untrusted scripts, embeds or copied copyrighted articles into Markdown posts.
