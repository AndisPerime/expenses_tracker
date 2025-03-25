/**
 * Base JavaScript for Expenses Tracker
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Base JS initialized');
    
    // Check if theme toggle exists and initialize
    initializeThemeToggle();
    
    // Initialize mobile navigation if it exists
    initializeMobileNav();
    
    /**
     * Initialize theme toggle button
     */
    function initializeThemeToggle() {
        const themeToggle = document.querySelector('.theme-toggle');
        if (!themeToggle) {
            console.log('No theme toggle found, creating one');
            // Create theme toggle in navbar
            const navbar = document.querySelector('.navbar');
            if (navbar) {
                const button = document.createElement('button');
                button.className = 'theme-toggle';
                button.setAttribute('aria-label', 'Toggle Dark Mode');
                
                const sunIcon = document.createElement('span');
                sunIcon.className = 'icon sun-icon';
                sunIcon.textContent = '☀️';
                
                const moonIcon = document.createElement('span');
                moonIcon.className = 'icon moon-icon';
                moonIcon.textContent = '🌙';
                
                button.appendChild(sunIcon);
                button.appendChild(moonIcon);
                
                navbar.appendChild(button);
                console.log('Theme toggle created');
            }
        }
    }
    
    /**
     * Initialize mobile navigation menu
     */
    function initializeMobileNav() {
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        if (mobileToggle && navMenu) {
            mobileToggle.addEventListener('click', function() {
                navMenu.classList.toggle('active');
                document.body.classList.toggle('menu-open');
                
                // Toggle hamburger icon if it exists
                const hamburgerIcon = this.querySelector('.hamburger-icon');
                if (hamburgerIcon) {
                    hamburgerIcon.classList.toggle('active');
                }
            });
        }
    }
});
