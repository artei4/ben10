document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".alien-card").forEach(card => {
    card.addEventListener("mouseenter", () => {
      document.body.dataset.scan = "active";
    });
    card.addEventListener("mouseleave", () => {
      document.body.dataset.scan = "";
    });
  });
});