"""GET-only HTTP audit; no form submission and no deployment."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from audit_site import ORIGIN, ROOT, Page, clean


class RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append({'url': req.full_url, 'status': code, 'location': newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url):
    redirects = RedirectRecorder()
    opener = urllib.request.build_opener(redirects)
    request = urllib.request.Request(url, headers={'User-Agent': 'CWA-ReadOnly-Audit/1.0'})
    try:
        try:
            response = opener.open(request, timeout=25)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            body = response.read()
            result = {'url': url, 'status': response.code, 'final_url': response.url,
                      'redirects': redirects.chain, 'headers': dict(response.headers),
                      'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
            if 'text/html' in response.headers.get('Content-Type', ''):
                text = body.decode('utf-8', errors='replace')
                nodes = Page(text).nodes
                result['title'] = [clean(n['text']) for n in nodes if n['tag'] == 'title']
                result['canonical'] = [n['attrs'].get('href') for n in nodes if n['tag'] == 'link' and n['attrs'].get('rel') == 'canonical']
                result['robots'] = [n['attrs'].get('content') for n in nodes if n['tag'] == 'meta' and n['attrs'].get('name') == 'robots']
                if url in content_urls and response.code == 200:
                    rel = 'index.html' if url == ORIGIN + '/' else url.removeprefix(ORIGIN + '/') + '.html'
                    result['same_as_local_normalized'] = text.replace('\r\n', '\n') == (ROOT / rel).read_text(encoding='utf-8')
                    result['html_extension_links'] = [n['attrs'].get('href') for n in nodes if n['tag'] == 'a' and '.html' in n['attrs'].get('href', '')]
            if url.endswith(('robots.txt', 'sitemap.xml')):
                result['body'] = body.decode('utf-8', errors='replace')
            return result
    except Exception as exc:
        return {'url': url, 'error': str(exc), 'redirects': redirects.chain}


if __name__ == '__main__':
    (ROOT / 'audit').mkdir(parents=True, exist_ok=True)
    content_urls = [e.text for e in ET.parse(ROOT / 'sitemap.xml').iter() if e.tag.endswith('}loc')]
    variants = [ORIGIN + line.split()[0] for line in (ROOT / '_redirects').read_text().splitlines() if line.strip() and not line.startswith('#')]
    extra = [ORIGIN + p for p in ['/robots.txt', '/sitemap.xml', '/audit-missing-page-20261019', '/index', '/blog/site-vitrine-restaurant-lyon', '/images/logo.png', '/web-app-manifest-192x192.png', '/web-app-manifest-512x512.png', '/services/', '/blog/site-vitrine-restaurant/']]
    extra += ['http://central-web-agency.com/', 'https://www.central-web-agency.com/', 'http://www.central-web-agency.com/']
    urls = list(dict.fromkeys(content_urls + variants + extra))
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, urls))
    (ROOT / 'audit/live-http.json').write_text(json.dumps({'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'results': results}, ensure_ascii=False, indent=2), encoding='utf-8')
    for r in results:
        print(json.dumps({k: v for k, v in r.items() if k in ('url', 'status', 'final_url', 'redirects', 'error', 'same_as_local_normalized')}, ensure_ascii=False))
