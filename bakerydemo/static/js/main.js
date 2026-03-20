document.addEventListener('DOMContentLoaded', () => {
  const navigation = document.querySelector('[data-navigation]');
  const mobileNavigation = navigation.querySelector('[data-mobile-navigation]');
  const body = document.querySelector('body');
  const mobileNavigationToggle = navigation.querySelector(
    '[data-mobile-navigation-toggle]',
  );

  function toggleMobileNavigation() {
    if (mobileNavigation.hidden) {
      body.classList.add('no-scroll');
      mobileNavigation.hidden = false;
      mobileNavigationToggle.setAttribute('aria-expanded', 'true');
    } else {
      body.classList.remove('no-scroll');
      mobileNavigation.hidden = true;
      mobileNavigationToggle.setAttribute('aria-expanded', 'false');
    }
  }

  mobileNavigationToggle.addEventListener('click', () => {
    toggleMobileNavigation();
  });

  // ── Theme Toggle ──────────────────────────────────────────────────────────
  const themeToggle = document.getElementById('theme-toggle');

  /**
   * Apply a theme ('light' | 'dark') to the document:
   *  - Sets / removes [data-theme="dark"] on <html>
   *  - Shows the correct icon inside the toggle button
   */
  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
    // Update aria-label for screen readers
    if (themeToggle) {
      themeToggle.setAttribute(
        'aria-label',
        theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode',
      );
    }
  }

  // Determine initial theme:
  //   1. User's saved preference takes priority.
  //   2. Default to light — user switches to dark manually.
  function getInitialTheme() {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark' || saved === 'light') return saved;
    return 'light';
  }

  let currentTheme = getInitialTheme();
  applyTheme(currentTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
      localStorage.setItem('theme', currentTheme);
      applyTheme(currentTheme);
    });
  }
});
