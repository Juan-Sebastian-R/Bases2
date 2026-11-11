/* ============================================================
   Professional Network Graph Database — App JavaScript
   ============================================================ */

// -------------------- Toast Notification System --------------------

/**
 * Create the toast container element if it doesn't exist.
 * @returns {HTMLElement} The toast container.
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    container.setAttribute('aria-live', 'polite');
    container.setAttribute('aria-atomic', 'true');
    document.body.appendChild(container);
    return container;
}

/**
 * Show a toast notification.
 * @param {string} message - The message to display.
 * @param {string} type - One of 'success', 'error', 'warning', 'info'.
 */
function showToast(message, type = 'success') {
    const container = document.querySelector('.toast-container') || createToastContainer();

    const colors = {
        success: { bg: '#198754', icon: 'fas fa-check-circle',  label: 'Éxito' },
        error:   { bg: '#dc3545', icon: 'fas fa-times-circle',  label: 'Error' },
        warning: { bg: '#ffc107', icon: 'fas fa-exclamation-triangle', label: 'Advertencia', textColor: '#1a1a2e' },
        info:    { bg: '#0dcaf0', icon: 'fas fa-info-circle',   label: 'Info',  textColor: '#1a1a2e' }
    };

    const cfg = colors[type] || colors.success;
    const textColor = cfg.textColor || '#ffffff';
    const id = 'toast-' + Date.now();

    const toastEl = document.createElement('div');
    toastEl.id = id;
    toastEl.className = 'toast fade-in';
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    toastEl.style.cssText = `background:${cfg.bg}; color:${textColor}; margin-bottom:0.5rem;`;

    toastEl.innerHTML = `
        <div class="toast-body d-flex align-items-center justify-content-between py-2 px-3">
            <span><i class="${cfg.icon} me-2"></i>${escapeHtml(message)}</span>
            <button type="button" class="btn-close btn-close-white ms-3" aria-label="Close" onclick="this.closest('.toast').remove()"></button>
        </div>
    `;

    container.appendChild(toastEl);

    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        if (toastEl.parentNode) {
            toastEl.style.opacity = '0';
            toastEl.style.transition = 'opacity 0.3s ease';
            setTimeout(() => toastEl.remove(), 300);
        }
    }, 3000);
}

// -------------------- API Helper Functions --------------------

/**
 * Generic API call with error handling.
 * @param {string} url - The endpoint URL.
 * @param {string} method - HTTP method.
 * @param {object|null} data - Request body (ignored for GET).
 * @returns {Promise<any>} Parsed JSON response.
 */
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };

    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Error en la operación');
        }

        return result;
    } catch (error) {
        showToast(error.message, 'error');
        throw error;
    }
}

/** GET helper. */
async function apiGet(url) {
    return apiCall(url, 'GET');
}

/** POST helper. */
async function apiPost(url, data) {
    return apiCall(url, 'POST', data);
}

/** PUT helper. */
async function apiPut(url, data) {
    return apiCall(url, 'PUT', data);
}

/** DELETE helper. */
async function apiDelete(url, data = null) {
    return apiCall(url, 'DELETE', data);
}

// -------------------- UI Utilities --------------------

/**
 * Show a confirmation dialog.
 * @param {string} message - Confirmation prompt text.
 * @returns {boolean} True if the user confirmed.
 */
function confirmAction(message) {
    return confirm(message);
}

/**
 * Display a loading spinner inside a container element.
 * @param {string} containerId - The id of the container element.
 */
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner-border text-light" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2 text-muted">Cargando datos...</p>
            </div>`;
    }
}

/**
 * Clear a loading spinner and optionally set content.
 * @param {string} containerId - The id of the container element.
 * @param {string} [html=''] - HTML to set after clearing.
 */
function hideLoading(containerId, html = '') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = html;
    }
}

/**
 * Show an empty-state message inside a container.
 * @param {string} containerId - Container element id.
 * @param {string} message - Message to display.
 * @param {string} icon - Font Awesome icon class.
 */
function showEmptyState(containerId, message, icon = 'fas fa-inbox') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="${escapeHtml(icon)}"></i>
                <p>${escapeHtml(message)}</p>
            </div>`;
    }
}

// -------------------- Formatting Helpers --------------------

/**
 * Format an ISO date string as a locale-friendly date.
 * @param {string} dateStr - ISO date string.
 * @returns {string} Formatted date or 'N/A'.
 */
function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleDateString('es-CO');
}

/**
 * Format a number with thousands separators.
 * @param {number} num - The number to format.
 * @returns {string} Formatted number string.
 */
function formatNumber(num) {
    if (num == null) return '0';
    return Number(num).toLocaleString('es-CO');
}

// -------------------- Badge HTML Generators --------------------

/**
 * Generate a coloured badge for a node type.
 * @param {string} type - Node type (usuario, empresa, habilidad, proyecto, oferta).
 * @param {string} text - Badge label.
 * @returns {string} Badge HTML string.
 */
function nodeBadge(type, text) {
    const classes = {
        'usuario':   'badge-usuario',
        'empresa':   'badge-empresa',
        'habilidad': 'badge-habilidad',
        'proyecto':  'badge-proyecto',
        'oferta':    'badge-oferta'
    };
    return `<span class="badge ${classes[type] || 'bg-secondary'}">${text}</span>`;
}

/**
 * Generate a badge for a job modality.
 * @param {string} modalidad - 'remoto', 'presencial', or 'hibrido'.
 * @returns {string} Badge HTML string.
 */
