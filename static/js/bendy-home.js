/* ============================================================
   BENDY WIKI — bendy-home.js
   Animaciones específicas de la página de inicio
   ============================================================ */

"use strict";

/* ===================== HERO TITLE TYPEWRITER ===================== */
class HeroTypewriter {
  constructor(selector, options = {}) {
    this.el = document.querySelector(selector);
    this.delay = options.delay || 0;
    this.speed = options.speed || 80;
    if (this.el) this.init();
  }

  init() {
    const text = this.el.textContent.trim();
    this.el.textContent = "";
    this.el.style.overflow = "hidden";
    this.el.style.whiteSpace = "nowrap";
    this.el.style.display = "inline-block";

    setTimeout(() => this.type(text, 0), this.delay);
  }

  type(text, index) {
    if (index <= text.length) {
      this.el.textContent = text.slice(0, index);
      setTimeout(() => this.type(text, index + 1), this.speed);
    }
  }
}

/* ===================== GAME CARD INK HOVER ===================== */
class GameCardEffects {
  constructor() {
    this.cards = document.querySelectorAll(".game-card");
    this.init();
  }

  init() {
    this.cards.forEach(card => {
      card.addEventListener("mousemove", (e) => this.handleMouseMove(e, card));
      card.addEventListener("mouseleave", (e) => this.handleMouseLeave(card));
    });
  }

  handleMouseMove(e, card) {
    const rect = card.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;

    const glow = card.querySelector(".game-card-glow");
    if (glow) {
      glow.style.background = `radial-gradient(circle at ${x}% ${y}%, rgba(212,170,71,0.12) 0%, transparent 60%)`;
    }

    const rotX = ((e.clientY - rect.top) / rect.height - 0.5) * -6;
    const rotY = ((e.clientX - rect.left) / rect.width - 0.5) * 6;
    card.style.transform = `translateY(-4px) perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg)`;
  }

  handleMouseLeave(card) {
    card.style.transform = "";
    card.style.transition = "transform 0.5s ease";
    setTimeout(() => { card.style.transition = ""; }, 500);
  }
}

/* ===================== STAT COUNTER (HOME BRANDING) ===================== */
class HomeBrandingStats {
  constructor() {
    this.statNumbers = document.querySelectorAll(".auth-stat-number[data-target]");
    if (this.statNumbers.length) this.init();
  }

  init() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animate(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    this.statNumbers.forEach(el => observer.observe(el));
  }

  animate(el) {
    const target = parseInt(el.dataset.target, 10);
    const duration = 1200;
    const start = performance.now();

    const update = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target);
      if (progress < 1) requestAnimationFrame(update);
      else el.textContent = target;
    };

    requestAnimationFrame(update);
  }
}

/* ===================== HERO INK PARALLAX ===================== */
class HeroParallax {
  constructor() {
    this.hero = document.querySelector(".bendy-hero");
    this.bg = document.querySelector(".hero-ink-bg");
    this.content = document.querySelector(".hero-content");
    if (this.hero && this.bg) this.init();
  }

  init() {
    window.addEventListener("scroll", () => this.handleScroll(), { passive: true });
  }

  handleScroll() {
    const scroll = window.scrollY;
    if (scroll > window.innerHeight) return;

    const factor = scroll * 0.35;
    if (this.bg) {
      this.bg.style.transform = `translateY(${factor}px)`;
    }
    if (this.content) {
      this.content.style.transform = `translateY(${scroll * 0.15}px)`;
      this.content.style.opacity = `${1 - scroll / (window.innerHeight * 0.7)}`;
    }
  }
}

/* ===================== USER CARD HOVER INK ===================== */
class UserCardHover {
  constructor() {
    this.cards = document.querySelectorAll(".user-card");
    this.init();
  }

  init() {
    this.cards.forEach(card => {
      card.addEventListener("mouseenter", () => this.createRipple(card));
    });
  }

  createRipple(card) {
    const ripple = document.createElement("div");
    ripple.style.cssText = `
      position: absolute;
      inset: 0;
      border-radius: inherit;
      background: radial-gradient(circle at 50% 50%, rgba(212,170,71,0.08) 0%, transparent 70%);
      animation: ink-ripple 0.6s ease forwards;
      pointer-events: none;
      z-index: 0;
    `;
    card.style.position = "relative";
    card.appendChild(ripple);
    setTimeout(() => ripple.remove(), 700);
  }
}

/* ===================== JOIN CTA PULSE ===================== */
class JoinCtaPulse {
  constructor() {
    this.cta = document.querySelector(".join-cta");
    if (this.cta) this.init();
  }

  init() {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.cta.style.animation = "scale-in 0.6s ease both";
            observer.unobserve(this.cta);
          }
        });
      },
      { threshold: 0.4 }
    );
    observer.observe(this.cta);
  }
}

/* ===================== INIT ===================== */
document.addEventListener("DOMContentLoaded", () => {
  new GameCardEffects();
  new HomeBrandingStats();
  new HeroParallax();
  new UserCardHover();
  new JoinCtaPulse();
});
