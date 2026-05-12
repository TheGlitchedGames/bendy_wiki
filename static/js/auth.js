/* ============================================================
   BENDY WIKI — auth.js
   Formularios de login, registro, contraseña — validación y UX
   ============================================================ */

"use strict";

/* ===================== TOGGLE PASSWORD ===================== */
class PasswordToggle {
  constructor() {
    document.querySelectorAll(".toggle-password").forEach(btn => {
      btn.addEventListener("click", () => this.toggle(btn));
    });
  }

  toggle(btn) {
    const targetId = btn.dataset.target;
    const input    = document.getElementById(targetId);
    const icon     = btn.querySelector("i");
    if (!input) return;

    if (input.type === "password") {
      input.type = "text";
      icon.classList.replace("fa-eye", "fa-eye-slash");
      btn.style.color = "var(--ink-gold)";
    } else {
      input.type = "password";
      icon.classList.replace("fa-eye-slash", "fa-eye");
      btn.style.color = "";
    }
  }
}

/* ===================== PASSWORD STRENGTH ===================== */
class PasswordStrength {
  constructor(inputId, fillId, labelId) {
    this.input  = document.getElementById(inputId);
    this.fill   = document.getElementById(fillId);
    this.label  = document.getElementById(labelId);
    if (this.input && this.fill) this.init();
  }

  init() {
    this.input.addEventListener("input", () => this.evaluate());
  }

  evaluate() {
    const val = this.input.value;
    let score = 0;

    if (val.length >= 8)  score++;
    if (val.length >= 12) score++;
    if (/[A-Z]/.test(val))        score++;
    if (/[a-z]/.test(val))        score++;
    if (/[0-9]/.test(val))        score++;
    if (/[^A-Za-z0-9]/.test(val)) score++;

    const levels = [
      { max: 1, pct: "15%",  color: "#e74c3c", text: "Muy débil",  css: "color:#e74c3c" },
      { max: 2, pct: "30%",  color: "#e67e22", text: "Débil",      css: "color:#e67e22" },
      { max: 3, pct: "50%",  color: "#f39c12", text: "Regular",    css: "color:#f39c12" },
      { max: 4, pct: "70%",  color: "#2ecc71", text: "Buena",      css: "color:#2ecc71" },
      { max: 5, pct: "85%",  color: "#27ae60", text: "Fuerte",     css: "color:#27ae60" },
      { max: 99,"pct": "100%", color: "var(--ink-gold)", text: "Muy fuerte ✦", css: "color:var(--ink-gold)" },
    ];

    if (!val) {
      this.fill.style.width = "0";
      if (this.label) this.label.textContent = "";
      return;
    }

    const level = levels.find(l => score <= l.max) || levels[levels.length - 1];
    this.fill.style.width = level.pct;
    this.fill.style.background = level.color;
    this.fill.style.boxShadow  = `0 0 6px ${level.color}66`;

    if (this.label) {
      this.label.setAttribute("style", level.css);
      this.label.textContent = level.text;
    }
  }
}

/* ===================== PASSWORD MATCH ===================== */
class PasswordMatch {
  constructor(pass1Id, pass2Id, indicatorId) {
    this.pass1     = document.getElementById(pass1Id);
    this.pass2     = document.getElementById(pass2Id);
    this.indicator = document.getElementById(indicatorId);
    if (this.pass1 && this.pass2 && this.indicator) this.init();
  }

  init() {
    [this.pass1, this.pass2].forEach(el =>
      el.addEventListener("input", () => this.check())
    );
  }

  check() {
    const v1 = this.pass1.value;
    const v2 = this.pass2.value;
    if (!v2) { this.indicator.textContent = ""; return; }

    if (v1 === v2) {
      this.indicator.style.color = "var(--color-success)";
      this.indicator.textContent = "✓ Las contraseñas coinciden";
      this.pass2.style.borderColor = "var(--color-success)";
    } else {
      this.indicator.style.color = "var(--color-error)";
      this.indicator.textContent = "✗ Las contraseñas no coinciden";
      this.pass2.style.borderColor = "var(--color-error)";
    }
  }
}

