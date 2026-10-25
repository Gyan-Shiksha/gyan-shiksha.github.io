#!/usr/bin/env python3
"""Section-only news monitor. Never writes to a publishing Sheet or news feed."""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import time
from datetime import datetime, timezone
from urllib.parse import quote, urljoin, urlsplit, urlunsplit, parse_qsl, urlencode
from urllib.request import Request, urlopen, build_opener, HTTPRedirectHandler
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
MAX_DOWNLOAD = 10 * 1024 * 1024
SCHEMA = 1
CATEGORIES = {"Board Exam", "SSA", "UDISE+", "Recruitment", "Education News", "Circular", "Scholarship", "Other"}


def digest(value):
    return hashlib.sha256(value.encode("utf-8") if isinstance(value, str) else value).hexdigest()


def clean(value):
    return re.sub(r"\s+", " ", value).strip().lstrip("> ")


def canonical(url):
    p = urlsplit(url.strip())
    if p.scheme not in ("http", "https") or not p.hostname or p.username or p.password:
        raise ValueError("Only public HTTP(S) notice links are supported")
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not k.lower().startswith("utm_")]
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), quote(p.path, safe="/%:@!$&'()*+,;=-._~"), urlencode(query), ""))


class SourceRedirect(HTTPRedirectHandler):
    def __init__(self, allowed):
        self.allowed = set(allowed)

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlsplit(newurl).hostname not in self.allowed:
            raise ValueError("Source redirected outside its configured official hosts")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, allowed_hosts):
    url = canonical(url)
    if urlsplit(url).hostname not in set(allowed_hosts):
        raise ValueError("Source URL is outside its official-host allowlist")
    request = Request(url, headers={"User-Agent": "GyanShikshaNewsMonitor/1.0 (+https://gyanshiksha.in)", "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.5"})
    with build_opener(SourceRedirect(allowed_hosts)).open(request, timeout=25) as response:
        data = response.read(MAX_DOWNLOAD + 1)
        if len(data) > MAX_DOWNLOAD:
            raise ValueError("Source exceeds the 10 MiB download budget")
        return data


def extract(source, html):
    """Fail on missing/ambiguous section; never fall back to the whole page."""
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.select(source["section_selector"])
    if source.get("section_heading"):
        sections = [node for node in sections if node.select_one(source["section_heading_selector"])
                    and clean(node.select_one(source["section_heading_selector"]).get_text(" ", strip=True)) == source["section_heading"]]
    if len(sections) != 1:
        raise ValueError("Expected exactly one configured news section")
    section = sections[0]
    if source.get("content_selector"):
        nodes = section.select(source["content_selector"])
        if len(nodes) != 1:
            raise ValueError("Configured content section is missing or ambiguous")
        section = nodes[0]
    for node in section.select("script, style, nav, footer"):
        node.decompose()
    links = section.select(source["link_selector"])
    if not links:
        raise ValueError("No notice links in the configured section")
    items = {}
    for link in links:
        title = clean(link.get_text(" ", strip=True))
        if len(title) < 4:
            continue
        if source.get("exclude_pattern") and re.search(source["exclude_pattern"], title):
            continue
        if source.get("include_pattern") and not re.search(source["include_pattern"], title):
            continue
        try:
            url = canonical(urljoin(source["url"], link.get("href", "")))
        except ValueError:
            continue
        if urlsplit(url).hostname not in source["allowed_hosts"]:
            continue
        item_id = digest(url)
        items.setdefault(item_id, {"title": title, "url": url, "pdf_url": url if urlsplit(url).path.lower().endswith(".pdf") else ""})
    if not items and not source.get("include_pattern"):
        raise ValueError("Section links could not be parsed into valid official notices")
    return items


def empty_state():
    return {"schema": SCHEMA, "sources": {}, "outbox": {}, "delivered": {}, "health": {}, "notification_sequence": 0}


