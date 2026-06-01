/* ============================================================
   BENDY WIKI — bendy-games.js
   Animaciones y lógica para páginas de juegos (lista y detalle)
   ============================================================ */

"use strict";

/* ===================== BÚSQUEDA EN VIVO ===================== */
class GameLiveSearch {
  constructor() {
    this.input = document.getElementById("quickSearch");
    this.form  = document.getElementById("quickSearchForm");
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


/* ===================== GRID STAGGER ANIMATION ===================== */
class GameGridStagger {
  constructor() {
    this.cards = document.querySelectorAll(".game-entry-card");
    if (!this.cards.length) return;
    this.init();
  }

  init() {
    this.cards.forEach((card, i) => {
      card.style.opacity   = "0";
      card.style.transform = "translateY(28px)";
      card.style.transition = `opacity 0.45s ease ${i * 0.08}s, transform 0.45s ease ${i * 0.08}s`;
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


/* ===================== CARD TILT (detalle 3D) ===================== */
class GameCardTilt {
  constructor() {
    if (window.matchMedia("(hover: none)").matches) return;

    document.querySelectorAll(".game-entry-card").forEach(card => {
      card.addEventListener("mousemove",  (e) => this._tilt(e, card));
      card.addEventListener("mouseleave", ()  => this._reset(card));
    });
  }

  _tilt(e, card) {
    const rect = card.getBoundingClientRect();
    const x    = (e.clientX - rect.left) / rect.width  - 0.5;
    const y    = (e.clientY - rect.top)  / rect.height - 0.5;
    card.style.transform  = `translateY(-6px) perspective(800px) rotateX(${-y * 6}deg) rotateY(${x * 6}deg)`;
    card.style.transition = "transform 0.1s linear";
  }

  _reset(card) {
    card.style.transform  = "";
    card.style.transition = "transform 0.45s ease";
  }
}


/* ===================== GLOW DINÁMICO AL HOVER ===================== */
class GameCardGlow {
  constructor() {
    document.querySelectorAll(".game-entry-card").forEach(card => {
      const glow = card.querySelector(".game-entry-card-glow");
      if (!glow) return;

      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x    = ((e.clientX - rect.left) / rect.width)  * 100;
        const y    = ((e.clientY - rect.top)  / rect.height) * 100;
        glow.style.background = `radial-gradient(circle at ${x}% ${y}%, rgba(212,170,71,0.13) 0%, transparent 65%)`;
      });

      card.addEventListener("mouseleave", () => {
        glow.style.background = "";
      });
    });
  }
}


/* ===================== HERO PARALLAX (detalle) ===================== */
class GameDetailParallax {
  constructor() {
    this.hero   = document.querySelector(".game-detail-hero");
    this.imgBg  = document.querySelector(".game-detail-hero-img-bg");
    this.content = document.querySelector(".game-detail-hero-content");
    if (this.hero && this.imgBg) this.init();
  }

  init() {
    window.addEventListener("scroll", () => this.handleScroll(), { passive: true });
  }

  handleScroll() {
    const scroll = window.scrollY;
    if (scroll > window.innerHeight) return;
    this.imgBg.style.transform = `translateY(${scroll * 0.3}px) scale(1.05)`;
    if (this.content) {
      this.content.style.opacity   = `${Math.max(0, 1 - scroll / 400)}`;
      this.content.style.transform = `translateY(${scroll * 0.12}px)`;
    }
  }
}


/* ===================== CHAPTER ROWS — REVEAL ===================== */
class ChapterRowsReveal {
  constructor() {
    this.rows = document.querySelectorAll(".game-chapter-row");
    if (!this.rows.length) return;
    this.init();
  }

  init() {
    this.rows.forEach((row, i) => {
      row.style.opacity   = "0";
      row.style.transform = "translateX(-14px)";
      row.style.transition = `opacity 0.4s ease ${i * 0.06}s, transform 0.4s ease ${i * 0.06}s`;
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity   = "1";
            entry.target.style.transform = "translateX(0)";
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );

    this.rows.forEach(row => observer.observe(row));
  }
}


/* ===================== CHARACTERS GRID — REVEAL ===================== */
class GameCharGridReveal {
  constructor() {
    this.cards = document.querySelectorAll(".game-char-card");
    if (!this.cards.length) return;
    this.init();
  }

  init() {
    this.cards.forEach((card, i) => {
      card.style.opacity   = "0";
      card.style.transform = "scale(0.88)";
      card.style.transition = `opacity 0.4s ease ${i * 0.05}s, transform 0.4s ease ${i * 0.05}s`;
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity   = "1";
            entry.target.style.transform = "scale(1)";
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );

    this.cards.forEach(card => observer.observe(card));
  }
}


/* ===================== INK SPLASH ON CLICK ===================== */
class GameInkClick {
  constructor() {
    document.addEventListener("click", (e) => {
      if (!e.target.closest(".game-entry-card, .game-chapter-row, .game-char-card")) return;
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


/* ===================== SIDEBAR STICKY OFFSET ===================== */
class GameSidebarSticky {
  constructor() {
    const sidebar = document.querySelector(".game-sidebar-card");
    if (!sidebar) return;
    // El offset lo maneja CSS (position: sticky + top), pero
    // ajustamos dinámicamente si hay navbar fija.
    const navbar = document.getElementById("bendyNavbar");
    if (navbar) {
      const h = navbar.offsetHeight;
      sidebar.style.top = `${h + 20}px`;
    }
  }
}


/* ===================== INIT ===================== */
document.addEventListener("DOMContentLoaded", () => {
  new GameLiveSearch();
  new GameGridStagger();
  new GameCardTilt();
  new GameCardGlow();
  new GameDetailParallax();
  new ChapterRowsReveal();
  new GameCharGridReveal();
  new GameInkClick();
  new GameSidebarSticky();
});