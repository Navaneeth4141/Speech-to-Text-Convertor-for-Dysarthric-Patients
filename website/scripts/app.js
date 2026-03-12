/**
 * Main App Script
 * Handles initialization, theme, accessibility, and global functionality
 */

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    initializeAccessibility();
    initializeToasts();
});

/**
 * Theme Management
 */
function initializeTheme() {
    const themeToggle = document.getElementById('themeToggle');

    // Check for saved theme preference or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    } else if (systemPrefersDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);

            showToast(`Switched to ${newTheme} mode`, 'info');
        });
    }
}

/**
 * Accessibility Features
 */
function initializeAccessibility() {
    const fontIncrease = document.getElementById('fontIncrease');
    const fontDecrease = document.getElementById('fontDecrease');

    // Load saved font size
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        document.documentElement.setAttribute('data-font-size', savedFontSize);
    }

    if (fontIncrease) {
        fontIncrease.addEventListener('click', () => {
            const currentSize = document.documentElement.getAttribute('data-font-size');
            let newSize;

            if (!currentSize || currentSize === 'normal') {
                newSize = 'large';
            } else if (currentSize === 'large') {
                newSize = 'xlarge';
            } else {
                showToast('Maximum font size reached', 'info');
                return;
            }

            document.documentElement.setAttribute('data-font-size', newSize);
            localStorage.setItem('fontSize', newSize);
            showToast('Font size increased', 'info');
        });
    }

    if (fontDecrease) {
        fontDecrease.addEventListener('click', () => {
            const currentSize = document.documentElement.getAttribute('data-font-size');
            let newSize;

            if (currentSize === 'xlarge') {
                newSize = 'large';
            } else if (currentSize === 'large') {
                newSize = 'normal';
            } else {
                showToast('Minimum font size reached', 'info');
                return;
            }

            document.documentElement.setAttribute('data-font-size', newSize);
            localStorage.setItem('fontSize', newSize);
            showToast('Font size decreased', 'info');
        });
    }

    // Keyboard navigation enhancements
    document.addEventListener('keydown', (e) => {
        // ESC to close loading overlay
        if (e.key === 'Escape') {
            const loadingOverlay = document.getElementById('loadingOverlay');
            if (loadingOverlay && !loadingOverlay.classList.contains('hidden')) {
                // Can't cancel transcription, but close any modals
            }
        }

        // Space to start/stop recording when record button is focused
        if (e.key === ' ' && document.activeElement?.id === 'recordBtn') {
            e.preventDefault();
            document.getElementById('recordBtn')?.click();
        }
    });
}

/**
 * Toast Notification System
 */
let toastContainer;

function initializeToasts() {
    toastContainer = document.getElementById('toastContainer');

    // Make showToast globally available
    window.showToast = showToast;
}

function showToast(message, type = 'info') {
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        toastContainer.id = 'toastContainer';
        document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icons = {
        success: '✓',
        error: '✕',
        info: 'ℹ',
        warning: '⚠'
    };

    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || icons.info}</span>
        <span class="toast-message">${message}</span>
    `;

    toastContainer.appendChild(toast);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

/**
 * Utility Functions
 */

// Format duration in seconds to MM:SS
function formatDuration(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Check if browser supports required features
function checkBrowserSupport() {
    const features = {
        mediaDevices: !!navigator.mediaDevices?.getUserMedia,
        audioContext: !!(window.AudioContext || window.webkitAudioContext),
        mediaRecorder: typeof MediaRecorder !== 'undefined',
        speechSynthesis: 'speechSynthesis' in window
    };

    const unsupported = Object.entries(features)
        .filter(([, supported]) => !supported)
        .map(([feature]) => feature);

    if (unsupported.length > 0) {
        console.warn('Unsupported features:', unsupported);
        showToast('Some features may not work in this browser', 'warning');
    }

    return features;
}

// Run browser check on load
checkBrowserSupport();
