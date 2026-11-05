document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;

  document.querySelectorAll(".alien-card, .omni-button, .back-link, .sidebar a, .topbar nav a, button, .collection-card").forEach(control => {
    control.addEventListener("mouseenter", () => body.dataset.scan = "active");
    control.addEventListener("mouseleave", () => body.dataset.scan = "");
  });

  function playOmnitrixTransition({ target, image, name, label = "DNA SELECTED", variant = "normal", replace = false }) {
    if (!target) return false;

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

    const duration = variant === "ultimate" ? 1350 : 900;
    window.setTimeout(() => {
      // replace: a tela de entrada não fica no histórico, senão o botão "voltar" cairia nela de novo.
      if (replace) window.location.replace(target);
      else window.location.href = target;
    }, duration);
    return true;
  }

  const entry = document.querySelector("[data-omnitrix-entry]");
  if (entry) {
    playOmnitrixTransition({
      target: entry.getAttribute("href"),
      name: entry.dataset.name || "ONLINE",
      label: entry.dataset.label || "OMNITRIX",
      replace: true
    });
  }

  document.querySelectorAll(".alien-card").forEach(card => {
    card.addEventListener("click", event => {
      const target = card.getAttribute("href");
      const image = card.dataset.selectionImage || card.querySelector("img")?.src || "";
      const name = card.dataset.alienName || "ALIEN";
      const label = card.dataset.transitionLabel;
      if (!playOmnitrixTransition({ target, image, name, label })) return;
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
        label: button.dataset.transitionLabel || "ULTIMATRIX // EVOLUTION",
        variant: "ultimate"
      })) return;
      event.preventDefault();
    });
  });

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
});
