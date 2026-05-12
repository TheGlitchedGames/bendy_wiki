/* ============================================================
   BENDY WIKI — bendy-main.js
   Lógica principal: menú móvil, utilidades, formularios globales
   ============================================================ */

"use strict";

/* ===================== MOBILE MENU ===================== */
class MobileMenu {
  constructor() {
    this.toggle  = document.getElementById("navToggle");
    this.menu    = document.getElementById("mobileMenu");
    this.isOpen  = false;
    if (this.toggle && this.menu) this.init();
  }

  init() {
    this.toggle.addEventListener("click", () => this.handleToggle());

    // Cerrar al hacer clic fuera
    document.addEventListener("click", (e) => {
      if (this.isOpen && !e.target.closest("#bendyNavbar")) this.close();
    });

    // Cerrar al cambiar a desktop
    window.addEventListener("resize", () => {
      if (window.innerWidth >= 992 && this.isOpen) this.close();
    });

    // Cerrar con Escape
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.isOpen) this.close();
    });
  }

  handleToggle() {
    this.isOpen ? this.close() : this.open();
  }

  open() {
    this.isOpen = true;
    this.menu.classList.add("open");
    this.toggle.classList.add("open");
    this.toggle.setAttribute("aria-expanded", "true");
  }

  close() {
    this.isOpen = false;
    this.menu.classList.remove("open");
    this.toggle.classList.remove("open");
    this.toggle.setAttribute("aria-expanded", "false");
  }
}

/* ===================== SMOOTH SCROLL ===================== */
class SmoothScroll {
  constructor() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener("click", (e) => {
        const target = document.querySelector(anchor.getAttribute("href"));
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }
}

/* ===================== ACTIVE NAV LINK ===================== */
class ActiveNavLink {
  constructor() {
    const path = window.location.pathname;
    document.querySelectorAll(".bendy-nav-link, .bendy-mobile-menu a").forEach(link => {
      if (link.getAttribute("href") === path) {
        link.classList.add("active");
        link.style.color = "var(--ink-gold)";
      }
    });
  }
}

/* ===================== AUTO-HIDE ALERTS ===================== */
class AutoHideAlerts {
  constructor() {
    document.querySelectorAll(".alert-dismissible").forEach(alert => {
      setTimeout(() => {
        alert.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        alert.style.opacity = "0";
        alert.style.transform = "translateX(20px)";
        setTimeout(() => alert.remove(), 500);
      }, 5000);
    });
  }
}

/* ===================== TOOLTIP SIMPLE ===================== */
class SimpleTooltips {
  constructor() {
    document.querySelectorAll("[title]").forEach(el => {
      const title = el.getAttribute("title");
      if (!title) return;

      el.removeAttribute("title");
      el.setAttribute("data-tip", title);

      el.addEventListener("mouseenter", (e) => this.show(e.target, title));
      el.addEventListener("mouseleave", () => this.hide());
    });
  }

  show(el, text) {
    const tip = document.createElement("div");
    tip.id = "bendy-tooltip";
    tip.textContent = text;
    tip.style.cssText = `
      position: fixed;
      background: var(--ink-black);
      color: var(--ink-cream);
      border: 1px solid var(--ink-gold-dim);
      border-radius: 4px;
      padding: 4px 10px;
      font-size: 0.74rem;
      font-family: var(--font-display);
      letter-spacing: 0.06em;
      pointer-events: none;
      z-index: 10000;
      white-space: nowrap;
      opacity: 0;
      transition: opacity 0.2s ease;
    `;

    document.body.appendChild(tip);

    const rect = el.getBoundingClientRect();
    tip.style.left = rect.left + rect.width / 2 - tip.offsetWidth / 2 + "px";
    tip.style.top  = rect.top - tip.offsetHeight - 8 + "px";

    requestAnimationFrame(() => { tip.style.opacity = "1"; });
  }

  hide() {
    const tip = document.getElementById("bendy-tooltip");
    if (tip) {
      tip.style.opacity = "0";
      setTimeout(() => tip.remove(), 200);
    }
  }
}

/* ===================== IMAGE LAZY LOADING ===================== */
class LazyImages {
  constructor() {
    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              const img = entry.target;
              if (img.dataset.src) {
                img.src = img.dataset.src;
                img.removeAttribute("data-src");
              }
              observer.unobserve(img);
            }
          });
        },
        { rootMargin: "100px" }
      );
      document.querySelectorAll("img[data-src]").forEach(img => observer.observe(img));
    }
  }
}

/* ===================== BACK TO TOP ===================== */
class BackToTop {
  constructor() {
    this.btn = this.createButton();
    this.init();
  }

  createButton() {
    const btn = document.createElement("button");
    btn.id = "backToTop";
    btn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    btn.setAttribute("aria-label", "Volver arriba");
    btn.style.cssText = `
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, var(--ink-gold-dim), var(--ink-gold));
      color: var(--ink-black);
      border: none;
      border-radius: 50%;
      cursor: pointer;
      font-size: 0.9rem;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
      z-index: 500;
      box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    `;
    document.body.appendChild(btn);
    return btn;
  }

  init() {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 500) {
        this.btn.style.opacity = "1";
        this.btn.style.transform = "translateY(0)";
      } else {
        this.btn.style.opacity = "0";
        this.btn.style.transform = "translateY(20px)";
      }
    }, { passive: true });

    this.btn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    this.btn.addEventListener("mouseenter", () => {
      this.btn.style.boxShadow = "0 6px 24px rgba(212,170,71,0.4)";
    });

    this.btn.addEventListener("mouseleave", () => {
      this.btn.style.boxShadow = "0 4px 16px rgba(0,0,0,0.4)";
    });
  }
}

/* ===================== CSRF FETCH HELPER ===================== */
window.bendyFetch = async (url, options = {}) => {
  const csrfEl = document.querySelector("[name=csrfmiddlewaretoken]");
  const csrf   = csrfEl ? csrfEl.value : "";

  const defaults = {
    headers: {
      "X-CSRFToken": csrf,
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  };

  const response = await fetch(url, defaults);
  return response;
};

/* ===================== INIT ===================== */
document.addEventListener("DOMContentLoaded", () => {
  new MobileMenu();
  new SmoothScroll();
  new ActiveNavLink();
  new AutoHideAlerts();
  new SimpleTooltips();
  new LazyImages();
  new BackToTop();

  // Animación de entrada de página
  document.body.style.opacity = "0";
  document.body.style.transition = "opacity 0.35s ease";
  requestAnimationFrame(() => {
    document.body.style.opacity = "1";
  });
});
