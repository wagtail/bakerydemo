document.addEventListener('DOMContentLoaded', () => {
  const navigation = document.querySelector('[data-navigation]');
  const themeToggle = document.querySelector('[data-theme-toggle]');
  const htmlElement = document.documentElement;
  const storage = {
    get(key) {
      try {
        return localStorage.getItem(key);
      } catch {
        return null;
      }
    },
    set(key, value) {
      try {
        localStorage.setItem(key, value);
      } catch {
        // Ignore storage failures and keep the theme change in-memory only.
      }
    },
  };

  function updateThemeToggleLabel() {
    if (!themeToggle) {
      return;
    }
    const isDarkTheme = htmlElement.dataset.theme === 'dark';
    themeToggle.textContent = isDarkTheme ? 'Light theme' : 'Dark theme';
    themeToggle.setAttribute('aria-pressed', isDarkTheme ? 'true' : 'false');
    themeToggle.setAttribute(
      'aria-label',
      isDarkTheme ? 'Switch to light theme' : 'Switch to dark theme',
    );
  }

  if (navigation) {
    const mobileNavigation = navigation.querySelector(
      '[data-mobile-navigation]',
    );
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
  }

  if (themeToggle) {
    updateThemeToggleLabel();

    themeToggle.addEventListener('click', () => {
      const nextTheme = htmlElement.dataset.theme === 'dark' ? 'light' : 'dark';
      htmlElement.dataset.theme = nextTheme;
      storage.set('theme', nextTheme);
      updateThemeToggleLabel();
    });
  }
});
