// Main JavaScript file for Fake News Detector

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize dynamic content loading
    initializeDynamicLoading();
    
    // Initialize progress tracking
    initializeProgressTracking();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize form validation and enhancements
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Real-time character counting for text areas
    const textareas = document.querySelectorAll('textarea[data-max-length]');
    textareas.forEach(function(textarea) {
        const maxLength = parseInt(textarea.getAttribute('data-max-length'));
        const counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.innerHTML = `<span class="char-count">0</span>/${maxLength} characters`;
        textarea.parentNode.appendChild(counter);
        
        textarea.addEventListener('input', function() {
            const currentLength = textarea.value.length;
            counter.querySelector('.char-count').textContent = currentLength;
            
            if (currentLength > maxLength * 0.9) {
                counter.classList.add('text-warning');
            } else {
                counter.classList.remove('text-warning');
            }
            
            if (currentLength >= maxLength) {
                counter.classList.add('text-danger');
                counter.classList.remove('text-warning');
            } else {
                counter.classList.remove('text-danger');
            }
        });
    });
}

/**
 * Initialize dynamic content loading
 */
function initializeDynamicLoading() {
    // Auto-save form data to localStorage
    const forms = document.querySelectorAll('form[data-auto-save]');
    forms.forEach(function(form) {
        const formId = form.getAttribute('id');
        if (!formId) return;
        
        // Load saved data
        loadFormData(formId);
        
        // Save on input
        form.addEventListener('input', function() {
            saveFormData(formId);
        });
        
        // Clear on submit
        form.addEventListener('submit', function() {
            clearFormData(formId);
        });
    });
}

/**
 * Initialize progress tracking for long-running operations
 */
function initializeProgressTracking() {
    const analysisForm = document.getElementById('analysisForm');
    if (analysisForm) {
        analysisForm.addEventListener('submit', function(e) {
            showProgressModal();
            
            // Simulate progress updates
            let progress = 0;
            const interval = setInterval(function() {
                progress += Math.random() * 20;
                if (progress >= 90) {
                    progress = 90;
                    clearInterval(interval);
                }
                updateProgress(progress);
            }, 500);
        });
    }
}

/**
 * Show progress modal with animated progress bar
 */
function showProgressModal() {
    const modalHTML = `
        <div class="modal fade" id="progressModal" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content bg-dark border-secondary">
                    <div class="modal-body text-center py-5">
                        <div class="mb-4">
                            <i class="fas fa-brain fa-3x text-primary mb-3"></i>
                            <h5 class="text-light">Analyzing Content</h5>
                            <p class="text-muted mb-0">Our AI is processing your content...</p>
                        </div>
                        <div class="progress mb-3" style="height: 10px;">
                            <div class="progress-bar progress-bar-striped progress-bar-animated bg-primary" 
                                 role="progressbar" style="width: 0%" id="analysisProgress"></div>
                        </div>
                        <div class="progress-steps">
                            <small class="text-muted" id="progressText">Initializing analysis...</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if present
    const existingModal = document.getElementById('progressModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add new modal
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    const modal = new bootstrap.Modal(document.getElementById('progressModal'));
    modal.show();
}

/**
 * Update progress bar and text
 */
function updateProgress(percentage) {
    const progressBar = document.getElementById('analysisProgress');
    const progressText = document.getElementById('progressText');
    
    if (progressBar) {
        progressBar.style.width = percentage + '%';
    }
    
    if (progressText) {
        let text = 'Initializing analysis...';
        if (percentage > 20) text = 'Extracting content features...';
        if (percentage > 40) text = 'Running ML algorithms...';
        if (percentage > 60) text = 'Analyzing sentiment...';
        if (percentage > 80) text = 'Computing credibility score...';
        if (percentage >= 90) text = 'Finalizing results...';
        
        progressText.textContent = text;
    }
}

/**
 * Save form data to localStorage
 */
function saveFormData(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    const data = {};
    const formData = new FormData(form);
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    localStorage.setItem(`form_${formId}`, JSON.stringify(data));
}

/**
 * Load form data from localStorage
 */
function loadFormData(formId) {
    const savedData = localStorage.getItem(`form_${formId}`);
    if (!savedData) return;
    
    try {
        const data = JSON.parse(savedData);
        const form = document.getElementById(formId);
        
        Object.keys(data).forEach(function(key) {
            const element = form.querySelector(`[name="${key}"]`);
            if (element) {
                element.value = data[key];
            }
        });
    } catch (e) {
        console.error('Error loading form data:', e);
    }
}

/**
 * Clear form data from localStorage
 */
function clearFormData(formId) {
    localStorage.removeItem(`form_${formId}`);
}

/**
 * Format numbers with appropriate suffixes
 */
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

/**
 * Debounce function for performance optimization
 */
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

/**
 * Show notification toast
 */
function showToast(message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();
    const toastId = 'toast_' + Date.now();
    
    const toastHTML = `
        <div class="toast" id="${toastId}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${type} text-white">
                <i class="fas fa-${getToastIcon(type)} me-2"></i>
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body bg-dark text-light">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toast = new bootstrap.Toast(document.getElementById(toastId));
    toast.show();
    
    // Remove toast element after it's hidden
    document.getElementById(toastId).addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

/**
 * Get or create toast container
 */
function getOrCreateToastContainer() {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    return container;
}

/**
 * Get appropriate icon for toast type
 */
function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Smooth scroll to element
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('Copied to clipboard!', 'success');
        }).catch(function() {
            fallbackCopyTextToClipboard(text);
        });
    } else {
        fallbackCopyTextToClipboard(text);
    }
}

/**
 * Fallback copy function for older browsers
 */
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.top = '0';
    textArea.style.left = '0';
    textArea.style.position = 'fixed';
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showToast('Copied to clipboard!', 'success');
        } else {
            showToast('Failed to copy to clipboard', 'danger');
        }
    } catch (err) {
        showToast('Failed to copy to clipboard', 'danger');
    }
    
    document.body.removeChild(textArea);
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

/**
 * Initialize lazy loading for images
 */
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const lazyImageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove('lazy');
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(function(lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    }
}

// Export functions for use in other scripts
window.FakeNewsDetector = {
    showToast,
    copyToClipboard,
    smoothScrollTo,
    formatDate,
    formatNumber,
    debounce
};