def load_state(path):
    if not path.exists():
        return empty_state()
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("schema") != SCHEMA or not all(isinstance(state.get(k), dict) for k in ("sources", "outbox", "delivered", "health")):
        raise ValueError("Invalid monitor state; refusing to reset the baseline silently")
    return state


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def render_news(item, source, kind, when):
    title = item["title"]
    summary = f'{source["name"]} દ્વારા “{title}” અંગેની સૂચના ઉપલબ્ધ છે. સંપૂર્ણ વિગતો અને લાગુ શરતો માટે મૂળ સત્તાવાર સૂચના વાંચો.'
    notes = f'{kind}; સ્ત્રોત: {source["id"]}; પ્રથમ નોંધાયેલ સમય: {when}. મૂળ પ્રકાશન તારીખ અલગથી ચકાસીને Dમાં ભરો.'
    if item.get("pdf_changed"):
        notes += " એ જ PDF લિંકની ફાઇલ બદલાઈ છે; ફક્ત metadata પણ બદલાયું હોઈ શકે. મૂળ PDF વાંચો."
    fields = {"A": source["category"], "B": title, "C": summary, "D": "", "E": item["url"], "F": item.get("pdf_url", ""),
              "G": "", "H": "Draft", "I": "", "J": notes, "K": ""}
    headline = ("સુધારેલી સૂચના: " if kind == "UPDATED" else "") + title
    post = f"📢 જ્ઞાન શિક્ષા\n\n{headline}\n\n{summary}\n\nસત્તાવાર સૂચના:\n{item['url']}\n\n— જ્ઞાન શિક્ષા\nhttps://gyanshiksha.in"
    labels = {"A": "વિભાગ", "B": "સમાચારનું શીર્ષક", "C": "ટૂંકી માહિતી", "D": "પ્રકાશન તારીખ", "E": "સત્તાવાર લિંક", "F": "PDF લિંક", "G": "છેલ્લી તારીખ", "H": "સ્થિતિ", "I": "ચકાસણી તારીખ", "J": "આંતરિક નોંધ", "K": "ફોટો લિંક"}
    lines = []
    for key, value in fields.items():
        display = "આપમેળે; હાથેથી ભરવાની નથી" if key == "I" else value or "ખાલી"
        lines.append(f"{key} — {labels[key]}:\n{display}")
    body = "એડમિન ફોર્મ માટેની વિગતો\n\n" + "\n\n".join(lines)
    body += "\n\n──────── WhatsApp માટે કોપી કરો ────────\n\n" + post
    body += "\n\n──────── માત્ર સંચાલક માટે ────────\nDની પ્રકાશન તારીખ અને મૂળ સૂચના ચકાસો. G ખાલી રાખો. I આપમેળે ભરાશે. Jની નોંધ જાહેર પોસ્ટમાં ન મૂકો."
    return {"kind": "news", "brand": "gyan_shiksha", "subject": f"[જ્ઞાન શિક્ષા] {kind} — {title}", "body": body,
            "fields": fields, "whatsapp": post, "review_required": True}


def enqueue(state, key, payload, now):
    if key not in state["outbox"] and key not in state["delivered"]:
        state["notification_sequence"] = state.get("notification_sequence", 0) + 1
        payload.update({"id": key, "created_at": now, "sequence": state["notification_sequence"]})
        state["outbox"][key] = payload


def scan(config, profiles, state, fetcher=fetch, now=None, pdf=True):
    now = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    state.setdefault("notification_sequence", max((e.get("sequence", 0) for e in state["outbox"].values()), default=0))
    results = []
    for source in config:
        if not source.get("enabled") or not profiles.get(source.get("brand"), {}).get("enabled"):
            continue
        # Adhyapak's basics are reserved; no delivery or Sheet integration is implemented.
        if source["brand"] != "gyan_shiksha" or source["category"] not in CATEGORIES:
            raise ValueError("Only configured Gyan Shiksha sources may run")
        sid = source["id"]
        previous = state["sources"].get(sid)
        identity = digest(json.dumps({k: source.get(k) for k in ("url", "brand", "section_selector", "section_heading", "content_selector", "link_selector", "include_pattern", "exclude_pattern")}, sort_keys=True))
        try:
            items = extract(source, fetcher(source["url"], source["allowed_hosts"]))
            baseline = previous is None or previous.get("identity") != identity
            record = {"identity": identity, "seen": {} if baseline else dict(previous["seen"]), "pdf_cursor": 0 if baseline else previous.get("pdf_cursor", 0)}
            for item_id, item in items.items():
                old = record["seen"].get(item_id, {})
                item["pdf_hash"] = old.get("pdf_hash", "")
            warnings = []
            candidates = [(key, item) for key, item in items.items() if item.get("pdf_url")][:source.get("pdf_window", 12)]
            if pdf and candidates:
                cursor = record["pdf_cursor"] % len(candidates)
                count = min(source.get("pdf_checks_per_run", 2), len(candidates))
                for offset in range(count):
                    key, item = candidates[(cursor + offset) % len(candidates)]
                    try:
                        data = fetcher(item["pdf_url"], source["allowed_hosts"])
                        if not data.lstrip().startswith(b"%PDF-"):
                            raise ValueError("Expected a PDF response")
                        new_hash = digest(data)
                        item["pdf_changed"] = bool(item["pdf_hash"] and item["pdf_hash"] != new_hash)
                        item["pdf_hash"] = new_hash
                    except Exception as exc:
                        warnings.append(type(exc).__name__ + ": PDF check failed")
                record["pdf_cursor"] = (cursor + count) % len(candidates)
            changed = 0
            for item_id, item in items.items():
                old = record["seen"].get(item_id)
                content_hash = digest(item["title"] + "\n" + item["url"])
                if not baseline and (old is None or old.get("content_hash") != content_hash or item.get("pdf_changed")):
                    event = "NEW" if old is None else "UPDATED"
                    payload = render_news(item, source, event, now)
                    event_id = digest(source["brand"] + item_id + content_hash + item["pdf_hash"])
                    enqueue(state, event_id, payload, now)
                    changed += 1
                record["seen"][item_id] = {"content_hash": content_hash, "pdf_hash": item["pdf_hash"]}
            health_before = state["health"].get(sid, {})
            state["sources"][sid] = record
            state["health"][sid] = {"last_success": now, "last_attempt": now, "failures": 0, "warnings": warnings}
            if health_before.get("failures", 0) >= 3:
                key = digest(sid + "recovered" + health_before.get("incident", ""))
                enqueue(state, key, {"kind": "health", "brand": "gyan_shiksha", "subject": f"[જ્ઞાન શિક્ષા] મોનીટર ફરી કાર્યરત — {sid}", "body": f"{source['name']}ની તપાસ ફરી સફળ થઈ. સમય: {now}"}, now)
            results.append({"source": sid, "status": "BASELINE" if baseline else "OK", "items": len(items), "changed": changed, "warnings": len(warnings)})
        except Exception as exc:
            prior = state["health"].get(sid, {})
            failures = prior.get("failures", 0) + 1
            incident = prior.get("incident", now) if prior.get("failures", 0) else now
            state["health"][sid] = {**prior, "last_attempt": now, "failures": failures, "incident": incident, "error": type(exc).__name__ + ": " + str(exc)[:180]}
            if failures >= 3:
                key = digest(sid + "error" + incident)
                enqueue(state, key, {"kind": "health", "brand": "gyan_shiksha", "subject": f"[જ્ઞાન શિક્ષા] સ્ત્રોતની તપાસ અટકી — {sid}", "body": f"{source['name']}ની સતત {failures} તપાસ નિષ્ફળ. આ સમાચાર નથી; મોનીટર તપાસવાની જરૂર છે. છેલ્લો પ્રયત્ન: {now}"}, now)
            results.append({"source": sid, "status": "SOURCE_ERROR", "error": state["health"][sid]["error"]})
    # Keep delivered IDs for 180 days; pending deliveries are never pruned.
    cutoff = time.time() - 180 * 86400
    state["delivered"] = {key: stamp for key, stamp in state["delivered"].items() if stamp >= cutoff}
    # The private Google mailer maintains a sequence cursor; retain a 90-day catch-up feed.
    feed_cutoff = datetime.now(timezone.utc).timestamp() - 90 * 86400
    state["outbox"] = {key: event for key, event in state["outbox"].items()
                       if datetime.fromisoformat(event["created_at"]).timestamp() >= feed_cutoff}
    state["last_run"] = now
    return results


