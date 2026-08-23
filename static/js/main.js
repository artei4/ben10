document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;

  document.querySelectorAll(".alien-card, .omni-button, .back-link, .sidebar a, .topbar nav a, button, .collection-card").forEach(control => {
    control.addEventListener("mouseenter", () => body.dataset.scan = "active");
    control.addEventListener("mouseleave", () => body.dataset.scan = "");
  });

  function playOmnitrixTransition({ target, image, name, label = "DNA SELECTED", variant = "normal" }) {
    if (!target) return false;

    // Mesmo com movimento reduzido, mantemos a navegação funcionando.
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      window.location.href = target;
      return true;
    }

    const overlay = document.createElement("div");
    overlay.className = `omnitrix-selection omnitrix-${variant}`;
    overlay.setAttribute("role", "status");
    overlay.setAttribute("aria-live", "assertive");
    overlay.innerHTML = `
      <div class="omnitrix-device" aria-hidden="true">
        <div class="omnitrix-ring ring-outer"></div>
        <div class="omnitrix-ring ring-middle"></div>
        <div class="omnitrix-ring ring-symbol"></div>
        <div class="omnitrix-dial">
          ${image ? `<img src="${image}" alt="">` : ""}
        </div>
        <div class="omnitrix-core"></div>
      </div>
      <div class="omnitrix-readout">${label} // ${name}</div>
      <div class="omnitrix-progress"><span></span></div>
    `;

    body.appendChild(overlay);
    body.classList.add("omnitrix-active");
    document.documentElement.classList.add("omnitrix-lock-scroll");

    // A forma Suprema tem uma sequência um pouco mais longa e agressiva.
    const duration = variant === "ultimate" ? 1350 : 900;
    window.setTimeout(() => {
      window.location.href = target;
    }, duration);
    return true;
  }

  document.querySelectorAll(".alien-card").forEach(card => {
    card.addEventListener("click", event => {
      const target = card.getAttribute("href");
      const image = card.dataset.selectionImage || card.querySelector("img")?.src || "";
      const name = card.dataset.alienName || "ALIEN";
      if (!playOmnitrixTransition({ target, image, name })) return;
      event.preventDefault();
    });
  });

  document.querySelectorAll("[data-ultimate-transition]").forEach(button => {
    button.addEventListener("click", event => {
      const target = button.getAttribute("href");
      const image = button.dataset.ultimateTransition;
      const name = button.dataset.transitionName || "ALIEN SUPREMO";
      if (!playOmnitrixTransition({
        target,
        image,
        name,
        label: "ULTIMATRIX // EVOLUTION",
        variant: "ultimate"
      })) return;
      event.preventDefault();
    });
  });

  // Volta exatamente para a coleção/página de origem sempre que possível.
  document.querySelectorAll("[data-go-back]").forEach(button => {
    button.addEventListener("click", event => {
      event.preventDefault();
      const fallback = button.dataset.goBack;
      if (window.history.length > 1 && document.referrer) {
        window.history.back();
      } else if (fallback) {
        window.location.href = fallback;
      }
    });
  });

  // Compatibilidade com formulários antigos: o servidor é a autoridade final do redirecionamento.
  document.querySelectorAll(".auth-redirect-form").forEach(form => {
    form.addEventListener("submit", async event => {
      event.preventDefault();
      const button = form.querySelector("button[type='submit']");
      if (button) button.disabled = true;
      try {
        const response = await fetch(form.action || window.location.href, {
          method: "POST",
          body: new FormData(form),
          credentials: "same-origin",
          redirect: "follow"
        });
        if (response.redirected) {
          window.location.href = form.dataset.successUrl || "/aliens";
          return;
        }
        const html = await response.text();
        document.open();
        document.write(html);
        document.close();
      } catch (error) {
        form.submit();
      } finally {
        if (button) button.disabled = false;
      }
    });
  });
});
