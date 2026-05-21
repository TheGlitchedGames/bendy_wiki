/* ============================================================
   BENDY WIKI — bendy-characters.js
   Modal de filtros, búsqueda en vivo, lazy load de imágenes
   ============================================================ */

"use strict";

/* ─────────────────────────────────────────────────────────────
   FILTER MODAL (drawer lateral)
───────────────────────────────────────────────────────────── */
class FilterModal {
  constructor() {
    this.modal    = document.getElementById("filterModal");
    this.backdrop = document.getElementById("filterModalBackdrop");
    this.openBtn  = document.getElementById("openFilterModal");
    this.closeBtn = document.getElementById("closeFilterModal");

    if (!this.modal) return;

    this._onKeydown = (e) => { if (e.key === "Escape") this.close(); };
    this.init();
  }

  init() {
    this.openBtn?.addEventListener("click",  () => this.open());
    this.closeBtn?.addEventListener("click", () => this.close());
    this.backdrop?.addEventListener("click", () => this.close());

    // Cerrar con Escape
    document.addEventListener("keydown", this._onKeydown);

    // Activar si hay filtros activos (abre con clase ya puesta)
    const params = new URLSearchParams(window.location.search);
    params.delete("page");
    if (params.toString() && document.querySelector(".char-filter-badge")) {
      // No abrir automáticamente, sólo resaltar el botón
      this.openBtn?.classList.add("has-filters");
    }
  }

  open() {
    this.modal?.classList.add("is-open");
    this.backdrop?.classList.add("is-open");
    document.body.style.overflow = "hidden";

    // Focus al primer campo
    setTimeout(() => {
      this.modal?.querySelector("input, select")?.focus();
    }, 350);

    this.openBtn?.setAttribute("aria-expanded", "true");
  }

  close() {
    this.modal?.classList.remove("is-open");
    this.backdrop?.classList.remove("is-open");
    document.body.style.overflow = "";
    this.openBtn?.setAttribute("aria-expanded", "false");
    this.openBtn?.focus();
  }

  destroy() {
    document.removeEventListener("keydown", this._onKeydown);
  }
}


/* ─────────────────────────────────────────────────────────────
   BÚSQUEDA EN VIVO (debounced)
   Envía el form de búsqueda rápida tras 350 ms de inactividad
───────────────────────────────────────────────────────────── */
class LiveSearch {
  constructor() {
    this.input = document.getElementById("quickSearch");
    this.form  = document.getElementById("quickSearchForm");
    this.timer = null;
    this.DELAY = 350; // ms

    if (this.input && this.form) this.init();
  }

  init() {
    this.input.addEventListener("input", () => {
      clearTimeout(this.timer);
      this.timer = setTimeout(() => {
        this.form.submit();
      }, this.DELAY);
    });
  }
}


/* ─────────────────────────────────────────────────────────────
   LAZY LOAD DE IMÁGENES
   Usa IntersectionObserver sobre img[data-src]
───────────────────────────────────────────────────────────── */
class CharacterLazyImages {
  constructor() {
    this.images = document.querySelectorAll("img[data-src]");
    if (!this.images.length) return;

    if ("IntersectionObserver" in window) {
      this.observer = new IntersectionObserver(
        (entries) => entries.forEach(e => { if (e.isIntersecting) this.load(e.target); }),
        { rootMargin: "120px" }
      );
      this.images.forEach(img => this.observer.observe(img));
    } else {
      // Fallback: cargar todas de golpe
      this.images.forEach(img => this.load(img));
    }
  }

  load(img) {
    img.src = img.dataset.src;
    img.removeAttribute("data-src");
    img.classList.add("char-img-loaded");
    this.observer?.unobserve(img);
  }
}


/* ─────────────────────────────────────────────────────────────
   GRID STAGGER ANIMATION
   Anima las cards al entrar en viewport con delay escalonado
───────────────────────────────────────────────────────────── */
class GridStagger {
  constructor() {
    this.cards = document.querySelectorAll(".char-card, .char-related-card");
    if (!this.cards.length) return;
    this.init();
  }

