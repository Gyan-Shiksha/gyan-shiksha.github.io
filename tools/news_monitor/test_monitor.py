import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location("monitor", ROOT / "monitor.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def page(items, banner="outside"):
    anchors = ''.join(f'<a href="{url}">{title}</a>' for title, url in items)
    return f'<nav>{banner}</nav><div id="news">{anchors}</div><footer>{banner}</footer>'.encode()


class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.source = {"id":"test", "enabled":True, "brand":"gyan_shiksha", "name":"સત્તાવાર બોર્ડ", "url":"https://school.example/", "section_selector":"#news", "link_selector":"a[href]", "category":"Board Exam", "allowed_hosts":["school.example"], "pdf_window":10, "pdf_checks_per_run":2}
        self.profiles = {"gyan_shiksha":{"enabled":True}, "adhyapak_saathi":{"enabled":False}}
        self.items = [("ધોરણ ૧૦ પરીક્ષાની સૂચના", "/notice.pdf")]
        self.state = m.empty_state()
        self.now = "2026-10-25T08:00:00+00:00"

    def run_scan(self, html, pdf=None, **kwargs):
        def fetch(url, allowed):
            return pdf if url.endswith('.pdf') and pdf is not None else html
        return m.scan([self.source], self.profiles, self.state, fetcher=fetch, now=self.now, pdf=pdf is not None, **kwargs)

    def baseline(self):
        return self.run_scan(page(self.items))

    def test_first_run_baselines_without_old_alerts(self):
        self.assertEqual(self.baseline()[0]['status'], 'BASELINE')
        self.assertFalse(self.state['outbox'])

    def test_new_notice_one_event_even_on_repeat(self):
        self.baseline()
        html = page(self.items + [("ધોરણ ૧૨ની નવી સૂચના", "/second.pdf")])
        self.run_scan(html)
        self.run_scan(html)
        self.assertEqual(len(self.state['outbox']), 1)
        self.assertIn('NEW', next(iter(self.state['outbox'].values()))['subject'])

    def test_order_banner_and_whitespace_do_not_alert(self):
        self.items.append(("શિષ્યવૃત્તિ જાહેરાત", "/two.pdf"))
        self.baseline()
        reordered = [("  શિષ્યવૃત્તિ    જાહેરાત ", "/two.pdf"), self.items[0]]
        self.run_scan(page(reordered, banner="new counter 999"))
        self.assertFalse(self.state['outbox'])

    def test_same_link_changed_title_is_updated(self):
        self.baseline()
        self.run_scan(page([("ધોરણ ૧૦ પરીક્ષાની સુધારેલી સૂચના", "/notice.pdf")]))
        self.assertIn('UPDATED', next(iter(self.state['outbox'].values()))['subject'])

    def test_same_pdf_url_changed_bytes(self):
        self.run_scan(page(self.items), pdf=b'%PDF-1.4 first')
        self.run_scan(page(self.items), pdf=b'%PDF-1.4 second')
        event = next(iter(self.state['outbox'].values()))
        self.assertIn('UPDATED', event['subject'])
        self.assertIn('metadata', event['fields']['J'])

    def test_later_pdf_hash_initialization_does_not_alert(self):
        self.baseline()
        self.run_scan(page(self.items), pdf=b'%PDF-1.4 first')
        self.assertFalse(self.state['outbox'])

    def test_missing_section_does_not_fall_back_to_page(self):
        self.baseline()
        old = copy.deepcopy(self.state['sources'])
        result = self.run_scan(b'<a href="https://school.example/new.pdf">new</a>')
        self.assertEqual(result[0]['status'], 'SOURCE_ERROR')
        self.assertEqual(self.state['sources'], old)
        self.assertFalse(self.state['outbox'])

    def test_third_failure_single_health_alert_and_recovery(self):
        self.baseline()
        for _ in range(4): self.run_scan(b'<html>broken</html>')
        self.assertEqual(len(self.state['outbox']), 1)
        self.assertEqual(next(iter(self.state['outbox'].values()))['kind'], 'health')
        self.baseline()
        self.assertEqual(len(self.state['outbox']), 2)

    def test_external_and_javascript_links_ignored(self):
        html = page(self.items + [('External notice', 'https://elsewhere.example/new.pdf'), ('Click it', 'javascript:go()')])
        self.assertEqual(len(m.extract(self.source, html)), 1)

    def test_config_change_establishes_fresh_baseline(self):
        self.baseline()
        self.source['section_selector'] = '#different'
        html = page([('સંપૂર્ણ નવી યાદી', '/new.pdf')]).replace(b'id="news"', b'id="different"')
        self.assertEqual(self.run_scan(html)[0]['status'], 'BASELINE')
        self.assertFalse(self.state['outbox'])

    def test_school_filter_excludes_teacher_exam(self):
        self.source['include_pattern'] = '(?i)NMMS|શિષ્યવૃત્તિ'
        self.source['exclude_pattern'] = '(?i)TET|TAT'
        items = [('NMMS શિષ્યવૃત્તિ', '/nmms.pdf'), ('TAT શિક્ષક પરીક્ષા', '/tat.pdf')]
        got = m.extract(self.source, page(items))
        self.assertEqual([i['title'] for i in got.values()], ['NMMS શિષ્યવૃત્તિ'])

    def test_unknown_source_date_blank_and_last_date_always_blank(self):
        item = {'title':'છેલ્લી તારીખ 30-10-2026', 'url':'https://school.example/n.pdf', 'pdf_url':'https://school.example/n.pdf'}
        event = m.render_news(item, self.source, 'NEW', self.now)
        self.assertEqual(list(event['fields']), list('ABCDEFGHIJK'))
        for key in ('D','G','I','K'): self.assertEqual(event['fields'][key], '')
        self.assertEqual(event['fields']['H'], 'Draft')
        self.assertNotIn('પ્રથમ નોંધાયેલ સમય', event['whatsapp'])
        self.assertNotIn('Draft', event['whatsapp'])

    def test_deferred_adhyapak_never_fetches(self):
        self.source['brand'] = 'adhyapak_saathi'
        with patch.object(m, 'fetch', side_effect=AssertionError('must not fetch')):
            self.assertEqual(m.scan([self.source], self.profiles, self.state, fetcher=m.fetch), [])

    def test_named_section_ignores_other_cards(self):
        self.source.update(section_selector='.card', section_heading_selector='.heading', section_heading='Notice Board', content_selector='.body')
        html = b'<div class="card"><div class="heading">Menu</div><div class="body"><a href="/menu">Menu item</a></div></div><div class="card"><div class="heading">Notice Board</div><div class="body"><a href="/new.pdf">School notice</a></div></div>'
        self.assertEqual(len(m.extract(self.source, html)), 1)

    def test_valid_empty_school_filter_is_not_parser_error(self):
        self.source['include_pattern'] = 'NMMS'
        self.assertEqual(self.run_scan(page([('Other examination', '/x.pdf')]))[0]['status'], 'BASELINE')

    def test_corrupt_state_is_not_reset(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'state.json'
            path.write_text('{"schema":999}')
            with self.assertRaises(ValueError): m.load_state(path)

    def test_relay_failure_keeps_pending_delivery(self):
        self.baseline()
        self.run_scan(page(self.items+[('નવી સૂચના', '/new.pdf')]))
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {'GYAN_RELAY_URL':'url', 'GYAN_RELAY_SECRET':'secret'}):
            def fail(*args): raise ValueError('quota')
            with self.assertRaises(ValueError): m.deliver(self.state, Path(folder)/'state.json', sender=fail)
        self.assertEqual(len(self.state['outbox']), 1)
        self.assertFalse(self.state['delivered'])

    def test_acknowledged_delivery_not_resent(self):
        self.baseline()
        self.run_scan(page(self.items+[('નવી સૂચના', '/new.pdf')]))
        calls = []
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {'GYAN_RELAY_URL':'url', 'GYAN_RELAY_SECRET':'secret'}):
            path = Path(folder)/'state.json'
            self.assertEqual(m.deliver(self.state, path, sender=lambda *args: calls.append(args)), 1)
            restored = m.load_state(path)
            self.assertEqual(m.deliver(restored, path, sender=lambda *args: calls.append(args)), 0)
        self.assertEqual(len(calls), 1)

    def test_notice_removal_and_reappearance_do_not_flood(self):
        self.items.append(('બીજી સૂચના', '/other.pdf'))
        self.baseline()
        self.run_scan(page(self.items[:1]))
        self.run_scan(page(self.items))
        self.assertFalse(self.state['outbox'])

    def test_relay_hmac_request(self):
        captured = []
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self,*args): return b'{"ok":true}'
        def opener(request,**kwargs): captured.append(request); return Response()
        event = dict(id='a'*64, brand='gyan_shiksha', subject='Title', body='Body')
        with patch.object(m, 'urlopen', opener), patch.object(m.time, 'time', return_value=1780000000):
            m.relay_send(event, 'https://script.google.com/macros/s/example/exec', 'secret')
        envelope = json.loads(captured[0].data)
        self.assertEqual(envelope['signature'], m.hmac.new(b'secret', ('1780000000\n'+envelope['payload']).encode(), m.hashlib.sha256).hexdigest())


if __name__ == '__main__': unittest.main()
