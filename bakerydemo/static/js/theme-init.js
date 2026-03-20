// Loaded in the <head> to immediately verify and apply the theme preference
// before the rest of the DOM loads, preventing the "Flash of Unstyled Content" (FOUC).
(function () {
  var storedTheme = localStorage.getItem('theme');
  var prefersDark =
    window.matchMedia &&
    window.matchMedia('(prefers-color-scheme: dark)').matches;

  if (storedTheme === 'dark' || (!storedTheme && prefersDark)) {
    document.documentElement.classList.add('dark');
  }
})();
