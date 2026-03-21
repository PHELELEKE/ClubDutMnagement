// main JS

// Theme Toggle (Dark/Light Mode)
const themeToggle = document.getElementById('themeToggle');
function initTheme() {
    // Check for saved theme or system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
}

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

// Legacy dark mode support
const switchInput = document.getElementById('darkSwitch');
function initDarkModeLegacy() {
    if (localStorage.getItem('dark-mode') === 'true' ||
        (!('dark-mode' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.body.classList.add('dark');
        if (switchInput) switchInput.checked = true;
    }
}
if (switchInput) {
    switchInput.addEventListener('change', () => {
        document.body.classList.toggle('dark');
        localStorage.setItem('dark-mode', switchInput.checked);
    });
}

// mobile burger menu
const burger = document.getElementById('burger');
if (burger) {
    burger.addEventListener('click', () => {
        document.querySelector('.nav-items').classList.toggle('open');
    });
}

// =====================
// Real-time Notification Polling (WhatsApp-style)
// =====================

function updateNotificationBadges() {
    // Check if user is logged in by looking for nav links
    const isLoggedIn = document.querySelector('.navbar') !== null;
    if (!isLoggedIn) return;
    
    // Update notifications badge
    fetch('/notifications/api/unread-count')
        .then(res => res.json())
        .then(data => {
            updateBadgeByLink('/notifications', data.count);
        })
        .catch(() => {});
    
    // Update announcements badge
    fetch('/announcements/api/unread-count')
        .then(res => res.json())
        .then(data => {
            updateBadgeByLink('/announcements', data.count);
        })
        .catch(() => {});
    
    // Update chat badge
    fetch('/chat/api/unread-count')
        .then(res => res.json())
        .then(data => {
            updateBadgeByLink('/chat', data.count);
        })
        .catch(() => {});
}

function updateBadgeByLink(href, count) {
    // Find the nav link with this href
    const links = document.querySelectorAll('a.nav-link');
    
    links.forEach(link => {
        if (link.getAttribute('href') === href || 
            (link.href && link.href.includes(href))) {
            let badge = link.querySelector('.notification-badge');
            
            if (count > 0) {
                // Create badge if it doesn't exist
                if (!badge) {
                    badge = document.createElement('span');
                    badge.className = 'notification-badge';
                    link.appendChild(badge);
                }
                badge.textContent = count > 99 ? '99+' : count;
                badge.style.display = 'inline-flex';
                // Add pulse animation for new notifications
                badge.style.animation = 'none';
                badge.offsetHeight; // Trigger reflow
                badge.style.animation = 'badgePulse 2s infinite';
            } else if (badge) {
                badge.style.display = 'none';
            }
        }
    });
}

// Add CSS for badge pulse animation
const badgeStyle = document.createElement('style');
badgeStyle.textContent = `
    @keyframes badgePulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(badgeStyle);

// Start polling when page loads
document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initDarkModeLegacy();
    
    // Start real-time notification polling (every 10 seconds - WhatsApp style)
    updateNotificationBadges();
    setInterval(updateNotificationBadges, 10000);
});

initTheme();
initDarkModeLegacy();

console.log('Main script loaded');

