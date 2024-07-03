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

document.addEventListener('DOMContentLoaded', () => {
  mobileNavigationToggle.addEventListener('click', () => {
    toggleMobileNavigation();
  });
});
