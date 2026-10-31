"use strict";

// The invitation and the configuration remain usable without JavaScript.
const status = document.getElementById("copy-status");
let statusTimer;

document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const field = document.getElementById(button.dataset.copy);
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(field.value);
      status.textContent = button.dataset.copy === "public-key" ? "Öffentlicher Schlüssel kopiert." : "Einladungslink kopiert.";
    } catch {
      field.focus();
      field.select();
      field.setSelectionRange(0, field.value.length);
      status.textContent = "Text ist markiert. Bitte über das Kopiermenü kopieren.";
    }
    clearTimeout(statusTimer);
    statusTimer = setTimeout(() => { status.textContent = ""; }, 6000);
  });
});
