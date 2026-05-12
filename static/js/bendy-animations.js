/* ============================================================
   BENDY WIKI — bendy-animations.js
   Sistema de animaciones: partículas de tinta, goteos, efectos
   ============================================================ */

"use strict";

/* ===================== INK PARTICLES ===================== */
class InkParticleSystem {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.particles = [];
    this.maxParticles = 18;
    this.running = false;
    if (this.container) this.init();
  }

  init() {
    this.running = true;
    this.spawnLoop();
  }

  createParticle() {
    const el = document.createElement("div");
    el.className = "ink-particle";
    const size = Math.random() * 60 + 20;
    const x = Math.random() * 100;
    const duration = Math.random() * 12 + 10;
    const delay = Math.random() * 8;
    const opacity = Math.random() * 0.12 + 0.03;

    el.style.cssText = `
      width: ${size}px;
      height: ${size}px;
      left: ${x}%;
      top: -${size}px;
      opacity: ${opacity};
      animation-duration: ${duration}s;
      animation-delay: ${delay}s;
    `;

    this.container.appendChild(el);
    this.particles.push(el);

    setTimeout(() => {
      el.remove();
      this.particles = this.particles.filter(p => p !== el);
    }, (duration + delay) * 1000);
  }

  spawnLoop() {
    if (!this.running) return;
    if (this.particles.length < this.maxParticles) {
      this.createParticle();
    }
    const interval = Math.random() * 1800 + 600;
    setTimeout(() => this.spawnLoop(), interval);
  }

  stop() {
    this.running = false;
  }
}

/* ===================== INK DRIP GENERATOR ===================== */
class InkDripGenerator {
  constructor(containerId, count = 12) {
    this.container = document.getElementById(containerId);
    this.count = count;
    if (this.container) this.generate();
  }

  generate() {
    this.container.innerHTML = "";
    for (let i = 0; i < this.count; i++) {
      const drip = document.createElement("div");
      drip.className = "ink-drip-element";
      const x = (i / (this.count - 1)) * 100;
      const height = Math.random() * 28 + 8;
      const width = Math.random() * 4 + 2;
      const duration = Math.random() * 2 + 1.5;
      const delay = Math.random() * 4;

      drip.style.cssText = `
        position: absolute;
        left: ${x}%;
        top: 0;
        width: ${width}px;
        height: ${height}px;
        background: linear-gradient(180deg, var(--ink-gold-dim), transparent);
        border-radius: 0 0 ${width}px ${width}px;
        transform-origin: top;
        animation: ink-drip ${duration}s ease-in-out ${delay}s infinite;
        opacity: 0.6;
      `;

      this.container.appendChild(drip);
    }
  }
}

/* ===================== HERO INK DRIPS ===================== */
class HeroInkDrips {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (this.container) this.generate();
  }

  generate() {
    const count = 20;
    for (let i = 0; i < count; i++) {
      const drip = document.createElement("div");
      drip.className = "hero-ink-drip";
      const x = (i / count) * 100 + (Math.random() * 3);
      const height = Math.random() * 40 + 10;
      const duration = Math.random() * 3 + 2;
      const delay = Math.random() * 6;

      drip.style.cssText = `
        left: ${x}%;
        height: ${height}px;
        width: ${Math.random() * 3 + 1}px;
        animation-duration: ${duration}s;
        animation-delay: ${delay}s;
        opacity: ${Math.random() * 0.5 + 0.1};
      `;

      this.container.appendChild(drip);
    }
  }
}

/* ===================== COUNTER ANIMATION ===================== */
class CounterAnimation {
  constructor(selector) {
    this.elements = document.querySelectorAll(selector);
    this.observer = null;
    this.init();
  }

  init() {
    if (!this.elements.length) return;
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.animateCounter(entry.target);
            this.observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );
    this.elements.forEach(el => this.observer.observe(el));
  }

  animateCounter(el) {
    const target = parseInt(el.dataset.target || el.textContent, 10);
    if (isNaN(target)) return;
    const duration = 1400;
    const step = 16;
    const steps = duration / step;
    const increment = target / steps;
    let current = 0;

    const update = () => {
      current = Math.min(current + increment, target);
      el.textContent = Math.floor(current).toLocaleString("es-ES");
      if (current < target) requestAnimationFrame(update);
      else el.textContent = target.toLocaleString("es-ES");
    };

    requestAnimationFrame(update);
  }
}

/* ===================== SCROLL REVEAL ===================== */
class ScrollReveal {
  constructor() {
    this.elements = document.querySelectorAll(
      ".game-card, .stat-card, .community-block, .user-card, .bendy-panel, .profile-info-card"
    );
    this.init();
  }

  init() {
    if (!this.elements.length) return;

    this.elements.forEach((el, i) => {
      el.style.opacity = "0";
      el.style.transform = "translateY(24px)";
      el.style.transition = `opacity 0.55s ease ${i * 0.07}s, transform 0.55s ease ${i * 0.07}s`;
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
    );

    this.elements.forEach(el => observer.observe(el));
  }
}

/* ===================== NAVBAR SCROLL EFFECT ===================== */
class NavbarScroll {
  constructor() {
    this.navbar = document.getElementById("bendyNavbar");
    this.lastScroll = 0;
    if (this.navbar) this.init();
  }

  init() {
    window.addEventListener("scroll", () => this.handleScroll(), { passive: true });
  }

  handleScroll() {
    const currentScroll = window.scrollY;
    if (currentScroll > 60) {
      this.navbar.classList.add("scrolled");
    } else {
      this.navbar.classList.remove("scrolled");
    }
    this.lastScroll = currentScroll;
  }
}

/* ===================== INK SPLASH ON CLICK ===================== */
class InkClickEffect {
  constructor() {
    document.addEventListener("click", (e) => this.createSplash(e));
  }

  createSplash(e) {
    const target = e.target;
    if (!target.closest(".bendy-btn, .bendy-nav-link, .user-card, .game-card")) return;

    const splash = document.createElement("div");
    splash.style.cssText = `
      position: fixed;
      left: ${e.clientX - 20}px;
      top: ${e.clientY - 20}px;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(212,170,71,0.4) 0%, transparent 70%);
      pointer-events: none;
      z-index: 9999;
      animation: ink-splat 0.5s ease forwards;
    `;
    document.body.appendChild(splash);
    setTimeout(() => splash.remove(), 600);
  }
}

/* ===================== LOGO FLICKER ===================== */
class LogoFlicker {
  constructor() {
    this.logo = document.querySelector(".bendy-logo");
    if (this.logo) this.scheduleFlicker();
  }

  scheduleFlicker() {
    const delay = Math.random() * 12000 + 8000;
    setTimeout(() => {
      this.logo.style.animation = "flicker 0.4s ease";
      setTimeout(() => {
        this.logo.style.animation = "";
        this.scheduleFlicker();
      }, 500);
    }, delay);
  }
}

/* ===================== INIT ===================== */
document.addEventListener("DOMContentLoaded", () => {
  new InkParticleSystem("inkParticles");
  new InkDripGenerator("inkDrips", 14);
  new HeroInkDrips("heroInkDrips");
  new CounterAnimation("[data-target]");
  new ScrollReveal();
  new NavbarScroll();
  new InkClickEffect();
  new LogoFlicker();
});
