document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;

  document.querySelectorAll(".alien-card, .omni-button, .back-link, .sidebar a, .topbar nav a, button, .collection-card").forEach(control => {
    control.addEventListener("mouseenter", () => body.dataset.scan = "active");
    control.addEventListener("mouseleave", () => body.dataset.scan = "");
  });

  function playOmnitrixTransition({ target, image, name, label = "DNA SELECTED" }) {
    if (!target || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return false;

    const overlay = document.createElement("div");
    overlay.className = "omnitrix-selection";
    overlay.innerHTML = `<div class="omnitrix-device" aria-hidden="true"><div class="omnitrix-ring ring-outer"></div><div class="omnitrix-ring ring-middle"></div><div class="omnitrix-dial">${image ? `<img src="${image}" alt="">` : ""}</div><div class="omnitrix-core"></div></div><div class="omnitrix-readout">${label} // ${name}</div><div class="omnitrix-progress"><span></span></div>`;
    body.appendChild(overlay);
    body.classList.add("omnitrix-active");
    window.setTimeout(() => { window.location.href = target; }, 900);
    return true;
  }

  document.querySelectorAll(".alien-card").forEach(card => {
    card.addEventListener("click", event => {
      const target = card.getAttribute("href");
      const image = card.dataset.selectionImage || card.querySelector("img")?.src || "";
      const name = card.dataset.alienName || "ALIEN";
      if (!target || !playOmnitrixTransition({ target, image, name })) return;
      event.preventDefault();
    });
  });

  document.querySelectorAll("[data-ultimate-transition]").forEach(button => {
    button.addEventListener("click", event => {
      const target = button.getAttribute("href");
      const image = button.dataset.ultimateTransition;
      const name = button.dataset.transitionName || "ALIEN SUPREMO";
      if (!target || !playOmnitrixTransition({ target, image, name, label: "ULTIMATRIX // EVOLUTION" })) return;
      event.preventDefault();
    });
  });

  document.querySelectorAll("[data-go-back]").forEach(button => {
    button.addEventListener("click", event => {
      event.preventDefault();
      if (window.history.length > 1) window.history.back();
      else window.location.href = button.dataset.goBack;
    });
  });
});
