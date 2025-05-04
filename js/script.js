document.addEventListener("DOMContentLoaded", () => {
  // ==========================
  // Animation du titre (si présent)
  // ==========================
  const title = document.getElementById("animated-title");

  if (title) {
    const text = title.textContent;
    title.textContent = "";

    const letters = Array.from(text).reverse();

    letters.forEach((letter, index) => {
      const span = document.createElement("span");
      span.textContent = letter === " " ? "\u00A0" : letter;
      span.classList.add("letter");
      title.prepend(span);

      setTimeout(() => {
        span.classList.add("visible");
      }, index * 80);
    });
  }

  // ==========================
  // Scroll reveal (toutes les pages)
  // ==========================
  const revealElements = document.querySelectorAll(".reveal");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      } else {
        entry.target.classList.remove("visible");
      }
    });
  }, {
    threshold: 0.1
  });

  revealElements.forEach(el => observer.observe(el));

  // ==========================
  // Menu de navigation
  // ==========================
  const navToggle = document.getElementById("nav-toggle");
  const mobileNav = document.getElementById("mobile-nav");
  const overlay = document.getElementById("overlay");

  if (navToggle && mobileNav && overlay) {
    function openMenu() {
      mobileNav.classList.add("open");
      overlay.classList.add("show");
      document.body.style.overflow = "hidden";
    }

    function closeMenu() {
      mobileNav.classList.remove("open");
      overlay.classList.remove("show");
      document.body.style.overflow = "";
    }

    navToggle.addEventListener("click", () => {
      if (mobileNav.classList.contains("open")) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    overlay.addEventListener("click", closeMenu);
  }
});




