/* If a card picture cannot load (for example the image server is
   down), show CardVault's own placeholder instead of a broken image.
   Loaded in the <head>, before any picture, so no failure is missed.
   Image errors do not bubble, so the listener uses the capture phase. */
document.addEventListener("error", function (event) {
    const img = event.target;
    if (!(img instanceof HTMLImageElement)) {
        return;
    }
    const fallback = img.dataset.fallback;
    if (fallback && img.getAttribute("src") !== fallback) {
        img.src = fallback;
    }
}, true);