function modalidadBadge(modalidad) {
    const colors = {
        'remoto':      'success',
        'presencial':  'primary',
        'hibrido':     'warning'
    };
    return `<span class="badge bg-${colors[modalidad] || 'secondary'}">${escapeHtml(modalidad || 'N/A')}</span>`;
}

// -------------------- Security --------------------

/**
 * Escape a string for safe insertion into HTML.
 * @param {string} text - Raw text.
 * @returns {string} HTML-escaped text.
 */
function escapeHtml(text) {
    if (text == null) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}

// -------------------- Path Visualization --------------------

/**
 * Render a sequence of path nodes with arrows between them.
 * @param {Array} pathNodes - Array of node objects with group and label/nombre.
 * @returns {string} HTML string of the path.
 */
function renderPath(pathNodes) {
    if (!pathNodes || pathNodes.length === 0) {
        return '<p class="text-muted">No se encontró ruta</p>';
    }

    return pathNodes.map((node, i) => {
        const badge = nodeBadge(
            (node.group || 'usuario').toLowerCase(),
            escapeHtml(node.label || node.nombre || 'Unknown')
        );
        const arrow = i < pathNodes.length - 1
            ? '<span class="path-arrow"><i class="fas fa-arrow-right"></i></span>'
            : '';
        return `<span class="path-node">${badge}</span>${arrow}`;
    }).join('');
}

// -------------------- Page Initialisation --------------------

document.addEventListener('DOMContentLoaded', () => {
    // Apply fade-in to elements marked as ready
    document.querySelectorAll('.fade-in-ready').forEach(el => {
        el.classList.add('fade-in');
    });

    // Activate Bootstrap tooltips if present
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
});

// -------------------- Graph Configuration (vis.js) --------------------

/**
 * Shared graph configuration for vis.js networks.
 */
const graphConfig = {
    nodeColors: {
        'Usuario':   '#4CAF50',
        'Empresa':   '#2196F3',
        'Habilidad': '#FF9800',
        'Proyecto':  '#9C27B0',
        'Oferta':    '#F44336'
    },

    nodeShapes: {
        'Usuario':   'dot',
        'Empresa':   'diamond',
        'Habilidad': 'triangle',
        'Proyecto':  'square',
        'Oferta':    'star'
    },

    /**
     * Get vis.js node options for a given group.
     * @param {string} group - The node group name.
     * @returns {object} vis.js node options.
     */
    getNodeOptions(group) {
        const color = this.nodeColors[group] || '#666666';
        return {
            color: {
                background: color,
                border: color,
                highlight: { background: '#e94560', border: '#e94560' },
                hover: { background: color, border: '#ffffff' }
            },
            shape: this.nodeShapes[group] || 'dot',
            font: { color: '#ffffff', size: 12 }
        };
    },

    /** Default physics and interaction options for vis.js. */
    physicsOptions: {
        physics: {
            barnesHut: {
                gravitationalConstant: -3000,
                centralGravity: 0.3,
                springLength: 150,
                springConstant: 0.04
            },
            stabilization: { iterations: 150, fit: true }
        },
        interaction: {
            hover: true,
            tooltipDelay: 200,
            navigationButtons: true,
            keyboard: true
        },
        edges: {
            color: { color: '#555555', highlight: '#e94560', hover: '#888888' },
            font: { color: '#a0a0b0', size: 10, strokeWidth: 0 },
            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
            smooth: { type: 'curvedCW', roundness: 0.2 }
        }
    }
};

// -------------------- Graph Builder --------------------

/**
 * Build and render a vis.js network graph from API data.
 * @param {HTMLElement} containerElement - DOM element for the graph.
 * @param {object} graphData - Object with nodes[] and edges[] arrays.
 * @param {object} [options={}] - Extra vis.js options to merge.
 * @returns {object} { network, nodesDataSet, edgesDataSet }
 */
function buildGraph(containerElement, graphData, options = {}) {
    const nodes = graphData.nodes.map(n => ({
        id: n.id,
        label: n.label,
        group: n.group,
        title: `${n.group}: ${n.label}`,
        ...graphConfig.getNodeOptions(n.group),
        size: options.sizeByConnections
            ? Math.max(15, (n.connections || 1) * 3)
            : 20
    }));

    const edges = graphData.edges.map(e => ({
        from: e.from,
        to: e.to,
        label: e.label || '',
        title: e.label || ''
    }));

    const nodesDataSet = new vis.DataSet(nodes);
    const edgesDataSet = new vis.DataSet(edges);

    const networkOptions = { ...graphConfig.physicsOptions, ...options };
    // Remove custom flags not understood by vis.js
    delete networkOptions.sizeByConnections;

    const network = new vis.Network(
        containerElement,
        { nodes: nodesDataSet, edges: edgesDataSet },
        networkOptions
    );

    // Fire a stabilised event to hide any loading overlay
    network.once('stabilized', () => {
        network.fit({ animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
    });

    return { network, nodesDataSet, edgesDataSet };
}

/**
 * Generate HTML for the graph legend.
 * @returns {string} Legend HTML.
 */
function buildLegendHtml() {
    const items = [
        { label: 'Usuario',   color: graphConfig.nodeColors['Usuario'] },
        { label: 'Empresa',   color: graphConfig.nodeColors['Empresa'] },
        { label: 'Habilidad', color: graphConfig.nodeColors['Habilidad'] },
        { label: 'Proyecto',  color: graphConfig.nodeColors['Proyecto'] },
        { label: 'Oferta',    color: graphConfig.nodeColors['Oferta'] }
    ];

    return items.map(item =>
        `<span class="legend-item">
            <span class="legend-dot" style="background:${item.color}"></span>
            ${item.label}
        </span>`
    ).join('');
}