/* ===================== FORM SUBMIT LOADING ===================== */
class FormSubmitLoading {
  constructor(formId, btnId) {
    this.form = document.getElementById(formId);
    this.btn  = document.getElementById(btnId);
    if (this.form && this.btn) this.init();
  }

  init() {
    this.form.addEventListener("submit", () => {
      const text    = this.btn.querySelector(".btn-text");
      const loading = this.btn.querySelector(".btn-loading");
      if (text && loading) {
        text.classList.add("d-none");
        loading.classList.remove("d-none");
      }
      this.btn.disabled = true;
    });
  }
}

/* ===================== AUTH BRANDING INK BG ===================== */
class AuthBrandingInk {
  constructor() {
    this.bg = document.getElementById("authInkBg");
    if (this.bg) this.generate();
  }

  generate() {
    for (let i = 0; i < 6; i++) {
      const blob = document.createElement("div");
      const size = Math.random() * 120 + 60;
      blob.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${Math.random() * 100}%;
        top:  ${Math.random() * 100}%;
        background: radial-gradient(circle,
          rgba(212,170,71,${Math.random() * 0.06 + 0.02}) 0%,
          transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        animation: float-up ${Math.random() * 6 + 8}s ease-in-out ${Math.random() * 4}s infinite alternate;
      `;
      this.bg.appendChild(blob);
    }
  }
}

/* ===================== LOGIN SHAKE ON ERROR ===================== */
class LoginShakeError {
  constructor(formId) {
    this.form = document.getElementById(formId);
    if (this.form) this.init();
  }

  init() {
    const hasErrors = this.form.querySelectorAll(".bendy-field-error, .bendy-non-field-error");
    if (hasErrors.length) {
      this.form.style.animation = "shake 0.5s ease";
      setTimeout(() => { this.form.style.animation = ""; }, 600);
    }
  }
}

/* ===================== INPUT FOCUS INK EFFECT ===================== */
class InputFocusEffect {
  constructor() {
    document.querySelectorAll(".bendy-input, .bendy-select, .bendy-textarea").forEach(input => {
      input.addEventListener("focus", (e) => this.onFocus(e.target));
      input.addEventListener("blur",  (e) => this.onBlur(e.target));
    });
  }

  onFocus(input) {
    const wrapper = input.closest(".form-group-bendy");
    if (wrapper) {
      const label = wrapper.querySelector(".bendy-label");
      if (label) label.style.color = "var(--ink-gold)";
    }
  }

  onBlur(input) {
    const wrapper = input.closest(".form-group-bendy");
    if (wrapper) {
      const label = wrapper.querySelector(".bendy-label");
      if (label) label.style.color = "";
    }
  }
}

/* ===================== AUTH CONTAINER REVEAL ===================== */
class AuthContainerReveal {
  constructor() {
    const container = document.getElementById("authContainer");
    if (!container) return;

    container.style.opacity = "0";
    container.style.transform = "scale(0.96) translateY(16px)";

    requestAnimationFrame(() => {
      container.style.transition = "opacity 0.5s ease, transform 0.5s ease";
      container.style.opacity    = "1";
      container.style.transform  = "scale(1) translateY(0)";
    });
  }
}

/* ===================== INIT ===================== */
document.addEventListener("DOMContentLoaded", () => {
  new PasswordToggle();
  new InputFocusEffect();
  new AuthBrandingInk();
  new AuthContainerReveal();

  // Login
  new FormSubmitLoading("loginForm", "loginBtn");
  new LoginShakeError("loginForm");

  // Registro
  new PasswordStrength("id_password1", "strengthFill", "strengthLabel");
  new PasswordMatch("id_password1", "id_password2", "matchIndicator");
  new FormSubmitLoading("registerForm", "registerBtn");
  new LoginShakeError("registerForm");

  // Cambio de contraseña
  new PasswordStrength("id_new_password1", "strengthFill", "strengthLabel");
  new PasswordMatch("id_new_password1", "id_new_password2", "matchIndicator");
});
