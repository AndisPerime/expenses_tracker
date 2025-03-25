document.addEventListener('DOMContentLoaded', function() {
    // Set flag to indicate theme.js has loaded
    window.themeSwitcherLoaded = true;

    // Get theme elements
    const themeToggle = document.querySelector('.theme-toggle');
    const sunIcon = document.querySelector('.theme-toggle .sun-icon');
    const moonIcon = document.querySelector('.theme-toggle .moon-icon');
    
    // Initialize theme based on localStorage or system preference
    const savedTheme = localStorage.getItem('theme');
    
    function setTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.classList.add('dark-mode');
            document.body.classList.add('dark-mode');
            document.documentElement.classList.remove('light-mode');
            document.body.classList.remove('light-mode');
            
            // Update icons
            if (sunIcon && moonIcon) {
                sunIcon.style.display = 'inline-block';
                moonIcon.style.display = 'none';
            }
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.add('light-mode');
            document.body.classList.add('light-mode');
            document.documentElement.classList.remove('dark-mode');
            document.body.classList.remove('dark-mode');
            
            // Update icons
            if (sunIcon && moonIcon) {
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'inline-block';
            }
            localStorage.setItem('theme', 'light');
        }
    }
    
    // Set initial theme
    if (savedTheme === 'dark') {
        setTheme('dark');
    } else if (savedTheme === 'light') {
        setTheme('light');
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        setTheme('dark');
    } else {
        setTheme('light');
    }
    
    // Toggle theme when button is clicked
    if (themeToggle) {
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            if (document.documentElement.classList.contains('dark-mode')) {
                setTheme('light');
            } else {
                setTheme('dark');
            }
        });
    }
    
    console.log('Theme switcher initialized');
});
