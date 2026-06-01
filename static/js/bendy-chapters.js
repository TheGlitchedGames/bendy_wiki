/* ============================================================
   BENDY WIKI — bendy-chapters.js
   Animaciones y lógica para páginas de capítulos (lista y detalle)
   ============================================================ */

"use strict";

/* ===================== FILTER MODAL (drawer lateral) ===================== */
class ChapterFilterModal {
  constructor() {
    this.modal    = document.getElementById("chapterFilterModal");
    this.backdrop = document.getElementById("chapterFilterBackdrop");
    this.openBtn  = document.getElementById("openChapterFilter");
    this.closeBtn = document.getElementById("closeChapterFilter");
    if (!this.modal) return;
    this._onKeydown = (e) => { if (e.key === "Escape") this.close(); };
    this.init();
  }

  init() {
    this.openBtn?.addEventListener("click",  () => this.open());
    this.closeBtn?.addEventListener("click", () => this.close());
    this.backdrop?.addEventListener("click", () => this.close());
    document.addEventListener("keydown", this._onKeydown);

    const params = new URLSearchParams(window.location.search);
    params.delete("page");
    if (params.toString()) this.openBtn?.classList.add("has-filters");
  }

  open() {
    this.modal?.classList.add("is-open");
    this.backdrop?.classList.add("is-open");
    document.body.style.overflow = "hidden";
    this.openBtn?.setAttribute("aria-expanded", "true");
    setTimeout(() => this.modal?.querySelector("input, select")?.focus(), 350);
  }

  close() {
    this.modal?.classList.remove("is-open");
    this.backdrop?.classList.remove("is-open");
    document.body.style.overflow = "";
    this.openBtn?.setAttribute("aria-expanded", "false");
    this.openBtn?.focus();
  }
}


/* ===================== BÚSQUEDA EN VIVO ===================== */
class ChapterLiveSearch {
  constructor() {
    this.input = document.getElementById("chapterQuickSearch");
    this.form  = document.getElementById("chapterQuickSearchForm");
    this.timer = null;
    this.DELAY = 350;
    if (this.input && this.form) this.init();
  }

  init() {
    this.input.addEventListener("input", () => {
      clearTimeout(this.timer);
      this.timer = setTimeout(() => this.form.submit(), this.DELAY);
    });
  }
}


/* ===================== FILTER COUNTER ===================== */
class ChapterFilterCounter {
  constructor() {
    this.form = document.getElementById("chapterFilterForm");
    if (!this.form) return;
    this.form.querySelectorAll("input, select").forEach(f =>
      f.addEventListener("change", () => this._update())
    );
  }

  _update() {
    let count = 0;
    this.form.querySelectorAll("select").forEach(s => { if (s.value) count++; });
    this.form.querySelectorAll("input[type=text]").forEach(i => { if (i.value.trim()) count++; });
    this.form.querySelectorAll("input[type=checkbox]:checked").forEach(() => count++);

    const badge = document.querySelector(".chapter-filter-badge");
    const btn   = document.getElementById("openChapterFilter");

    if (count > 0) {
      if (badge) {
        badge.textContent = count > 9 ? "9+" : String(count);
      } else if (btn) {
        const dot = document.createElement("span");
        dot.className   = "chapter-filter-badge";
        dot.textContent = String(count);
        btn.appendChild(dot);
      }
    } else {
      badge?.remove();
    }
  }
}


/* ===================== LAZY LOAD DE IMÁGENES ===================== */
class ChapterLazyImages {
  constructor() {
    const images = document.querySelectorAll("img[data-src]");
    if (!images.length) return;

    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(
        (entries) => entries.forEach(e => { if (e.isIntersecting) this._load(e.target, observer); }),
        { rootMargin: "120px" }
      );
      images.forEach(img => observer.observe(img));
    } else {
      images.forEach(img => this._load(img, null));
    }
  }

  _load(img, observer) {
    img.src = img.dataset.src;
    img.removeAttribute("data-src");
    img.classList.add("chapter-img-loaded");
    observer?.unobserve(img);
  }
}


