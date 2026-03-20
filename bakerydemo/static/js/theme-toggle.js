// Deferred execution waits for the DOM content to safely load, handling the interactive logic.
document.addEventListener('DOMContentLoaded', function () {
  var toggleBtn = document.getElementById('theme-toggle');

  if (toggleBtn) {
    // Initial accessibility setup based on applied class
    var isDark = document.documentElement.classList.contains('dark');
    toggleBtn.setAttribute('aria-pressed', isDark);

    toggleBtn.addEventListener('click', function () {
      var isCurrentlyDark = document.documentElement.classList.contains('dark');

      if (isCurrentlyDark) {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        toggleBtn.setAttribute('aria-pressed', 'false');
      } else {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        toggleBtn.setAttribute('aria-pressed', 'true');
      }
    });
  }
});
