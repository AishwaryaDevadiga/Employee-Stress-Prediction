// Client-side interactions and theme switching logic

document.addEventListener('DOMContentLoaded', () => {
    // Theme Switcher Initialization
    const themeToggleBtn = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Apply initial theme
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeToggleIcon(currentTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const activeTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeToggleIcon(newTheme);
        });
    }

    function updateThemeToggleIcon(theme) {
        if (!themeToggleBtn) return;
        const icon = themeToggleBtn.querySelector('i');
        if (icon) {
            if (theme === 'dark') {
                icon.className = 'fas fa-sun';
            } else {
                icon.className = 'fas fa-moon';
            }
        }
    }

    // Auto-dismiss Flash Messages after 5 seconds
    const flashAlerts = document.querySelectorAll('.alert-custom');
    flashAlerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.6s ease';
            setTimeout(() => {
                alert.remove();
            }, 600);
        }, 5000);
    });

    // Client-side Heart Rate Validation and warnings
    const heartRateInput = document.getElementById('resting_heart_rate');
    const heartRateWarning = document.getElementById('hr-warning-alert');

    if (heartRateInput && heartRateWarning) {
        heartRateInput.addEventListener('input', () => {
            const hr = parseInt(heartRateInput.value, 10);
            if (isNaN(hr)) {
                heartRateWarning.classList.add('d-none');
                return;
            }

            if (hr < 60) {
                heartRateWarning.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Heart Rate is below the normal range (<60 BPM). Please consult a healthcare professional.';
                heartRateWarning.className = 'alert alert-warning d-block';
            } else if (hr > 120) {
                heartRateWarning.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Heart Rate is above the normal range (>120 BPM). Please consult a healthcare professional.';
                heartRateWarning.className = 'alert alert-warning d-block';
            } else {
                heartRateWarning.classList.add('d-none');
            }
        });
    }
});
