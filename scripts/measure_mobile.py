"""Comparable local Lighthouse runs plus font/style equivalence, no deployment.

Uses the immutable pre-finalisation snapshot in the OS temporary directory.
"""
import argparse
from functools import partial
import gzip
from http.server import ThreadingHTTPServer
from io import BytesIO
import json
from pathlib import Path
import subprocess
import tempfile
from threading import Thread
from urllib.parse import unquote,urlsplit
from browser_audit import Handler,ROOT,sync_playwright

SNAPSHOT=Path(tempfile.gettempdir())/'cwa-finalisation-baseline-20261020'


class CompareHandler(Handler):
    def translate_path(self,path):
        path=unquote(urlsplit(path).path)
        if path.startswith('/before/'):
            rel=path.removeprefix('/before/') or 'index.html'
            if not Path(rel).suffix:
                rel+='.html'
            for base in [SNAPSHOT,ROOT]:
                resolved=(base/rel).resolve()
                if resolved.is_relative_to(base.resolve()) and resolved.is_file():
                    return str(resolved)
        return super().translate_path(path)

    def send_head(self):
        file=Path(self.translate_path(self.path))
        if file.is_dir():
            file=file/'index.html'
        if file.is_file() and file.suffix in ['.html','.css','.js','.json'] and 'gzip' in self.headers.get('Accept-Encoding',''):
            data=gzip.compress(file.read_bytes(),compresslevel=6)
            self.send_response(200)
            self.send_header('Content-Type',self.guess_type(str(file)))
            self.send_header('Content-Encoding','gzip')
            self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control','no-store')
            self.end_headers()
            return BytesIO(data)
        return super().send_head()


def main(skip_lighthouse=False):
    assert (SNAPSHOT/'index.html').is_file(), 'Pre-change snapshot required'
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(CompareHandler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    origin=f'http://127.0.0.1:{server.server_port}'
    results={'scope':'Local gzip server, same Chrome/Lighthouse mobile simulation; not production CWV','runs':[],'visual_equivalence':[]}
    with sync_playwright() as pw:
        browser=pw.chromium.launch(channel='chrome',headless=True)
        context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
        page=context.new_page()
        for phase,url in [('before',origin+'/before/'),('after',origin+'/')]:
            page.goto(url,wait_until='networkidle')
            values=page.evaluate('''async () => {
                const samples=['300 60px "Cormorant Garamond"','italic 300 60px "Cormorant Garamond"','400 16px Outfit','600 16px Outfit','900 24px "Font Awesome 6 Free"','400 24px "Font Awesome 6 Brands"'];
                await Promise.all(samples.map(font=>document.fonts.load(font,'Élégance Lyon 2026')));
                await document.fonts.ready;
                const canvas=document.createElement('canvas'), ctx=canvas.getContext('2d');
                const widths=samples.map(font=>{ctx.font=font; return {font,width:ctx.measureText('Élégance Lyon 2026').width,ready:document.fonts.check(font)};});
                const selectors=['.hero-title','.hero-sub','.btn-primary','.feature-card h3, .feature-card h4','.footer-col h2, .footer-col h4'];
                const styles=selectors.map(selector=>{const el=document.querySelector(selector),s=getComputedStyle(el);return {selector,fontFamily:s.fontFamily,fontSize:s.fontSize,fontWeight:s.fontWeight,lineHeight:s.lineHeight,color:s.color,marginTop:s.marginTop,marginBottom:s.marginBottom};});
                const faces=[...document.fonts].filter(font=>font.status==='loaded').map(font=>({family:font.family,weight:font.weight,style:font.style}));
                return {widths,styles,faces};
            }''')
            results['visual_equivalence'].append({'phase':phase,**values})
        browser.close()
    before,after=results['visual_equivalence']
    assert before['widths']==after['widths'], 'Webfont metrics changed'
    assert before['styles']==after['styles'], 'Computed typography/colors/margins changed'
    if not skip_lighthouse:
        npx=__import__('shutil').which('npx.cmd')
        for iteration in range(2):
            for phase,url in [('before',origin+'/before/'),('after',origin+'/')]:
                output=ROOT/f'audit/mobile-{phase}-{iteration+1}.json'
                command=[npx,'--yes','--cache',str(Path(tempfile.gettempdir())/'cwa-npm-cache'),'lighthouse@12.8.2',url,'--chrome-flags=--headless=new','--only-categories=performance,accessibility,best-practices,seo','--output=json','--output-path='+str(output),'--quiet']
                subprocess.run(command,check=True,timeout=180)
                report=json.loads(output.read_text(encoding='utf-8'))
                results['runs'].append({'phase':phase,'iteration':iteration+1,'scores':{k:v['score'] for k,v in report['categories'].items()},'metrics':{k:report['audits'][k].get('numericValue') for k in ['largest-contentful-paint','first-contentful-paint','total-blocking-time','cumulative-layout-shift','total-byte-weight']}})
                print(json.dumps(results['runs'][-1]),flush=True)
    server.shutdown()
    (ROOT/'audit/mobile-comparison-2026-10-20.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Font metrics, computed typography, colors and heading margins match.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--skip-lighthouse',action='store_true')
    main(parser.parse_args().skip_lighthouse)
