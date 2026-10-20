"""Local Chromium checks. Requires playwright; never submits the real contact form."""
import argparse
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
from threading import Thread
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(tempfile.gettempdir()) / 'cwa-audit-tools'))
from playwright.sync_api import sync_playwright
from audit_site import ROOT, audit


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path != '/' and not Path(path).suffix and (ROOT / (path.lstrip('/') + '.html')).is_file():
            self.path = path + '.html'
        try:
            super().do_GET()
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            pass  # The browser cancels media requests when leaving a page.

    def log_message(self, *args):
        pass


def run(baseline, selected=None, output=None):
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    results = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'mode': 'baseline' if baseline else 'after', 'pages': [], 'checks': {}}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome', headless=True)
        context = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
        # Stable layout tests without third-party network dependencies. No POST allowed.
        context.route('**/*', lambda route: route.continue_() if urlsplit(route.request.url).hostname == '127.0.0.1' and route.request.method == 'GET' else route.abort())
        page = context.new_page()
        errors = []
        asset_errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('response', lambda response: asset_errors.append({'url': response.url, 'status': response.status}) if response.url.startswith(origin) and response.status >= 400 else None)
        paths = ['/', '/contact', '/offres', '/fiches-metiers/coach-sportif', '/blog', '/sites-abonnement'] if baseline else [p['url'].replace('https://central-web-agency.com', '') for p in audit()['inventory']]
        if selected:
            paths = selected
        for path in paths:
            errors.clear()
            asset_errors.clear()
            response = page.goto(origin + path, wait_until='load')
            page.wait_for_timeout(50)
            result = {'path': path, 'status': response.status, 'js_errors': list(errors)}
            result['mobile_layout'] = page.evaluate('''() => ({width: innerWidth, scrollWidth: document.documentElement.scrollWidth, mainWidth: document.querySelector('main').getBoundingClientRect().width})''')
            if page.locator('.faq-question').count():
                clipped = []
                for button in page.locator('.faq-question').all():
                    button.press('Enter')
                    page.wait_for_timeout(50)
                    answer = button.locator('..').locator('.faq-answer')
                    dims = answer.evaluate('(el) => ({height: el.clientHeight, content: el.scrollHeight})')
                    if dims['content'] > dims['height'] + 2:
                        clipped.append({'question': button.inner_text(), **dims})
                result['clipped_faq'] = clipped
            result['menu_hidden_when_closed'] = page.locator('#mobileOverlay').evaluate('(el) => getComputedStyle(el).visibility === "hidden" || el.inert')
            page.locator('#navBurger').click(force=True)
            page.wait_for_timeout(50)
            result['menu_opens'] = page.locator('#navBurger').get_attribute('aria-expanded') == 'true'
            result['menu_focus_inside'] = page.locator('#mobileOverlay').evaluate('(el) => el.contains(document.activeElement)')
            if not result['menu_focus_inside'] and not baseline:
                result['focus_debug'] = page.evaluate("() => ({active: document.activeElement.outerHTML.slice(0, 250), inert: document.querySelector('#mobileOverlay').inert, visibility: getComputedStyle(document.querySelector('#mobileOverlay')).visibility, html: document.querySelector('#mobileOverlay').outerHTML.slice(0, 500)})")
            if page.locator('#mobileOverlayClose').count():
                page.locator('#mobileOverlayClose').dispatch_event('click')
                result['close_button_works'] = page.locator('#navBurger').get_attribute('aria-expanded') == 'false'
            page.keyboard.press('Escape')
            result['escape_closes'] = page.locator('#navBurger').get_attribute('aria-expanded') == 'false'
            page.set_viewport_size({'width': 1440, 'height': 1000})
            result['desktop_layout'] = page.evaluate('() => ({width: innerWidth, scrollWidth: document.documentElement.scrollWidth})')
            page.set_viewport_size({'width': 768, 'height': 1000})
            result['tablet_layout'] = page.evaluate('() => ({width: innerWidth, scrollWidth: document.documentElement.scrollWidth})')
            page.set_viewport_size({'width': 390, 'height': 844})
            result['asset_errors'] = list(asset_errors)
            results['pages'].append(result)

        page.goto(origin + '/contact', wait_until='load')
        page.locator('.contact-form').scroll_into_view_if_needed()
        results['checks']['empty_form_invalid'] = not page.locator('form').evaluate('(form) => form.checkValidity()')
        page.locator('#email').fill('adresse-invalide')
        results['checks']['invalid_email_rejected'] = not page.locator('#email').evaluate('(input) => input.checkValidity()')
        for selector, value in [('#name', 'Audit local'), ('#email', 'audit@example.com'), ('#activity', 'Test local'), ('#details', 'Vérification locale sans envoi'), ('#location', 'Heyrieux')]:
            page.locator(selector).fill(value)
        page.locator('#texts').select_option('non')
        results['checks']['completed_form_valid'] = page.locator('form').evaluate('(form) => form.checkValidity()')
        results['checks']['form_action'] = page.locator('form').get_attribute('action')
        # Intercept the submit event before any navigation or external request.
        page.locator('form').evaluate("form => form.addEventListener('submit', event => { event.preventDefault(); form.dataset.testSubmitted = 'yes'; })")
        page.locator('button[type=submit]').click()
        results['checks']['submit_event_reached'] = page.locator('form').get_attribute('data-test-submitted') == 'yes'

        # Keyboard focus must remain within the mobile menu and its toggle.
        page.locator('#navBurger').click()
        escaped_focus = []
        for _ in range(18):
            page.keyboard.press('Tab')
            if not page.evaluate("() => document.querySelector('#mobileOverlay').contains(document.activeElement) || document.activeElement.id === 'navBurger'"):
                escaped_focus.append(page.evaluate('() => document.activeElement.outerHTML.slice(0, 150)'))
        results['checks']['menu_focus_trapped'] = not escaped_focus
        page.keyboard.press('Escape')
        results['checks']['focus_restored'] = page.evaluate("() => document.activeElement.id === 'navBurger'")
        page.locator('#navBurger').click()
        page.set_viewport_size({'width': 1440, 'height': 1000})
        page.wait_for_timeout(100)
        results['checks']['resize_unlocks_scroll'] = page.evaluate("() => document.body.style.overflow !== 'hidden'")

        nojs = browser.new_context(java_script_enabled=False)
        nojs.route('**/*', lambda route: route.continue_() if urlsplit(route.request.url).hostname == '127.0.0.1' else route.abort())
        plain = nojs.new_page()
        plain.goto(origin + '/contact')
        results['checks']['nojs_form_opacity'] = plain.locator('.contact-form-wrapper').evaluate('(el) => getComputedStyle(el).opacity')
        plain.goto(origin + '/offres')
        results['checks']['nojs_faq_height'] = plain.locator('.faq-answer').first.evaluate('(el) => el.clientHeight')
        browser.close()
    server.shutdown()
    outfile = ROOT / output if output else ROOT / 'audit' / ('browser-before.json' if baseline else 'browser-after.json')
    outfile.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'pages_tested': len(results['pages']), 'checks': results['checks'],
                      'failures': [p for p in results['pages'] if p['js_errors'] or p.get('clipped_faq') or not p['menu_focus_inside'] or not p.get('close_button_works', True)]}, ensure_ascii=True, indent=2))
    if not baseline:
        assert all(p['status'] == 200 and not p['js_errors'] and not p['asset_errors'] and not p.get('clipped_faq') and p['menu_hidden_when_closed'] and p['menu_opens'] and p['menu_focus_inside'] and p.get('close_button_works', True) and p['escape_closes'] and all(p[k]['scrollWidth'] <= p[k]['width'] for k in ['mobile_layout','tablet_layout','desktop_layout']) for p in results['pages'])
        assert all(results['checks'][k] for k in ['empty_form_invalid', 'invalid_email_rejected', 'completed_form_valid', 'submit_event_reached', 'menu_focus_trapped', 'focus_restored', 'resize_unlocks_scroll'])
        assert results['checks']['nojs_form_opacity'] == '1' and results['checks']['nojs_faq_height'] > 0