  init() {
    this.cards.forEach((card, i) => {
      card.style.opacity = "0";
      card.style.transform = "translateY(20px)";
      card.style.transition = `opacity 0.4s ease ${i * 0.045}s, transform 0.4s ease ${i * 0.045}s`;
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
      { threshold: 0.08, rootMargin: "0px 0px -20px 0px" }
    );

    this.cards.forEach(card => observer.observe(card));
  }
}


/* ─────────────────────────────────────────────────────────────
   CARD TILT (efecto 3D suave al mover el ratón sobre las cards)
───────────────────────────────────────────────────────────── */
class CardTilt {
  constructor() {
    // Solo en desktop
    if (window.matchMedia("(hover: none)").matches) return;

    document.querySelectorAll(".char-card").forEach(card => {
      card.addEventListener("mousemove", (e) => this._tilt(e, card));
      card.addEventListener("mouseleave", () => this._reset(card));
    });
  }

  _tilt(e, card) {
    const rect   = card.getBoundingClientRect();
    const x      = (e.clientX - rect.left) / rect.width  - 0.5;
    const y      = (e.clientY - rect.top)  / rect.height - 0.5;
    const rotX   = -y * 5;
    const rotY   =  x * 5;

    card.style.transform = `translateY(-5px) perspective(700px) rotateX(${rotX}deg) rotateY(${rotY}deg)`;
    card.style.transition = "transform 0.1s linear";
  }

  _reset(card) {
    card.style.transform  = "";
    card.style.transition = "transform 0.45s ease";
  }
}


/* ─────────────────────────────────────────────────────────────
   ACTIVE FILTER COUNTER (actualiza el número de filtros activos
   en el botón "Filtros" sin recargar la página)
───────────────────────────────────────────────────────────── */
class FilterCounter {
  constructor() {
    this.form = document.getElementById("filterForm");
    if (!this.form) return;

    // Actualizar counter al cambiar cualquier campo del modal
    this.form.querySelectorAll("input, select").forEach(field => {
      field.addEventListener("change", () => this._update());
    });
  }

  _update() {
    let count = 0;
    this.form.querySelectorAll("select").forEach(sel => { if (sel.value) count++; });
    this.form.querySelectorAll("input[type=text]").forEach(inp => { if (inp.value.trim()) count++; });
    this.form.querySelectorAll("input[type=checkbox]:checked").forEach(() => count++);

    const badge = document.querySelector(".char-filter-badge");
    const btn   = document.getElementById("openFilterModal");

    if (count > 0) {
      if (badge) {
        badge.textContent = count > 9 ? "9+" : String(count);
      } else if (btn) {
        const dot = document.createElement("span");
        dot.className = "char-filter-badge";
        dot.textContent = String(count);
        btn.appendChild(dot);
      }
    } else {
      badge?.remove();
    }
  }
}


/* ─────────────────────────────────────────────────────────────
   DETAIL PAGE — QUOTE REVEAL
   Revela el bloque de cita con una animación al hacer scroll
───────────────────────────────────────────────────────────── */
class QuoteReveal {
  constructor() {
    const quote = document.querySelector(".char-quote");
    if (!quote) return;

    quote.style.opacity  = "0";
    quote.style.transform = "translateX(-12px)";
    quote.style.transition = "opacity 0.6s ease, transform 0.6s ease";

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          quote.style.opacity   = "1";
          quote.style.transform = "translateX(0)";
          observer.disconnect();
        }
      },
      { threshold: 0.3 }
    );

    observer.observe(quote);
  }
}


/* ─────────────────────────────────────────────────────────────
   INIT
───────────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  new FilterModal();
  new LiveSearch();
  new CharacterLazyImages();
  new GridStagger();
  new CardTilt();
  new FilterCounter();
  new QuoteReveal();
});