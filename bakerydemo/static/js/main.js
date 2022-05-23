
const navigation = document.querySelector('[data-navigation]');
const mobileNavigation = navigation.querySelector('[data-mobile-navigation]');
const body = document.querySelector('body');
const mobileNavigationToggle = navigation.querySelector('[data-mobile-navigation-toggle]');

let mobileNavigationIsOpen = false;

function toggleMobileNavigation() {
    if (mobileNavigationIsOpen) {
        body.classList.remove('no-scroll');
        mobileNavigation.setAttribute('data-active', 'closed');
        mobileNavigationToggle.setAttribute('data-active', 'closed');
    } else {
        body.classList.add('no-scroll');
        mobileNavigation.setAttribute('data-active', 'opened');
        mobileNavigationToggle.setAttribute('data-active', 'opened');
    }
    mobileNavigationIsOpen = !mobileNavigationIsOpen;
}

mobileNavigationToggle.addEventListener('click', (e) => {
    e.preventDefault();
    toggleMobileNavigation();
});
    
