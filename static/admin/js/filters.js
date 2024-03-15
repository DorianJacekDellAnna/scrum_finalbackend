/**
 * Persist changelist filters state (collapsed/expanded).
 */
'use strict';

// Retrieve filters state from sessionStorage
let filters = JSON.parse(sessionStorage.getItem('django.admin.filtersState')) || {};

// Initialize filter states based on sessionStorage data
Object.entries(filters).forEach(([key, value]) => {
    const detailElement = document.querySelector(`[data-filter-title='${CSS.escape(key)}']`);
    if (detailElement) {
        value ? detailElement.setAttribute('open', '') : detailElement.removeAttribute('open');
    }
});

// Save filter state when clicks
document.querySelectorAll('details').forEach(detail => {
    detail.addEventListener('toggle', event => {
        filters[`${event.target.dataset.filterTitle}`] = detail.open;
        sessionStorage.setItem('django.admin.filtersState', JSON.stringify(filters));
    });
});