def visual_checks(output=None):
    """Additional checks with animations and the real external font stylesheets."""
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    screenshots = Path(tempfile.gettempdir()) / 'cwa-audit-screenshots'
    screenshots.mkdir(exist_ok=True)
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome', headless=True)
        context = browser.new_context()
        # Only GETs; remote services can supply existing fonts, never receive a form.
        context.route('**/*', lambda route: route.continue_() if route.request.method == 'GET' else route.abort())
        page = context.new_page()
        for width in [320, 768, 1440]:
            page.set_viewport_size({'width': width, 'height': 900})
            for path in ['/', '/contact', '/offres', '/fiches-metiers/coach-sportif']:
                page.goto(origin + path, wait_until='networkidle')
                page.wait_for_timeout(1200)
                for target in page.locator('.reveal, .reveal-left, .reveal-right, .stagger').all():
                    if not target.is_visible():
                        continue  # Decorative blocks intentionally hidden at this breakpoint.
                    target.evaluate("el => el.scrollIntoView({block: 'center', behavior: 'instant'})")
                    page.wait_for_timeout(150)
                page.wait_for_timeout(1200)
                hidden = page.locator('.reveal, .reveal-left, .reveal-right, .stagger > *').evaluate_all("els => els.filter(el => el.getClientRects().length && getComputedStyle(el).opacity === '0').map(el => el.className)")
                clipped = []
                for button in page.locator('.faq-question').all():
                    button.press('Enter')
                    page.wait_for_timeout(450)
                    if button.locator('..').locator('.faq-answer').evaluate('(el) => el.scrollHeight > el.clientHeight + 2'):
                        clipped.append(button.inner_text())
                    button.press('Enter')
                if width <= 768:
                    page.locator('#navBurger').click()
                    page.wait_for_timeout(500)
                    focus_inside = page.locator('#mobileOverlay').evaluate('(el) => el.contains(document.activeElement)')
                    page.keyboard.press('Escape')
                else:
                    focus_inside = True
                page.evaluate('window.scrollTo(0, 0)')
                page.wait_for_timeout(600)
                shot = screenshots / f"{path.strip('/').replace('/', '-') or 'home'}-{width}.png"
                page.screenshot(path=str(shot), full_page=True)
                results.append({'path': path, 'width': width, 'hidden_content': hidden,
                                'clipped_faq': clipped, 'menu_focus_inside': focus_inside,
                                'screenshot': str(shot)})
        browser.close()
    server.shutdown()
    (ROOT / (output or 'audit/browser-visual.json')).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(results, ensure_ascii=True, indent=2))
    assert all(not r['hidden_content'] and not r['clipped_faq'] and r['menu_focus_inside'] for r in results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--paths', nargs='+')
    parser.add_argument('--visual', action='store_true')
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.visual:
        visual_checks(args.output)
    else:
        run(args.baseline, args.paths, args.output)
