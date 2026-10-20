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
    if (window.matchMedia('(max-width: 768px), (pointer: coarse), (prefers-reduced-motion: reduce)').matches) return;

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
      const closeButton = document.getElementById('mobileOverlayClose');
      const desktop = window.matchMedia('(min-width: 769px)');
      let previousOverflow = '';
      mobileOverlay.inert = true;
      mobileOverlay.setAttribute('aria-hidden', 'true');

      function toggleNew(open, restoreFocus = true) {
        if (open === mobileOverlay.classList.contains('open')) return;
        if (open) previousOverflow = document.body.style.overflow;
        // Move focus out before hiding the dialog from assistive technology.
        if (!open && restoreFocus) burger.focus();
        if (!open && !restoreFocus && mobileOverlay.contains(document.activeElement)) {
          document.activeElement.blur();
        }
        burger.classList.toggle('open', open);
        mobileOverlay.classList.toggle('open', open);
        burger.setAttribute('aria-expanded', String(open));
        burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
        mobileOverlay.inert = !open;
        mobileOverlay.setAttribute('aria-hidden', String(!open));
        document.body.style.overflow = open ? 'hidden' : previousOverflow;
        if (open) {
          requestAnimationFrame(() => {
            if (mobileOverlay.classList.contains('open')) {
              (closeButton || mobileOverlay.querySelector('a')).focus();
            }
          });
        }
      }

      burger.addEventListener('click', () => {
        toggleNew(!mobileOverlay.classList.contains('open'));
      });

      mobileOverlay.querySelectorAll('a').forEach(a =>
        a.addEventListener('click', () => toggleNew(false))
      );
      if (closeButton) closeButton.addEventListener('click', () => toggleNew(false));

      document.addEventListener('keydown', e => {
        if (!mobileOverlay.classList.contains('open')) return;
        if (e.key === 'Escape') {
          e.preventDefault();
          toggleNew(false);
        }
        if (e.key === 'Tab') {
          const focusable = [burger, ...mobileOverlay.querySelectorAll('a[href], button:not([disabled])')];
          const current = focusable.indexOf(document.activeElement);
          const next = (current + (e.shiftKey ? -1 : 1) + focusable.length) % focusable.length;
          e.preventDefault();
          focusable[next].focus();
        }
      });
      desktop.addEventListener('change', e => {
        if (e.matches) toggleNew(false, false);
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
    // Content remains visible when scripting/animation support is unavailable.
    if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

    targets.forEach(el => {
      el.classList.add('reveal-pending');
      observer.observe(el);
    });
  })();


  /* ══════════════════════════════════════════════════════════════
     6. FAQ ACCORDION
     Un seul item ouvert à la fois
  ══════════════════════════════════════════════════════════════ */
  (function initFAQ() {
    const questions = document.querySelectorAll('.faq-question');
    if (!questions.length) return;
    document.documentElement.classList.add('faq-ready');

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
  
    /* ══════════════════════════════════════════════════════════════
     7. BOUTON RETOUR EN HAUT
     Apparaît après 500px de scroll
  ══════════════════════════════════════════════════════════════ */
(function initBackToTop() {
  const backToTop = document.createElement('button');

  backToTop.className = 'back-to-top';
  backToTop.type = 'button';
  backToTop.setAttribute('aria-label', 'Retour en haut de la page');
  backToTop.innerHTML = '<i class="fa-solid fa-arrow-up" aria-hidden="true"></i>';

  document.body.appendChild(backToTop);

  // Compatible avec le curseur personnalisé
  const cursorRing = document.getElementById('cursorRing');

  if (cursorRing) {
    backToTop.addEventListener('mouseenter', () => {
      cursorRing.classList.add('hover');
    });

    backToTop.addEventListener('mouseleave', () => {
      cursorRing.classList.remove('hover');
    });
  }

  // Affiche le bouton après 500px de scroll
  const onScroll = () => {
    backToTop.classList.toggle('is-visible', window.scrollY > 500);
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Retour fluide en haut de page
  backToTop.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
})();
  // Note : les vidéos utilisent l'attribut `controls` natif du navigateur.
  // Pas d'autoplay — l'utilisateur clique pour lancer.

});



