"""Read-only static checks for CWA. Run: python scripts/audit_site.py [--output PATH]."""
import argparse
import hashlib
from collections import Counter, deque
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://central-web-agency.com'
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.stack = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attrs': dict(attrs), 'text': '',
                'parents': [n['tag'] for n in self.stack],
                'line': self.getpos()[0]}
        self.nodes.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        for n in self.stack:
            n['text'] += data


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def audit():
    files = sorted([*ROOT.glob('*.html'), *ROOT.glob('blog/*.html'),
                    *ROOT.glob('fiches-metiers/*.html')])
    pages = {}
    issues = []
    redirects = {}
    for line in (ROOT / '_redirects').read_text().splitlines():
        parts = line.split()
        if len(parts) >= 3 and not line.startswith('#'):
            redirects[parts[0]] = parts[1]
    sitemap = [e.text for e in ET.parse(ROOT / 'sitemap.xml').iter()
               if e.tag.endswith('}loc')]
    for file in files:
        if file.name.startswith('google'):
            continue  # Google ownership token, not a content page.
        rel = file.relative_to(ROOT).as_posix()
        path = '/' if rel == 'index.html' else '/' + rel.removesuffix('.html')
        nodes = Page(file.read_text(encoding='utf-8')).nodes
        pages[path] = (rel, nodes)

    def issue(file, kind, detail):
        issues.append({'file': file, 'kind': kind, 'detail': detail})

    inventory = []
    graph = {p: set() for p in pages}
    for path, (rel, nodes) in pages.items():
        url = ORIGIN + path
        bytag = lambda tag: [n for n in nodes if n['tag'] == tag]
        metas = {n['attrs'].get('name', n['attrs'].get('property')):
                 n['attrs'].get('content') for n in bytag('meta')}
        canonicals = [n['attrs'].get('href') for n in bytag('link')
                      if n['attrs'].get('rel') == 'canonical']
        headings = [(n['tag'], clean(n['text'])) for n in nodes
                    if re.fullmatch('h[1-6]', n['tag'])]
        titles = [clean(n['text']) for n in bytag('title')]
        ids = [n['attrs']['id'] for n in nodes if 'id' in n['attrs']]
        for id_, count in Counter(ids).items():
            if count > 1:
                issue(rel, 'duplicate_id', id_)
        if len(titles) != 1 or not titles[0]:
            issue(rel, 'title', titles)
        if not metas.get('description'):
            issue(rel, 'description', 'missing')
        if canonicals != [url]:
            issue(rel, 'canonical', canonicals)
        if sum(h[0] == 'h1' for h in headings) != 1:
            issue(rel, 'h1', headings)
        if len(bytag('main')) != 1:
            issue(rel, 'main', len(bytag('main')))
        if 'noindex' in (metas.get('robots') or '').lower():
            issue(rel, 'noindex', metas['robots'])
        if url not in sitemap:
            issue(rel, 'sitemap_missing', url)

        def check_ref(ref, kind):
            target = urlsplit(urljoin(url, ref))
            if target.scheme not in ('http', 'https') or target.netloc != urlsplit(ORIGIN).netloc:
                return
            dest = unquote(target.path)
            redirected = dest in redirects
            if redirected:
                issue(rel, 'redirected_' + kind, ref)
                dest = redirects[dest]
            if dest in pages:
                if kind == 'link':
                    graph[path].add(dest)
                if target.fragment:
                    dest_ids = {n['attrs'].get('id') for n in pages[dest][1]}
                    if unquote(target.fragment) not in dest_ids:
                        issue(rel, 'broken_fragment', ref)
            elif not (ROOT / dest.lstrip('/')).is_file():
                issue(rel, 'missing_' + kind, ref)

        for n in nodes:
            attrs = n['attrs']
            for name in ('aria-labelledby', 'aria-describedby', 'aria-controls'):
                for ref in (attrs.get(name) or '').split():
                    if ref not in ids:
                        issue(rel, 'missing_aria_target', ref)
            if n['tag'] == 'a' and attrs.get('href'):
                check_ref(attrs['href'], 'link')
            if n['tag'] in ('img', 'script', 'source', 'video', 'iframe'):
                for attr in ('src', 'poster'):
                    if attrs.get(attr):
                        check_ref(attrs[attr], 'asset')
            if n['tag'] == 'link' and attrs.get('rel') in ('stylesheet', 'icon', 'shortcut icon', 'apple-touch-icon', 'manifest', 'preload'):
                check_ref(attrs.get('href', ''), 'asset')
            if n['tag'] == 'img':
                if 'alt' not in attrs:
                    issue(rel, 'missing_alt', attrs.get('src'))
                if not attrs.get('width') or not attrs.get('height'):
                    issue(rel, 'image_dimensions', attrs.get('src'))

        schemas = []
        def schema_walk(value):
            if isinstance(value, dict):
                for k, v in value.items():
                    if k in ('url', '@id', 'logo', 'image', 'item') and isinstance(v, str) and v.startswith(ORIGIN):
                        # @id fragments identify entities, not HTML anchors.
                        check_ref(v.split('#')[0], 'schema_ref')
                    schema_walk(v)
            elif isinstance(value, list):
                for item in value:
                    schema_walk(item)

        for n in bytag('script'):
            if n['attrs'].get('type') == 'application/ld+json':
                try:
                    value = json.loads(n['text'])
                    schemas.append(value)
                    schema_walk(value)
                    if value.get('@type') == 'FAQPage':
                        questions = [clean(item['text']) for item in nodes if 'faq-question' in item['attrs'].get('class', '').split()]
                        answers = [clean(item['text']) for item in nodes if 'faq-answer' in item['attrs'].get('class', '').split()]
                        visible = list(zip(questions, answers))
                        structured = [(item.get('name'), item.get('acceptedAnswer', {}).get('text')) for item in value.get('mainEntity', [])]
                        if visible != structured:
                            issue(rel, 'faq_schema_mismatch', 'Questions/answers differ from visible FAQ')
                except json.JSONDecodeError as exc:
                    issue(rel, 'invalid_jsonld', str(exc))
        main = clean(' '.join(n['text'] for n in bytag('main')))
        inventory.append({'file': rel, 'url': url, 'title': titles[0] if titles else '',
                          'description': metas.get('description'), 'robots': metas.get('robots'),
                          'canonical': canonicals, 'headings': headings,
                          'words_main': len(main.split()), 'main_text': main,
                          'schemas': schemas,
                          'content_links': [{'href': n['attrs'].get('href'), 'text': clean(n['text'])}
                                            for n in bytag('a') if 'main' in n['parents']],
                          'images': [n['attrs'] for n in bytag('img')],
                          'forms': [n['attrs'] for n in bytag('form')]})
    for field in ('title', 'description'):
        values = Counter(p[field] for p in inventory)
        for val, count in values.items():
            if count > 1:
                issue('*', 'duplicate_' + field, val)
    for url in sitemap:
        if url.removeprefix(ORIGIN) not in pages:
            issue('sitemap.xml', 'unknown_sitemap_url', url)
    distances = {'/': 0}
    queue = deque(['/'])
    while queue:
        current = queue.popleft()
        for dest in graph[current]:
            if dest not in distances:
                distances[dest] = distances[current] + 1
                queue.append(dest)
    for p in inventory:
        path = p['url'].removeprefix(ORIGIN)
        p['depth_from_home'] = distances.get(path)
        p['incoming_pages'] = sum(path in dests for source, dests in graph.items() if source != path)
        if path not in distances:
            issue(p['file'], 'orphan', path)
    manifest = json.loads((ROOT / 'images/site.webmanifest').read_text())
    for icon in manifest['icons']:
        dest = urlsplit(urljoin(ORIGIN + '/images/site.webmanifest', icon['src'])).path
        if not (ROOT / dest.lstrip('/')).is_file():
            issue('images/site.webmanifest', 'missing_manifest_icon', icon['src'])
    # CSS font/image references must resolve too, including the self-hosted fonts.
    for stylesheet in (ROOT / 'css').rglob('*.css'):
        for ref in set(re.findall(r'url\([\'"]?([^\)\'\"]+)', stylesheet.read_text(encoding='utf-8'))):
            target = urlsplit(ref)
            if target.scheme or ref.startswith('//') or ref.startswith('#'):
                continue
            asset = ROOT / target.path.lstrip('/') if ref.startswith('/') else stylesheet.parent / unquote(target.path)
            if not asset.is_file():
                issue(stylesheet.relative_to(ROOT).as_posix(), 'missing_css_asset', ref)
    provenance = ROOT / 'css/vendor/sources.json'
    if provenance.is_file():
        for item in json.loads(provenance.read_text(encoding='utf-8')):
            asset = ROOT / item['file']
            if not asset.is_file() or hashlib.sha256(asset.read_bytes()).hexdigest() != item['sha256_download']:
                issue(item['file'], 'vendor_integrity', 'Downloaded asset differs from recorded hash')
    return {'pages_count': len(pages), 'sitemap_count': len(sitemap),
            'issues': issues, 'inventory': inventory}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true', help='Exit nonzero if a static check fails')
    args = parser.parse_args()
    result = audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'pages': result['pages_count'], 'sitemap': result['sitemap_count'],
                      'issues_by_kind': dict(Counter(i['kind'] for i in result['issues'])),
                      'issues': result['issues']}, ensure_ascii=False, indent=2))
    if args.check and result['issues']:
        sys.exit(1)
