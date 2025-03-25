/**
 * Theme switcher for Expenses Tracker
 * Handles dark/light mode preferences and toggles
 */
document.addEventListener('DOMContentLoaded', function() {
    // Add console logging for debugging
    console.log('Theme switcher initialized (correct path version)');
    
    // Flag to prevent duplicate initialization
    window.themeSwitcherLoaded = true;
    
    // Get theme toggle button
    const themeToggle = document.querySelector('.theme-toggle');
    
    // Debug if theme toggle button is found
    if (themeToggle) {
        console.log('Theme toggle button found');
        
        // Clear any existing click handlers to prevent issues
        themeToggle.onclick = null;
        
        // Add click event listener to theme toggle button
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Theme toggle clicked - handler in expenses_tracker path');
            toggleTheme();
        });
    } else {
        console.log('Theme toggle button NOT found - creating one');
        createThemeToggleButton();
    }
    
    // Initialize theme based on localStorage or system preference
    initializeTheme();
    
    /**
     * Create a theme toggle button if one doesn't exist in the DOM
     */
    function createThemeToggleButton() {
        // Check if we're on a page with a navbar
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            console.log('Creating theme toggle button in navbar');
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
            
            button.addEventListener('click', function(e) {
                e.preventDefault();
                toggleTheme();
            });
            
            navbar.appendChild(button);
            console.log('Theme toggle button created and added to navbar');
        }
    }
    
    /**
     * Initialize theme based on user preferences
     */
    function initializeTheme() {
        // Check localStorage first
        const savedTheme = localStorage.getItem('theme');
        console.log('Saved theme from localStorage:', savedTheme);
        
        if (savedTheme === 'dark') {
            setDarkMode();
        } else if (savedTheme === 'light') {
            setLightMode();
        } else {
            // If no saved preference, check system preference
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                console.log('System prefers dark mode');
                setDarkMode();
            } else {
                console.log('System prefers light mode or cannot determine preference');
                setLightMode();
            }
        }
        
        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                // Only change theme if user hasn't set a preference
                if (!localStorage.getItem('theme')) {
                    if (e.matches) {
                        setDarkMode();
                    } else {
                        setLightMode();
                    }
                }
            });
        }
    }
    
    /**
     * Toggle between light and dark themes
     */
    function toggleTheme() {
        console.log('Theme toggle clicked');
        
        // Check current theme - simplify the logic
        const isDarkMode = document.documentElement.classList.contains('dark-mode') || 
                          document.body.classList.contains('dark-mode');
        
        // Always update both documentElement and body for consistency
        if (isDarkMode) {
            setLightMode();
            localStorage.setItem('theme', 'light');
            console.log('Switched to light mode');
        } else {
            setDarkMode();
            localStorage.setItem('theme', 'dark');
            console.log('Switched to dark mode');
        }
    }
    
    /**
     * Apply dark mode to the document
     */
    function setDarkMode() {
        // Apply classes consistently 
        document.documentElement.classList.add('dark-mode');
        document.body.classList.add('dark-mode');
        document.documentElement.classList.remove('light-mode');
        document.body.classList.remove('light-mode');
        
        // Update icon if it exists
        updateThemeIcon('dark');
    }
    
    /**
     * Apply light mode to the document
     */
    function setLightMode() {
        // Apply classes consistently
        document.documentElement.classList.add('light-mode');
        document.body.classList.add('light-mode');
        document.documentElement.classList.remove('dark-mode');
        document.body.classList.remove('dark-mode');
        
        // Update icon if it exists
        updateThemeIcon('light');
    }
    
    /**
     * Update theme toggle icon based on current theme
     */
    function updateThemeIcon(theme) {
        const sunIcon = document.querySelector('.theme-toggle .sun-icon');
        const moonIcon = document.querySelector('.theme-toggle .moon-icon');
        
        if (!sunIcon || !moonIcon) {
            console.log('Theme icons not found');
            return;
        }
        
        if (theme === 'dark') {
            sunIcon.style.display = 'inline-block';
            moonIcon.style.display = 'none';
        } else {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'inline-block';
        }
        console.log(`Updated theme icon to ${theme} mode`);
    }
});
