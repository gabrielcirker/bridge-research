"""Integrity checks for the static research website (standard library only)."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.references.append(attrs[key])

class WebsiteChecks(unittest.TestCase):
    def test_local_links(self):
        for page in ROOT.rglob('*.html'):
            parsed = Links()
            parsed.feed(page.read_text())
            for reference in parsed.references:
                link = urlparse(reference)
                if link.scheme or link.netloc:
                    continue
                target = page.parent / unquote(link.path) if link.path else page
                if target.is_dir():
                    target /= 'index.html'
                with self.subTest(page=str(page.relative_to(ROOT)), reference=reference):
                    self.assertTrue(target.exists())
                    if not link.path and link.fragment:
                        self.assertIn(link.fragment, parsed.ids)

    def test_archive_hashes_and_references(self):
        manifest = json.loads((ROOT / 'archive/manifest.json').read_text())
        artifacts = {record['path']: record for record in manifest['files']}
        for path, record in artifacts.items():
            data = (ROOT / path).read_bytes()
            with self.subTest(path=path):
                self.assertEqual(len(data), record['bytes'])
                self.assertEqual(hashlib.sha256(data).hexdigest(), record['sha256'])
        for group in manifest['groups']:
            for record in group['files']:
                self.assertIn(record['path'], artifacts)
                self.assertEqual(record['sha256'], artifacts[record['path']]['sha256'])

    def test_presentation_omits_decorative_dates(self):
        text = (ROOT / 'index.html').read_text()
        self.assertIn('<p class="byline">Gabriel Cirker</p>', text)
        self.assertIn('<span>(original manuscript)</span>', text)
        self.assertIn('<span>(revision)</span>', text)
        self.assertNotIn('revised November 2026', text)
        self.assertNotIn('Original manuscript 2025', text)
        self.assertNotIn('Revised 2026', text)
        self.assertIn('Nishiyama &amp; Sato (2022)', text)
        self.assertIn('Sepahpour &amp; Chang (2007)', text)

    def test_report_pages(self):
        pages = json.loads((ROOT / 'assets/report/pages.json').read_text())
        self.assertEqual(len(pages), 4)
        for page in pages:
            self.assertTrue((ROOT / f'assets/report/page-{page["number"]}.webp').exists())
            self.assertGreater(len(page['text']), 100)

if __name__ == '__main__':
    unittest.main()
