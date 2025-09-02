// Crypto Scanner JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    console.log('Crypto RSI & MACD Scanner loaded');
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Form validation
    const scanForm = document.getElementById('scanForm');
    if (scanForm) {
        scanForm.addEventListener('submit', function(e) {
            const symbolsInput = document.getElementById('symbols');
            if (!symbolsInput.value.trim()) {
                e.preventDefault();
                alert('Please enter at least one cryptocurrency symbol');
                symbolsInput.focus();
                return false;
            }
        });
    }
    
    // Symbol input formatting
    const symbolsInput = document.getElementById('symbols');
    if (symbolsInput) {
        symbolsInput.addEventListener('input', function() {
            // Convert to uppercase and clean up formatting
            let value = this.value.replace(/[^a-zA-Z,\s]/g, '');
            value = value.replace(/\s+/g, ''); // Remove spaces
            value = value.replace(/,+/g, ','); // Replace multiple commas with single
            value = value.replace(/^,|,$/g, ''); // Remove leading/trailing commas
            this.value = value.toUpperCase();
        });
        
        // Add popular symbols on click
        const popularSymbols = ['BTC', 'ETH', 'LINK', 'XRP', 'SOL'];
        
        // Create quick select buttons
        const quickSelectContainer = document.createElement('div');
        quickSelectContainer.className = 'mt-2';
        quickSelectContainer.innerHTML = '<small class="text-muted">Quick select: </small>';
        
        popularSymbols.forEach(symbol => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-outline-secondary btn-sm me-1 mb-1';
            btn.textContent = symbol;
            btn.onclick = function() {
                const currentValue = symbolsInput.value;
                if (currentValue && !currentValue.endsWith(',')) {
                    symbolsInput.value += ',';
                }
                if (!currentValue.includes(symbol)) {
                    symbolsInput.value += symbol;
                }
            };
            quickSelectContainer.appendChild(btn);
        });
        
        symbolsInput.parentElement.appendChild(quickSelectContainer);
    }
});

// Utility functions
function formatPrice(price) {
    if (price < 0.01) {
        return price.toFixed(6);
    } else if (price < 1) {
        return price.toFixed(4);
    } else {
        return price.toFixed(2);
    }
}

function getSignalColor(signal) {
    const colors = {
        'Strong Buy': 'success',
        'Buy': 'info',
        'Hold': 'secondary',
        'Sell': 'warning',
        'Strong Sell': 'danger',
        'Bullish': 'success',
        'Bearish': 'danger',
        'Oversold': 'success',
        'Overbought': 'danger',
        'Neutral': 'secondary'
    };
    return colors[signal] || 'secondary';
}

// Auto-refresh functionality
function setupAutoRefresh() {
    const refreshInterval = 300000; // 5 minutes
    
    setInterval(() => {
        const resultsTable = document.querySelector('.table');
        if (resultsTable) {
            console.log('Auto-refreshing data...');
            // Only refresh if there are existing results
            refreshData();
        }
    }, refreshInterval);
}

// Initialize auto-refresh if results are present
if (document.querySelector('.table')) {
    setupAutoRefresh();
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + R for refresh
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        refreshData();
    }
    
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const scanForm = document.getElementById('scanForm');
        if (scanForm) {
            scanForm.submit();
        }
    }
});
