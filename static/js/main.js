document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;

  document.querySelectorAll(".alien-card, .omni-button, .back-link, .sidebar a, .topbar nav a, button, .collection-card").forEach(control => {
    control.addEventListener("mouseenter", () => body.dataset.scan = "active");
    control.addEventListener("mouseleave", () => body.dataset.scan = "");
  });

  document.querySelectorAll(".alien-card").forEach(card => {
    card.addEventListener("click", event => {
      const target = card.getAttribute("href");
      if (!target || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      event.preventDefault();
      const name = card.dataset.alienName || "ALIEN";
      const image = card.querySelector("img")?.src || "";
      const overlay = document.createElement("div");
      overlay.className = "omnitrix-selection";
      overlay.innerHTML = `<div class="omnitrix-device" aria-hidden="true"><div class="omnitrix-ring ring-outer"></div><div class="omnitrix-ring ring-middle"></div><div class="omnitrix-dial">${image ? `<img src="${image}" alt="">` : ""}</div><div class="omnitrix-core"></div></div><div class="omnitrix-readout">DNA SELECTED // ${name}</div><div class="omnitrix-progress"><span></span></div>`;
      body.appendChild(overlay);
      body.classList.add("omnitrix-active");
      window.setTimeout(() => { window.location.href = target; }, 900);
    });
  });

  document.querySelectorAll("[data-go-back]").forEach(button => {
    button.addEventListener("click", () => {
      if (window.history.length > 1) window.history.back();
      else window.location.href = button.dataset.goBack;
    });
  });
});
