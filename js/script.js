'use strict';

document.addEventListener('DOMContentLoaded', () => {

  /* ══════════════════════════════════════════════════════════════
     1. TITRE ANIMÉ LETTRE PAR LETTRE
     Conservé pour les pages qui utilisent encore #animated-title
  ══════════════════════════════════════════════════════════════ */
  (function initAnimatedTitle() {
    const title = document.getElementById('animated-title');
    if (!title) return;

    const text = title.textContent;
    title.textContent = '';

    Array.from(text).reverse().forEach((letter, index) => {
      const span = document.createElement('span');
      span.textContent = letter === ' ' ? '\u00A0' : letter;
      span.classList.add('letter');
      title.prepend(span);
      setTimeout(() => span.classList.add('visible'), index * 80);
    });
  })();


  /* ══════════════════════════════════════════════════════════════
     2. CUSTOM CURSOR (desktop uniquement)
  ══════════════════════════════════════════════════════════════ */
  (function initCursor() {
    const dot  = document.getElementById('cursorDot');
    const ring = document.getElementById('cursorRing');
    if (!dot || !ring) return;

    let mx = 0, my = 0, rx = 0, ry = 0;

    document.addEventListener('mousemove', e => {
      mx = e.clientX;
      my = e.clientY;
      dot.style.left = mx + 'px';
      dot.style.top  = my + 'px';
    });

    (function loop() {
      rx += (mx - rx) * 0.12;
      ry += (my - ry) * 0.12;
      ring.style.left = rx + 'px';
      ring.style.top  = ry + 'px';
      requestAnimationFrame(loop);
    })();

    document.querySelectorAll('a, button').forEach(el => {
      el.addEventListener('mouseenter', () => ring.classList.add('hover'));
      el.addEventListener('mouseleave', () => ring.classList.remove('hover'));
    });
  })();


  /* ══════════════════════════════════════════════════════════════
     3. NAVIGATION — Fond au scroll
  ══════════════════════════════════════════════════════════════ */
  (function initNavScroll() {
    const nav = document.getElementById('siteNav');
    if (!nav) return;
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 60);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  })();


  /* ══════════════════════════════════════════════════════════════
     4. MENU MOBILE
     Compatible nouveau markup (#navBurger / #mobileOverlay)
     ET ancien markup (#nav-toggle / #mobile-nav / #overlay)
  ══════════════════════════════════════════════════════════════ */
  (function initMobileMenu() {

    // Nouveau markup (index.html refactorisé)
    const burger        = document.getElementById('navBurger');
    const mobileOverlay = document.getElementById('mobileOverlay');

    if (burger && mobileOverlay) {
      function toggleNew(open) {
        burger.classList.toggle('open', open);
        mobileOverlay.classList.toggle('open', open);
        burger.setAttribute('aria-expanded', String(open));
        document.body.style.overflow = open ? 'hidden' : '';
      }

      burger.addEventListener('click', () => {
        toggleNew(!mobileOverlay.classList.contains('open'));
      });

      mobileOverlay.querySelectorAll('a').forEach(a =>
        a.addEventListener('click', () => toggleNew(false))
      );

      document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && mobileOverlay.classList.contains('open')) {
          toggleNew(false);
        }
      });
    }

    // Ancien markup (pages non encore refactorisées)
    const navToggle     = document.getElementById('nav-toggle');
    const mobileNav     = document.getElementById('mobile-nav');
    const legacyOverlay = document.getElementById('overlay');

    if (navToggle && mobileNav && legacyOverlay) {
      const openLegacy  = () => { mobileNav.classList.add('open'); legacyOverlay.classList.add('show'); document.body.style.overflow = 'hidden'; };
      const closeLegacy = () => { mobileNav.classList.remove('open'); legacyOverlay.classList.remove('show'); document.body.style.overflow = ''; };
      navToggle.addEventListener('click', () => mobileNav.classList.contains('open') ? closeLegacy() : openLegacy());
      legacyOverlay.addEventListener('click', closeLegacy);
    }
  })();


  /* ══════════════════════════════════════════════════════════════
     5. SCROLL REVEAL — IntersectionObserver
     Déclenche une seule fois, puis se désinscrit
  ══════════════════════════════════════════════════════════════ */
  (function initReveal() {
    const targets = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .stagger');
    if (!targets.length) return;

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

    targets.forEach(el => observer.observe(el));
  })();


  /* ══════════════════════════════════════════════════════════════
     6. FAQ ACCORDION
     Un seul item ouvert à la fois
  ══════════════════════════════════════════════════════════════ */
  (function initFAQ() {
    const questions = document.querySelectorAll('.faq-question');
    if (!questions.length) return;

    questions.forEach(btn => {
      btn.addEventListener('click', () => {
        const item   = btn.closest('.faq-item');
        const isOpen = item.classList.contains('open');

        document.querySelectorAll('.faq-item.open').forEach(openItem => {
          openItem.classList.remove('open');
          openItem.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
        });

        if (!isOpen) {
          item.classList.add('open');
          btn.setAttribute('aria-expanded', 'true');
        }
      });
    });
  })();

  // Note : les vidéos utilisent l'attribut `controls` natif du navigateur.
  // Pas d'autoplay — l'utilisateur clique pour lancer.

});


