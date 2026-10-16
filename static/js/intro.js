/* Home page: the hero's "Pause animation" button, and the intro.
   The intro is shown on a visitor's first visit only: a Poké Ball
   drops in, opens and reveals the emblem and an "Enter the vault"
   button. The animation itself is CSS; this script starts it, records
   that it has been seen, and closes it. Visitors who ask for reduced
   motion see the finished scene straight away (handled in the CSS). */
document.addEventListener("DOMContentLoaded", function () {
    /* The hero's floating symbols keep moving, so they can be paused
       (WCAG 2.2.2). The choice lasts until the page is left. */
    const hero = document.querySelector(".hero-cosmic");
    const motionToggle = document.querySelector("[data-motion-toggle]");
    if (hero && motionToggle) {
        motionToggle.addEventListener("click", function () {
            const paused = hero.classList.toggle("motion-paused");
            motionToggle.textContent = paused ? "Play animation" : "Pause animation";
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const root = document.documentElement;
    const intro = document.getElementById("intro");
    if (!intro || !root.classList.contains("intro-pending")) {
        return;
    }

    try {
        window.localStorage.setItem("cardvault-intro-seen", "yes");
    } catch (error) {
        /* Storage blocked: the intro may show again next time. */
    }
    root.classList.add("intro-playing");

    function closeIntro() {
        root.classList.remove("intro-pending", "intro-playing");
        const heading = document.getElementById("hero-heading");
        if (heading) {
            heading.focus();
        }
    }

    intro.querySelectorAll("[data-close-intro]").forEach(function (button) {
        button.addEventListener("click", closeIntro);
    });
});