/* ===================== GRID STAGGER ===================== */
class ChapterGridStagger {
  constructor() {
    this.cards = document.querySelectorAll(".chapter-card");
    if (!this.cards.length) return;
    this.init();
  }

  init() {
    this.cards.forEach((card, i) => {
      card.style.opacity   = "0";
      card.style.transform = "translateY(22px)";
      card.style.transition = `opacity 0.42s ease ${i * 0.06}s, transform 0.42s ease ${i * 0.06}s`;
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity   = "1";
            entry.target.style.transform = "translateY(0)";
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -20px 0px" }
    );

    this.cards.forEach(card => observer.observe(card));
  }
}


/* ===================== CARD GLOW DINÁMICO ===================== */
class ChapterCardGlow {
  constructor() {
    if (window.matchMedia("(hover: none)").matches) return;

    document.querySelectorAll(".chapter-card").forEach(card => {
      const glow = card.querySelector(".chapter-card-glow");
      if (!glow) return;

      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x    = ((e.clientX - rect.left) / rect.width)  * 100;
        const y    = ((e.clientY - rect.top)  / rect.height) * 100;
        glow.style.background = `radial-gradient(circle at ${x}% ${y}%, rgba(212,170,71,0.12) 0%, transparent 65%)`;
      });

      card.addEventListener("mouseleave", () => {
        glow.style.background = "";
      });
    });
  }
}


/* ===================== DETAIL — PARALLAX HERO ===================== */
class ChapterDetailParallax {
  constructor() {
    this.hero   = document.querySelector(".chapter-detail-hero");
    this.imgBg  = document.querySelector(".chapter-detail-hero-img");
    this.content = document.querySelector(".chapter-detail-hero-content");
    if (this.hero && this.imgBg) this.init();
  }

  init() {
    window.addEventListener("scroll", () => this.handleScroll(), { passive: true });
  }

  handleScroll() {
    const scroll = window.scrollY;
    if (scroll > window.innerHeight) return;
    this.imgBg.style.transform  = `translateY(${scroll * 0.28}px) scale(1.06)`;
    if (this.content) {
      this.content.style.opacity   = `${Math.max(0, 1 - scroll / 420)}`;
      this.content.style.transform = `translateY(${scroll * 0.1}px)`;
    }
  }
}


/* ===================== DETAIL — TABS DE CONTENIDO ===================== */
class ChapterDetailTabs {
  constructor() {
    this.tabBtns    = document.querySelectorAll(".chapter-tab-btn");
    this.tabPanels  = document.querySelectorAll(".chapter-tab-panel");
    if (!this.tabBtns.length) return;
    this.init();
  }

  init() {
    this.tabBtns.forEach(btn => {
      btn.addEventListener("click", () => this._activate(btn.dataset.tab));
    });
  }

  _activate(tabId) {
    this.tabBtns.forEach(b => b.classList.toggle("active", b.dataset.tab === tabId));
    this.tabPanels.forEach(p => {
      const isActive = p.dataset.tab === tabId;
      p.classList.toggle("active", isActive);
      if (isActive) {
        p.style.animation = "fade-in 0.35s ease both";
      }
    });
  }
}


/* ===================== DETAIL — REVEAL DE SECCIONES ===================== */
class ChapterSectionsReveal {
  constructor() {
    this.sections = document.querySelectorAll(".chapter-info-section");
    if (!this.sections.length) return;
    this.init();
  }

  init() {
    this.sections.forEach((section, i) => {
      section.style.opacity   = "0";
      section.style.transform = "translateY(18px)";
      section.style.transition = `opacity 0.5s ease ${i * 0.07}s, transform 0.5s ease ${i * 0.07}s`;
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity   = "1";
            entry.target.style.transform = "translateY(0)";
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );

    this.sections.forEach(s => observer.observe(s));
  }
}


/* ===================== DETAIL — NAVEGACIÓN PREV / NEXT ===================== */
class ChapterNavigation {
  constructor() {
    this.prevBtn = document.getElementById("prevChapterBtn");
    this.nextBtn = document.getElementById("nextChapterBtn");
    if (!this.prevBtn && !this.nextBtn) return;
    this._addKeyNav();
  }

