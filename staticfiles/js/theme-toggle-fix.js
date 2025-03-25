/**
 * Theme toggle fixer script to ensure toggle works infinitely
 * This is a last-resort script to fix any potential issues with the theme toggle
 */
window.addEventListener('load', function() {
    console.log('Theme toggle fixer script loaded');
    
    // Wait for any other scripts to finish (short delay)
    setTimeout(function() {
        const themeToggle = document.querySelector('.theme-toggle');
        
        if (themeToggle) {
            console.log('Theme toggle found - ensuring it works for infinite toggling');
            
            // Remove all existing click listeners and replace with a single reliable one
            themeToggle.replaceWith(themeToggle.cloneNode(true));
            
            // Get the fresh button with no event listeners
            const freshToggle = document.querySelector('.theme-toggle');
            
            // Add our guaranteed-to-work toggle handler
            freshToggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Toggling theme from fixer script');
                
                // Simple but effective toggle
                const isDarkMode = document.documentElement.classList.contains('dark-mode') || 
                                  document.body.classList.contains('dark-mode');
                
                if (isDarkMode) {
                    // Switch to light mode
                    document.documentElement.classList.add('light-mode');
                    document.body.classList.add('light-mode');
                    document.documentElement.classList.remove('dark-mode');
                    document.body.classList.remove('dark-mode');
                    localStorage.setItem('theme', 'light');
                    
                    // Update icons if they exist
                    const sunIcon = document.querySelector('.theme-toggle .sun-icon');
                    const moonIcon = document.querySelector('.theme-toggle .moon-icon');
                    if (sunIcon && moonIcon) {
                        sunIcon.style.display = 'none';
                        moonIcon.style.display = 'inline-block';
                    }
                    
                    console.log('Fixed toggle: Switched to light mode');
                } else {
                    // Switch to dark mode
                    document.documentElement.classList.add('dark-mode');
                    document.body.classList.add('dark-mode');
                    document.documentElement.classList.remove('light-mode');
                    document.body.classList.remove('light-mode');
                    localStorage.setItem('theme', 'dark');
                    
                    // Update icons if they exist
                    const sunIcon = document.querySelector('.theme-toggle .sun-icon');
                    const moonIcon = document.querySelector('.theme-toggle .moon-icon');
                    if (sunIcon && moonIcon) {
                        sunIcon.style.display = 'inline-block';
                        moonIcon.style.display = 'none';
                    }
                    
                    console.log('Fixed toggle: Switched to dark mode');
                }
            });
            
            console.log('Theme toggle fixed - should now work infinitely');
        }
    }, 500);
});
