/**
 * MySQL SSH Connection UI - JavaScript App
 * Author: Julian Sukrisna (Javasatu.com)
 * Created: August 2025
 */

class MySQLSSHUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupActiveNavigation();
        this.setupThemeManager();
        console.log('MySQL SSH UI initialized');
    }

    setupThemeManager() {
        // Load saved theme or default to light
        const savedTheme = localStorage.getItem('mysql-ssh-theme') || 'light';
        this.applyTheme(savedTheme);
        
        // Setup theme switcher event listeners
        document.querySelectorAll('.theme-option').forEach(option => {
            option.addEventListener('click', (e) => {
                e.preventDefault();
                const theme = e.target.closest('.theme-option').getAttribute('data-theme');
                this.applyTheme(theme);
                localStorage.setItem('mysql-ssh-theme', theme);
            });
        });
        
        // Update theme dropdown text
        this.updateThemeDropdownText(savedTheme);
    }

    applyTheme(theme) {
        // Remove existing theme classes
        document.documentElement.removeAttribute('data-theme');
        
        // Apply new theme
        if (theme !== 'light') {
            document.documentElement.setAttribute('data-theme', theme);
        }
        
        // Update active theme in dropdown
        document.querySelectorAll('.theme-option').forEach(option => {
            option.classList.remove('active');
            if (option.getAttribute('data-theme') === theme) {
                option.classList.add('active');
            }
        });
        
        // Add theme-specific classes for special effects
        document.body.className = document.body.className.replace(/theme-\w+/g, '');
        document.body.classList.add(`theme-${theme}`);
        
        // Matrix theme special effects
        if (theme === 'matrix') {
            this.enableMatrixEffects();
        } else {
            this.disableMatrixEffects();
        }
        
        this.updateThemeDropdownText(theme);
    }

    updateThemeDropdownText(theme) {
        const themeDropdown = document.getElementById('themeDropdown');
        const themeNames = {
            'light': '<i class="fas fa-sun"></i><span class="d-none d-xl-inline ms-1">Light</span>',
            'dark': '<i class="fas fa-moon"></i><span class="d-none d-xl-inline ms-1">Dark</span>',
            'matrix': '<i class="fas fa-code"></i><span class="d-none d-xl-inline ms-1">Matrix</span>'
        };
        
        if (themeDropdown) {
            themeDropdown.innerHTML = themeNames[theme];
        }
    }

    enableMatrixEffects() {
        // Add matrix rain effect to navbar brand
        const brand = document.querySelector('.navbar-brand');
        if (brand) {
            brand.style.animation = 'matrix-glow 2s ease-in-out infinite alternate';
        }
        
        // Add pulsing effect to connected badge
        const connectedBadge = document.querySelector('.badge.bg-success');
        if (connectedBadge) {
            connectedBadge.style.animation = 'matrix-pulse 1.5s ease-in-out infinite';
        }
    }

    disableMatrixEffects() {
        // Remove matrix effects
        const brand = document.querySelector('.navbar-brand');
        if (brand) {
            brand.style.animation = '';
        }
        
        const connectedBadge = document.querySelector('.badge.bg-success');
        if (connectedBadge) {
            connectedBadge.style.animation = 'pulse 2s infinite';
        }
    }

    setupActiveNavigation() {
        // Mark active navigation item
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPath || (currentPath === '/' && href === '/')) {
                link.classList.add('active');
            }
        });
    }

    setupEventListeners() {
        // Form validation
        this.setupFormValidation();
        
        // AJAX handlers
        this.setupAjaxHandlers();
        
        // UI enhancements
        this.setupUIEnhancements();
    }

    setupFormValidation() {
        const forms = document.querySelectorAll('form[novalidate]');
        forms.forEach(form => {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        });

        // Real-time validation
        const inputs = document.querySelectorAll('input[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', this.validateInput.bind(this));
            input.addEventListener('input', this.clearValidationError.bind(this));
        });
    }

    setupAjaxHandlers() {
        // Setup CSRF token for AJAX requests
        const csrfToken = document.querySelector('meta[name=csrf-token]');
        if (csrfToken) {
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrfToken.getAttribute('content'));
                    }
                }
            });
        }
    }

    setupUIEnhancements() {
        // Auto-hide alerts after 5 seconds
        setTimeout(() => {
            $('.alert').fadeOut();
        }, 5000);

        // Tooltip initialization
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Add fade-in animation to cards
        $('.card').addClass('fade-in');
    }

    initializeComponents() {
        // Initialize any page-specific components
        if (window.location.pathname.includes('/query')) {
            this.initializeQueryPage();
        }
        
        if (window.location.pathname.includes('/dashboard')) {
            this.initializeDashboard();
        }
    }

    handleFormSubmit(event) {
        const form = event.target;
        if (!this.validateForm(form)) {
            event.preventDefault();
            event.stopPropagation();
        } else {
            this.showLoadingState(form);
        }
        form.classList.add('was-validated');
    }

    validateForm(form) {
        const inputs = form.querySelectorAll('input[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateInput({ target: input })) {
                isValid = false;
            }
        });

        return isValid;
    }

    validateInput(event) {
        const input = event.target;
        const value = input.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Required validation
        if (input.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required';
        }

        // Type-specific validation
        if (isValid && value) {
            switch (input.type) {
                case 'email':
                    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                        isValid = false;
                        errorMessage = 'Please enter a valid email address';
                    }
                    break;
                case 'number':
                    const num = parseInt(value);
                    const min = parseInt(input.getAttribute('min'));
                    const max = parseInt(input.getAttribute('max'));
                    if (isNaN(num) || (min && num < min) || (max && num > max)) {
                        isValid = false;
                        errorMessage = `Please enter a number between ${min || 1} and ${max || 65535}`;
                    }
                    break;
            }
        }

        this.showValidationResult(input, isValid, errorMessage);
        return isValid;
    }

    showValidationResult(input, isValid, errorMessage) {
        input.classList.toggle('is-valid', isValid);
        input.classList.toggle('is-invalid', !isValid);

        // Remove existing feedback
        const existingFeedback = input.parentNode.querySelector('.invalid-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }

        // Add error message if invalid
        if (!isValid && errorMessage) {
            const feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            feedback.textContent = errorMessage;
            input.parentNode.appendChild(feedback);
        }
    }

    clearValidationError(event) {
        const input = event.target;
        input.classList.remove('is-invalid');
        const feedback = input.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    }

    showLoadingState(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            submitBtn.disabled = true;

            // Store original text for potential restoration
            submitBtn.dataset.originalText = originalText;
        }
    }

    initializeQueryPage() {
        // Query page specific initialization
        console.log('Query page initialized');
        
        // Setup query execution
        const queryForm = document.getElementById('queryForm');
        if (queryForm) {
            queryForm.addEventListener('submit', this.executeQuery.bind(this));
        }

        // Setup query templates
        this.setupQueryTemplates();
    }

    initializeDashboard() {
        // Dashboard specific initialization
        console.log('Dashboard initialized');
        
        // Auto-refresh connection status every 30 seconds
        setInterval(this.checkConnectionStatus.bind(this), 30000);
    }

    setupQueryTemplates() {
        const templates = {
            'show-databases': 'SHOW DATABASES;',
            'show-tables': 'SHOW TABLES;',
            'describe-table': 'DESCRIBE table_name;',
            'select-all': 'SELECT * FROM table_name LIMIT 10;'
        };

        Object.keys(templates).forEach(key => {
            const btn = document.querySelector(`[data-template="${key}"]`);
            if (btn) {
                btn.addEventListener('click', () => {
                    const textarea = document.getElementById('queryText');
                    if (textarea) {
                        textarea.value = templates[key];
                        textarea.focus();
                    }
                });
            }
        });
    }

    executeQuery(event) {
        event.preventDefault();
        
        const queryText = document.getElementById('queryText').value.trim();
        if (!queryText) {
            this.showAlert('Please enter a SQL query', 'warning');
            return;
        }

        const resultsContainer = document.getElementById('queryResults');
        resultsContainer.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Executing query...</div>';

        fetch('/api/execute_query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: queryText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.displayQueryResults(data.data, data.message);
            } else {
                this.showAlert(data.error || 'Query execution failed', 'danger');
                resultsContainer.innerHTML = `<div class="text-danger">Error: ${data.error}</div>`;
            }
        })
        .catch(error => {
            this.showAlert('Network error occurred', 'danger');
            resultsContainer.innerHTML = `<div class="text-danger">Network Error: ${error}</div>`;
        });
    }

    displayQueryResults(data, message) {
        const resultsContainer = document.getElementById('queryResults');
        
        if (!data || data.length === 0) {
            resultsContainer.innerHTML = `
                <div class="results-info">
                    <span><i class="fas fa-info-circle me-2"></i>${message || 'Query executed successfully with no results.'}</span>
                </div>
            `;
            return;
        }

        // Results info bar
        let html = `
            <div class="results-info">
                <div>
                    <i class="fas fa-check-circle me-2 text-success"></i>
                    <span class="row-count">${data.length}</span> row(s) returned
                </div>
                <div class="export-options">
                    <button class="btn btn-outline-secondary btn-sm" onclick="app.exportToCSV()" title="Export to CSV">
                        <i class="fas fa-download"></i> CSV
                    </button>
                </div>
            </div>
        `;

        // Create compact table
        html += `
            <div class="query-results">
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
        `;

        // Table headers
        const headers = Object.keys(data[0]);
        headers.forEach(header => {
            html += `<th>${header}</th>`;
        });
        html += '</tr></thead><tbody>';

        // Table rows with compact data
        data.forEach((row, rowIndex) => {
            html += '<tr>';
            headers.forEach(header => {
                const value = row[header];
                let displayValue = '';
                
                if (value === null || value === undefined) {
                    displayValue = '<span class="text-muted font-italic">NULL</span>';
                } else {
                    const strValue = String(value);
                    if (strValue.length > 50) {
                        displayValue = `<span class="expandable" onclick="app.toggleCellExpansion(this)" title="Click to expand">${strValue.substring(0, 47)}</span>`;
                    } else {
                        displayValue = strValue;
                    }
                }
                
                html += `<td data-full-value="${value}">${displayValue}</td>`;
            });
            html += '</tr>';
        });

        html += '</tbody></table></div></div>';
        resultsContainer.innerHTML = html;
        
        // Store data for export
        this.currentResultData = data;
    }

    toggleCellExpansion(element) {
        const cell = element.parentElement;
        const fullValue = cell.getAttribute('data-full-value');
        
        if (element.classList.contains('expanded')) {
            // Collapse
            element.classList.remove('expanded');
            element.innerHTML = fullValue.substring(0, 47);
            cell.classList.remove('expanded');
        } else {
            // Expand
            element.classList.add('expanded');
            element.innerHTML = fullValue;
            cell.classList.add('expanded');
        }
    }

    exportToCSV() {
        if (!this.currentResultData || this.currentResultData.length === 0) {
            alert('No data to export');
            return;
        }

        const headers = Object.keys(this.currentResultData[0]);
        let csvContent = headers.join(',') + '\n';

        this.currentResultData.forEach(row => {
            const values = headers.map(header => {
                const value = row[header];
                if (value === null || value === undefined) return '';
                // Escape commas and quotes for CSV
                const strValue = String(value);
                if (strValue.includes(',') || strValue.includes('"') || strValue.includes('\n')) {
                    return '"' + strValue.replace(/"/g, '""') + '"';
                }
                return strValue;
            });
            csvContent += values.join(',') + '\n';
        });

        // Download CSV file
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `query_results_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    checkConnectionStatus() {
        fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            if (!data.connected) {
                this.showAlert('Connection lost. Please reconnect.', 'warning');
                setTimeout(() => {
                    window.location.href = '/';
                }, 3000);
            }
        })
        .catch(() => {
            // Ignore errors for status check
        });
    }

    showAlert(message, type = 'info') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
        alertContainer.innerHTML = `
            <i class="fas fa-${type === 'danger' ? 'exclamation-triangle' : type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertContainer, container.firstChild);
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                alertContainer.remove();
            }, 5000);
        }
    }

    // Utility methods
    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.mysqlSSHUI = new MySQLSSHUI();
    // Create global app alias for easier access
    window.app = window.mysqlSSHUI;
});

// Global utility functions
window.loadDatabases = function() {
    window.mysqlSSHUI.loadDatabases();
};

window.loadTables = function() {
    window.mysqlSSHUI.loadTables();
};