  _addKeyNav() {
    document.addEventListener("keydown", (e) => {
      if (e.target.matches("input, textarea, select")) return;
      if (e.key === "ArrowLeft"  && this.prevBtn) this.prevBtn.click();
      if (e.key === "ArrowRight" && this.nextBtn) this.nextBtn.click();
    });
  }
}


/* ===================== DIFFICULTY BADGE TOOLTIP ===================== */
class DifficultyTooltip {
  constructor() {
    const labels = {
      introductory: "Introductorio — ideal para nuevos jugadores",
      easy:         "Fácil — pocos obstáculos",
      medium:       "Medio — dificultad estándar",
      hard:         "Difícil — requiere habilidad",
      boss_heavy:   "Con múltiples jefes — muy exigente",
    };

    document.querySelectorAll("[data-difficulty]").forEach(el => {
      const key   = el.dataset.difficulty;
      const label = labels[key];
      if (!label) return;

      el.style.cursor = "help";
      el.addEventListener("mouseenter", (e) => this._show(e.currentTarget, label));
      el.addEventListener("mouseleave", ()  => this._hide());
    });
  }

  _show(el, text) {
    const tip = document.createElement("div");
    tip.id = "diffTip";
    tip.textContent = text;
    tip.style.cssText = `
      position: fixed;
      background: var(--ink-black);
      color: var(--ink-cream);
      border: 1px solid var(--ink-gold-dim);
      border-radius: 4px;
      padding: 5px 12px;
      font-size: 0.73rem;
      font-family: var(--font-display);
      letter-spacing: 0.05em;
      pointer-events: none;
      z-index: 10000;
      white-space: nowrap;
      opacity: 0;
      transition: opacity 0.2s ease;
      box-shadow: 0 4px 16px rgba(0,0,0,0.5);
    `;
    document.body.appendChild(tip);

    const rect = el.getBoundingClientRect();
    tip.style.left = `${rect.left + rect.width / 2 - tip.offsetWidth / 2}px`;
    tip.style.top  = `${rect.top - tip.offsetHeight - 8}px`;
    requestAnimationFrame(() => { tip.style.opacity = "1"; });
  }

  _hide() {
    const tip = document.getElementById("diffTip");
    if (tip) {
      tip.style.opacity = "0";
      setTimeout(() => tip.remove(), 200);
    }
  }
}


/* ===================== INK SPLASH ON CLICK ===================== */
class ChapterInkClick {
  constructor() {
    document.addEventListener("click", (e) => {
      if (!e.target.closest(".chapter-card, .chapter-nav-btn")) return;
      this._splash(e.clientX, e.clientY);
    });
  }

  _splash(cx, cy) {
    const el = document.createElement("div");
    el.style.cssText = `
      position: fixed;
      left: ${cx - 18}px; top: ${cy - 18}px;
      width: 36px; height: 36px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(212,170,71,0.38) 0%, transparent 70%);
      pointer-events: none;
      z-index: 9999;
      animation: ink-splat 0.5s ease forwards;
    `;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 550);
  }
}


/* ===================== SIDEBAR STICKY ===================== */
class ChapterSidebarSticky {
  constructor() {
    const sidebar = document.querySelector(".chapter-sidebar-card");
    if (!sidebar) return;
    const navbar = document.getElementById("bendyNavbar");
    if (navbar) sidebar.style.top = `${navbar.offsetHeight + 20}px`;
  }
}


/* ===================== INIT ===================== */
document.addEventListener("DOMContentLoaded", () => {
  new ChapterFilterModal();
  new ChapterLiveSearch();
  new ChapterFilterCounter();
  new ChapterLazyImages();
  new ChapterGridStagger();
  new ChapterCardGlow();
  new ChapterDetailParallax();
  new ChapterDetailTabs();
  new ChapterSectionsReveal();
  new ChapterNavigation();
  new DifficultyTooltip();
  new ChapterInkClick();
  new ChapterSidebarSticky();
});