def relay_send(event, url, secret):
    if not url.startswith("https://script.google.com/macros/s/") or not url.endswith("/exec"):
        raise ValueError("Relay must be the owner's deployed Google Apps Script /exec URL")
    payload = json.dumps({k: event[k] for k in ("id", "brand", "subject", "body")}, ensure_ascii=False, separators=(",", ":"))
    stamp = str(int(time.time()))
    signature = hmac.new(secret.encode(), (stamp + "\n" + payload).encode(), hashlib.sha256).hexdigest()
    request = Request(url, data=json.dumps({"timestamp": stamp, "payload": payload, "signature": signature}).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=45) as response:
        result = json.loads(response.read(65536))
    if result.get("ok") is not True:
        raise ValueError("Relay did not acknowledge the delivery: " + str(result.get("error", "unknown")))


def deliver(state, path, sender=relay_send, limit=30):
    url, secret = os.environ.get("GYAN_RELAY_URL", ""), os.environ.get("GYAN_RELAY_SECRET", "")
    if not url or not secret:
        raise ValueError("Mail relay secrets are not configured; pending messages are preserved")
    sent = 0
    for event_id, event in list(state["outbox"].items())[:limit]:
        if event["brand"] != "gyan_shiksha":
            raise ValueError("Adhyapak delivery is deferred")
        sender(event, url, secret)
        state["delivered"][event_id] = time.time()
        del state["outbox"][event_id]
        save_json(path, state)
        sent += 1
    return sent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["scan", "deliver"])
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--config", type=Path, default=ROOT / "sources.json")
    parser.add_argument("--profiles", type=Path, default=ROOT / "profiles.json")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-pdf", action="store_true")
    args = parser.parse_args()
    state = load_state(args.state)
    if args.command == "deliver":
        if args.dry_run:
            print(json.dumps({"pending": len(state["outbox"]), "sent": 0}))
        else:
            print(json.dumps({"sent": deliver(state, args.state), "pending": len(state["outbox"])}))
        return
    results = scan(json.loads(args.config.read_text()), json.loads(args.profiles.read_text()), state, pdf=not args.no_pdf)
    if not args.dry_run:
        save_json(args.state, state)
    if args.output:
        save_json(args.output, {"results": results, "pending": list(state["outbox"].values())})
    print(json.dumps({"dry_run": args.dry_run, "results": results, "pending": len(state["outbox"])}, ensure_ascii=False))
    if any(result["status"] == "SOURCE_ERROR" for result in results):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
