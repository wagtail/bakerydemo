document.addEventListener('DOMContentLoaded', () => {
  const navigation = document.querySelector('[data-navigation]');
  const body = document.querySelector('body');
  const colorSchemeMeta = document.querySelector('meta[name="color-scheme"]');
  const mobileNavigation = navigation?.querySelector(
    '[data-mobile-navigation]',
  );
  const mobileNavigationToggle = navigation?.querySelector(
    '[data-mobile-navigation-toggle]',
  );
  const themeToggles = document.querySelectorAll('[data-theme-toggle]');

  function getPreferredTheme() {
    try {
      const storedTheme = localStorage.getItem('theme');
      if (storedTheme === 'light' || storedTheme === 'dark') {
        return storedTheme;
      }
    } catch {
      // Ignore storage access errors and fall back to the system preference.
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.style.colorScheme = theme;

    if (colorSchemeMeta) {
      colorSchemeMeta.setAttribute('content', theme);
    }

    themeToggles.forEach((toggle) => {
      const isDark = theme === 'dark';

      toggle.setAttribute('aria-pressed', String(isDark));
      toggle.setAttribute(
        'aria-label',
        `Switch to ${isDark ? 'light' : 'dark'} theme`,
      );
    });
  }

  function toggleTheme() {
    const nextTheme = getPreferredTheme() === 'dark' ? 'light' : 'dark';

    try {
      localStorage.setItem('theme', nextTheme);
    } catch {
      // Ignore storage access errors and still apply the theme for this page view.
    }

    applyTheme(nextTheme);
  }

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

  if (mobileNavigation && mobileNavigationToggle) {
    mobileNavigationToggle.addEventListener('click', () => {
      toggleMobileNavigation();
    });
  }

  applyTheme(getPreferredTheme());

  themeToggles.forEach((toggle) => {
    toggle.addEventListener('click', () => {
      toggleTheme();
    });
  });
});
