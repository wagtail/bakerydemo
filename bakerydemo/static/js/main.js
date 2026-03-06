
// document.addEventListener('DOMContentLoaded', function() {
//     const searchInput = document.querySelector('.navigation__search-input');
//     const clearBtn = document.getElementById('search-clear');

//     if (searchInput && clearBtn) {
//         // Show/Hide button based on input value
//         searchInput.addEventListener('input', () => {
//             if (searchInput.value.length > 0) {
//                 clearBtn.classList.remove('is-hidden');
//             } else {
//                 clearBtn.classList.add('is-hidden');
//             }
//         });

//         // Clear input when clicked
//         clearBtn.addEventListener('click', () => {
//             searchInput.value = '';
//             clearBtn.classList.add('is-hidden');
//             searchInput.focus();
//         });
//     }
// });
    

// document.addEventListener('DOMContentLoaded', () => {
//   const navigation = document.querySelector('[data-navigation]');
//   const mobileNavigation = navigation.querySelector('[data-mobile-navigation]');
//   const body = document.querySelector('body');
//   const mobileNavigationToggle = navigation.querySelector(
//     '[data-mobile-navigation-toggle]',
//   );

  
//   function toggleMobileNavigation() {
//     if (mobileNavigation.hidden) {
//       body.classList.add('no-scroll');
//       mobileNavigation.hidden = false;
//       mobileNavigationToggle.setAttribute('aria-expanded', 'true');
//     } else {
//       body.classList.remove('no-scroll');
//       mobileNavigation.hidden = true;
//       mobileNavigationToggle.setAttribute('aria-expanded', 'false');
//     }
//   }

//   mobileNavigationToggle.addEventListener('click', () => {
//     toggleMobileNavigation();
//   });
// });
document.addEventListener('DOMContentLoaded', function() {
    // Select all potential search inputs (mobile and desktop)
    const searchInputs = document.querySelectorAll('.navigation__search-input');
    // Select the reset buttons
    const clearBtnDesktop = document.getElementById('search-clear');
    const clearBtnMobile = document.getElementById('search-clear-mobile');

    searchInputs.forEach(input => {
        input.addEventListener('input', () => {
            const currentBtn = input.id === 'mobile-search-input' ? clearBtnMobile : clearBtnDesktop;
            
            if (currentBtn) {
                // Show button if text exists, hide if empty
                if (input.value.length > 0) {
                    currentBtn.classList.remove('is-hidden');
                } else {
                    currentBtn.classList.add('is-hidden');
                }
            }
        });
    });

    // Clear button click: clear input, hide button, refocus input
    if (clearBtnDesktop) {
        clearBtnDesktop.addEventListener('click', () => {
            const desktopInput = document.querySelector('.navigation__search .navigation__search-input');
            if (desktopInput) {
                desktopInput.value = '';
                clearBtnDesktop.classList.add('is-hidden');
                desktopInput.focus();
            }
        });
    }
    if (clearBtnMobile) {
        clearBtnMobile.addEventListener('click', () => {
            const mobileInput = document.getElementById('mobile-search-input');
            if (mobileInput) {
                mobileInput.value = '';
                clearBtnMobile.classList.add('is-hidden');
                mobileInput.focus();
            }
        });
    }

    // Theme: apply stored preference on load
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme === 'dark' || storedTheme === 'light') {
        document.documentElement.setAttribute('data-theme', storedTheme);
    }

    // Minimal vanilla JS theme toggle (supports multiple buttons if needed)
    const themeToggles = document.querySelectorAll('[data-theme-toggle]');

    themeToggles.forEach((toggle) => {
        toggle.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme') || 'light';
            const next = current === 'dark' ? 'light' : 'dark';

            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
        });
    });
});
