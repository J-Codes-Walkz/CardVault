/* Runs in the <head>, before the page is drawn, so nothing flashes:
   - marks the page as having JavaScript, so the phone menu can start
     closed;
   - applies the light or dark theme the visitor chose earlier;
   - notes whether the home page intro has been seen.
   The two choices live in the browser's local storage, never on the
   server (see the Privacy page). If storage is blocked, the site uses
   the device's own theme and skips the intro. Loaded as a file, not
   inline, so the Content Security Policy can block inline scripts. */
document.documentElement.classList.add("js");
(function () {
    try {
        const theme = window.localStorage.getItem("cardvault-theme");
        if (theme === "light" || theme === "dark") {
            document.documentElement.dataset.theme = theme;
        }
        if (!window.localStorage.getItem("cardvault-intro-seen")) {
            document.documentElement.classList.add("intro-pending");
        }
    } catch (error) {
        document.documentElement.classList.remove("intro-pending");
    }
}());
