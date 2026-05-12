/* ============================================================
   BENDY WIKI — profile.js (auth_app)
   Animaciones y efectos para páginas de perfil
   ============================================================ */

"use strict";

/* ===================== STAT COUNTER PROFILE ===================== */
class ProfileStatCounter {
  constructor() {
    this.stats = document.querySelectorAll(".stat-card .stat-value");
    this.init();
  }

  init() {
    if (!this.stats.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.animateValue(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );

    this.stats.forEach(el => {
      const raw = el.textContent.trim();
      const num = parseInt(raw.replace(/\D/g, ""), 10);
      if (!isNaN(num) && num > 0) {
        el.dataset.finalValue = num;
        el.dataset.originalText = raw;
        observer.observe(el);
      }
    });
  }

  animateValue(el) {
    const target = parseInt(el.dataset.finalValue, 10);
    if (isNaN(target)) return;
    const duration = 1000;
    const start = performance.now();

    const update = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target).toLocaleString("es-ES");
      if (progress < 1) requestAnimationFrame(update);
      else el.textContent = el.dataset.originalText;
    };

    requestAnimationFrame(update);
  }
}

/* ===================== PROFILE HEADER PARALLAX ===================== */
class ProfileHeaderParallax {
  constructor() {
    this.header = document.getElementById("profileHeader");
    if (this.header) this.init();
  }

  init() {
    window.addEventListener("scroll", () => {
      const scroll = window.scrollY;
      const bg = this.header.querySelector(".profile-header-bg");
      if (bg && scroll < 400) {
        bg.style.transform = `translateY(${scroll * 0.2}px)`;
      }
    }, { passive: true });
  }
}

/* ===================== AVATAR HOVER EFFECT ===================== */
class AvatarHoverEffect {
  constructor() {
    this.wrapper = document.querySelector(".profile-avatar-wrapper");
    if (this.wrapper) this.init();
  }

  init() {
    this.wrapper.addEventListener("mouseenter", () => {
      const avatar = this.wrapper.querySelector(".profile-avatar, .profile-avatar-placeholder");
      if (avatar) {
        avatar.style.transform = "scale(1.05)";
        avatar.style.transition = "transform 0.3s ease, box-shadow 0.3s ease";
        avatar.style.boxShadow = "0 0 24px rgba(212,170,71,0.35)";
      }
    });

    this.wrapper.addEventListener("mouseleave", () => {
      const avatar = this.wrapper.querySelector(".profile-avatar, .profile-avatar-placeholder");
      if (avatar) {
        avatar.style.transform = "";
        avatar.style.boxShadow = "";
      }
    });
  }
}

/* ===================== STAT CARDS STAGGER ANIMATION ===================== */
class StatCardsStagger {
  constructor() {
    this.cards = document.querySelectorAll("#profileStats .stat-card");
    this.init();
  }

  init() {
    if (!this.cards.length) return;

    this.cards.forEach((card, i) => {
      card.style.opacity = "0";
      card.style.transform = "translateY(20px)";
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const cards = entry.target.querySelectorAll(".stat-card");
            cards.forEach((card, i) => {
              setTimeout(() => {
                card.style.transition = "opacity 0.5s ease, transform 0.5s ease";
                card.style.opacity = "1";
                card.style.transform = "translateY(0)";
              }, i * 100);
            });
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2 }
    );

    const grid = document.getElementById("profileStats");
    if (grid) observer.observe(grid);
  }
}

/* ===================== DANGER CONFIRM INPUT ===================== */
class DangerConfirmInput {
  constructor() {
    const form = document.getElementById("deleteAccountForm");
    if (!form) return;

    const input  = form.querySelector("input[name='confirm_username']");
    const btn    = form.querySelector("button[type='submit']");
    const target = btn ? btn.closest("form").querySelector("label strong")?.textContent : "";

    if (input && btn && target) {
      btn.disabled = true;
      btn.style.opacity = "0.5";

      input.addEventListener("input", () => {
        const match = input.value === target;
        btn.disabled = !match;
        btn.style.opacity = match ? "1" : "0.5";
        input.style.borderColor = input.value
          ? (match ? "var(--color-success)" : "var(--color-error)")
          : "";
      });
    }
  }
}

