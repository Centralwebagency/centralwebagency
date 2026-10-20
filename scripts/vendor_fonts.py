"""Vendor the exact existing webfonts/CSS; keep license and source hashes.

Run deliberately with network access: python scripts/vendor_fonts.py
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'css/vendor'
GOOGLE = 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Outfit:wght@300;400;500;600&display=swap'
FA = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'


def download(url):
    with urlopen(Request(url, headers={'User-Agent': UA}), timeout=30) as response:
        return response.read()


def main():
    sources = []
    def save(path, url, data):
        target = DEST / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        sources.append({'file': target.relative_to(ROOT).as_posix(), 'source': url,
                        'sha256_download': hashlib.sha256(data).hexdigest()})

    for source, output in [(GOOGLE, 'google-fonts.css'), (FA, 'fontawesome.css')]:
        original = download(source)
        css = original.decode('utf-8')
        refs = sorted(set(re.findall(r'url\([\'"]?([^\)\'\"]+)', css)))
        urls = [urljoin(source, ref) for ref in refs]
        with ThreadPoolExecutor(max_workers=4) as pool:
            blobs = list(pool.map(download, urls))
        for ref, url, blob in zip(refs, urls, blobs):
            filename = ('google-' if source == GOOGLE else '') + Path(urlsplit(url).path).name
            save('fonts/' + filename, url, blob)
            css = css.replace(ref, 'fonts/' + filename)
        # CSS content and glyphs remain the same; only URLs are made local.
        save(output, source, css.encode('utf-8'))
        sources[-1]['sha256_original_css'] = hashlib.sha256(original).hexdigest()

    licenses = [
        ('OFL-cormorant-garamond.txt', 'https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/OFL.txt'),
        ('OFL-outfit.txt', 'https://raw.githubusercontent.com/google/fonts/main/ofl/outfit/OFL.txt'),
        ('LICENSE-fontawesome.txt', 'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.5.0/LICENSE.txt'),
    ]
    for filename, url in licenses:
        save(filename, url, download(url))
    (DEST / 'sources.json').write_text(json.dumps(sources, indent=2), encoding='utf-8')
    print(json.dumps({'files': len(sources), 'font_files': len(list((DEST / 'fonts').iterdir()))}))


if __name__ == '__main__':
    main()
