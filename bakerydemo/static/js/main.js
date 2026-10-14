document.addEventListener('DOMContentLoaded', () => {
  const navigation = document.querySelector('[data-navigation]');
  const body = document.querySelector('body');
  const mobileNavigation = navigation?.querySelector(
    '[data-mobile-navigation]',
  );
  const mobileNavigationToggle = navigation?.querySelector(
    '[data-mobile-navigation-toggle]',
  );
  const themeToggles = document.querySelectorAll('[data-theme-toggle]');

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

  function updateThemeToggleState() {
    const isDark =
      document.documentElement.style.colorScheme === 'dark' ||
      document.querySelector('meta[name="color-scheme"]')?.content === 'dark';

    themeToggles.forEach((toggle) => {
      toggle.setAttribute('aria-pressed', String(isDark));
      toggle.setAttribute(
        'aria-label',
        `Switch to ${isDark ? 'light' : 'dark'} theme`,
      );
    });
  }

  document.addEventListener('theme:toggle-theme-mode', () => {
    window.requestAnimationFrame(() => {
      updateThemeToggleState();
    });
  });

  updateThemeToggleState();

  themeToggles.forEach((toggle) => {
    toggle.addEventListener('click', () => {
      document.dispatchEvent(new CustomEvent('theme:toggle-theme-mode'));
    });
  });
});
