"""Check the owner's protected URLs, canonical signals and actual offer prices."""
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
from audit_site import ROOT,audit

def prices(value,path=''):
    rows=[]
    if isinstance(value,dict):
        for key,item in value.items():
            if key in ('price','minPrice','maxPrice','priceCurrency','unitCode','unitText'):
                rows.append((path+'/'+key,item))
            rows.extend(prices(item,path+'/'+key))
    elif isinstance(value,list):
        for i,item in enumerate(value):
            rows.extend(prices(item,path+'/'+str(i)))
    return rows

def main():
    before=json.loads((ROOT/'audit/finalisation-before.json').read_text(encoding='utf-8'))
    after=audit()
    original={p['file']:p for p in before['inventory']}
    current={p['file']:p for p in after['inventory']}
    checks={'same_38_content_pages':original.keys()==current.keys() and len(current)==38,
            'same_public_urls':all(p['url']==original[f]['url'] for f,p in current.items()),
            'same_canonicals':all(p['canonical']==original[f]['canonical'] for f,p in current.items()),
            'same_robots_meta':all(p['robots']==original[f]['robots'] for f,p in current.items()),
            'same_structured_offer_prices':all(prices(p['schemas'])==prices(original[f]['schemas']) for f,p in current.items()),
            'static_audit_clean':not after['issues']}
    for filename in ['robots.txt','sitemap.xml','_redirects']:
        original_bytes=subprocess.check_output(['git','show','c2564b4:'+filename],cwd=ROOT)
        local=(ROOT/filename).read_bytes()
        checks[filename+'_unchanged']=original_bytes.replace(b'\r\n',b'\n')==local.replace(b'\r\n',b'\n')
    modified=subprocess.check_output(['git','diff','--name-only','--','images','videos'],cwd=ROOT,text=True).splitlines()
    checks['existing_images_and_videos_unchanged']=not any(Path(p).suffix.lower() in ['.webp','.png','.jpg','.jpeg','.svg','.ico','.mp4'] for p in modified)
    summary={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'checks':checks}
    (ROOT/'audit/finalisation-invariants.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
    assert all(checks.values()), 'A protected invariant changed'

if __name__=='__main__':main()
