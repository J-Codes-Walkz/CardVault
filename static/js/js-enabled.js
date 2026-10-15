/* Marks the page as having JavaScript, so the phone menu can start
   closed. Loaded as a file (not inline) so the Content Security
   Policy can block every inline script. */
document.documentElement.classList.add("js");
