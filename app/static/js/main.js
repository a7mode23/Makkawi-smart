/**
 * Makkawi Smart - Main JavaScript
 * Shared utilities and global event handlers
 */

// ─── Page Load Animations ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.mk-feature-card').forEach(card => {
        observer.observe(card);
    });
});

// ─── Utility Functions ─────────────────────────────────────────────────────────
const MakkawSmart = {
    /**
     * Show a toast notification
     */
    toast(message, type = 'info') {
        console.log(`[${type.toUpperCase()}] ${message}`);
    },

    /**
     * Format bytes to human-readable
     */
    formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
    },

    /**
     * Format uptime seconds to readable string
     */
    formatUptime(seconds) {
        const days = Math.floor(seconds / 86400);
        const hours = Math.floor((seconds % 86400) / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        return `${days}d ${hours}h ${mins}m`;
    }
};