/* ===================== USER GRID FILTER ===================== */
class UserGridFilter {
  constructor() {
    this.grid  = document.getElementById("userGrid");
    this.cards = this.grid ? this.grid.querySelectorAll(".col-sm-6") : [];
    if (this.cards.length) this.buildFilter();
  }

  buildFilter() {
    const container = document.createElement("div");
    container.className = "d-flex gap-2 flex-wrap mb-4";
    container.innerHTML = `
      <span class="filter-label" style="font-family:var(--font-display);font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--ink-sepia);align-self:center;">Filtrar:</span>
      <button class="bendy-btn bendy-btn-outline-sm filter-btn active" data-role="all">Todos</button>
      <button class="bendy-btn bendy-btn-outline-sm filter-btn" data-role="admin">Admins</button>
      <button class="bendy-btn bendy-btn-outline-sm filter-btn" data-role="editor">Editores</button>
      <button class="bendy-btn bendy-btn-outline-sm filter-btn" data-role="reader">Lectores</button>
    `;

    this.grid.parentNode.insertBefore(container, this.grid);

    container.querySelectorAll(".filter-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        container.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        this.filter(btn.dataset.role);
      });
    });
  }

  filter(role) {
    this.cards.forEach((col, i) => {
      const card = col.querySelector(".user-card");
      const cardRole = card ? card.dataset.role : "";
      const show = role === "all" || cardRole === role;

      col.style.transition = `opacity 0.3s ease ${i * 0.03}s, transform 0.3s ease ${i * 0.03}s`;
      if (show) {
        col.style.opacity = "1";
        col.style.transform = "scale(1)";
        col.style.display = "";
      } else {
        col.style.opacity = "0";
        col.style.transform = "scale(0.95)";
        setTimeout(() => { if (col.style.opacity === "0") col.style.display = "none"; }, 350);
      }
    });
  }
}

/* ===================== INK POINTS TOOLTIP ===================== */
class InkPointsTooltip {
  constructor() {
    const pointsEl = document.querySelector(".profile-meta-item:first-child");
    if (pointsEl) {
      pointsEl.style.cursor = "help";
      pointsEl.addEventListener("mouseenter", () => {
        this.showHint(pointsEl, "Gana puntos contribuyendo artículos y comentarios");
      });
      pointsEl.addEventListener("mouseleave", () => this.hideHint());
    }
  }

  showHint(el, text) {
    const hint = document.createElement("div");
    hint.id = "inkHint";
    hint.textContent = text;
    hint.style.cssText = `
      position: fixed;
      background: var(--ink-black);
      color: var(--ink-cream);
      border: 1px solid var(--ink-gold-dim);
      border-radius: 4px;
      padding: 6px 12px;
      font-size: 0.74rem;
      font-family: var(--font-display);
      letter-spacing: 0.06em;
      pointer-events: none;
      z-index: 9999;
      white-space: nowrap;
      box-shadow: 0 4px 16px rgba(0,0,0,0.5);
      animation: fade-in 0.2s ease both;
    `;
    document.body.appendChild(hint);

    const rect = el.getBoundingClientRect();
    hint.style.left = rect.left + "px";
    hint.style.top  = (rect.bottom + 6) + "px";
  }

  hideHint() {
    const hint = document.getElementById("inkHint");
    if (hint) hint.remove();
  }
}

/* ===================== INIT ===================== */
document.addEventListener("DOMContentLoaded", () => {
  new ProfileStatCounter();
  new ProfileHeaderParallax();
  new AvatarHoverEffect();
  new StatCardsStagger();
  new DangerConfirmInput();
  new UserGridFilter();
  new InkPointsTooltip();
});
