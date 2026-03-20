// Deferred execution waits for the DOM content to safely load, handling the interactive logic.
document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('theme-toggle');

  if (!toggleBtn) return;

  const root = document.documentElement;

  try {
    // Initial accessibility state
    const isDark = root.classList.contains('dark');
    toggleBtn.setAttribute('aria-pressed', isDark);
    toggleBtn.setAttribute('aria-label', 'Toggle dark mode');

    toggleBtn.addEventListener('click', function () {
      const isCurrentlyDark = root.classList.contains('dark');

      if (isCurrentlyDark) {
        root.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        toggleBtn.setAttribute('aria-pressed', 'false');
      } else {
        root.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        toggleBtn.setAttribute('aria-pressed', 'true');
      }
    });
  } catch (e) {
    // Fail silently if localStorage is unavailable
  }
});