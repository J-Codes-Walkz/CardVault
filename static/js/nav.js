/* Header controls: the phone menu button and the dark mode toggle. */
document.addEventListener("DOMContentLoaded", function () {
    const root = document.documentElement;
    const menuButton = document.querySelector(".nav-toggle");
    const menu = document.getElementById("nav-menu");
    const themeButton = document.querySelector(".theme-toggle");
    const darkQuery = window.matchMedia("(prefers-color-scheme: dark)");

    if (menuButton && menu) {
        menuButton.addEventListener("click", function () {
            const isOpen = menuButton.getAttribute("aria-expanded") === "true";
            menuButton.setAttribute("aria-expanded", String(!isOpen));
            menu.classList.toggle("is-open", !isOpen);
        });
    }

    if (!themeButton) {
        return;
    }

    /* A theme chosen with the button wins; otherwise follow the device. */
    function isDark() {
        if (root.dataset.theme) {
            return root.dataset.theme === "dark";
        }
        return darkQuery.matches;
    }

    function showState() {
        themeButton.setAttribute("aria-pressed", String(isDark()));
    }

    themeButton.addEventListener("click", function () {
        const next = isDark() ? "light" : "dark";
        root.dataset.theme = next;
        try {
            window.localStorage.setItem("cardvault-theme", next);
        } catch (error) {
            /* Storage blocked: the choice lasts until the page closes. */
        }
        showState();
    });

    darkQuery.addEventListener("change", showState);
    showState();
});
