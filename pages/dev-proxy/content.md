<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #f5f5f5;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    border-radius: 8px;
    padding: 40px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

h1 {
    font-size: 28px;
    margin: 0 0 8px 0;
    color: #333;
}

.subtitle {
    color: #666;
    font-size: 14px;
    margin-bottom: 32px;
}

.ports-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
}

.port-link {
    display: block;
    padding: 16px;
    background: #f0f0f0;
    border-radius: 6px;
    text-decoration: none;
    color: #333;
    border: 2px solid transparent;
    transition: all 0.2s ease;
    text-align: center;
}

.port-link:hover {
    background: #e0e0e0;
    border-color: #0066cc;
    transform: translateY(-2px);
}

.port-number {
    font-size: 24px;
    font-weight: bold;
    color: #0066cc;
    margin-bottom: 4px;
    font-family: 'Monaco', monospace;
}

.port-name {
    font-size: 13px;
    color: #666;
}

.controls-section {
    margin-top: 40px;
    padding-top: 32px;
    border-top: 2px solid #e0e0e0;
}

.controls-section h2 {
    margin: 0 0 16px 0;
    font-size: 18px;
    color: #333;
}

.control-buttons {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}

.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-restart {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
    color: white;
}

.btn-restart:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
}

.btn-status {
    background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
    color: white;
}

.btn-status:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

.status-box {
    background: #f9f9f9;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    padding: 16px;
    margin-top: 12px;
}

.status-healthy {
    border-color: #51cf66;
    background: #f0fdf4;
}

.status-unhealthy {
    border-color: #ff6b6b;
    background: #fef2f2;
}

.status-message {
    margin: 8px 0 0 0;
    font-size: 13px;
    line-height: 1.5;
}

.status-list {
    margin: 12px 0 0 0;
    list-style: none;
    padding: 0;
}

.status-item {
    display: flex;
    align-items: center;
    padding: 6px 0;
    font-size: 13px;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 8px;
}

.status-dot.running {
    background: #51cf66;
}

.status-dot.offline {
    background: #ff6b6b;
}

.loading-spinner {
    display: inline-block;
    width: 14px;
    height: 14px;
    border: 2px solid #f0f0f0;
    border-top: 2px solid #0066cc;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.handy-urls-section {
    margin-top: 40px;
    padding-top: 32px;
    border-top: 2px solid #e0e0e0;
}

.handy-urls-section h2 {
    margin: 0 0 16px 0;
    font-size: 18px;
    color: #333;
}

.urls-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 12px;
}

.url-link {
    display: block;
    padding: 16px;
    background: #f0f0f0;
    border-radius: 6px;
    text-decoration: none;
    color: #333;
    border: 2px solid transparent;
    transition: all 0.2s ease;
    word-break: break-all;
    font-size: 13px;
}

.url-link:hover {
    background: #e0e0e0;
    border-color: #0066cc;
    transform: translateY(-2px);
}

.url-label {
    font-weight: 600;
    color: #0066cc;
    margin-bottom: 6px;
    font-size: 12px;
    text-transform: uppercase;
}
</style>

<html>
<div class="container">
    <h1>Dev Proxy Ports</h1>
    <p class="subtitle">Click any port below to access the service</p>

    <div class="ports-grid">
        <a href="/dev/3000" class="port-link">
            <div class="port-number">3000</div>
            <div class="port-name">Next.js</div>
        </a>
        <a href="/dev/3001" class="port-link">
            <div class="port-number">3001</div>
            <div class="port-name">Next.js (Alt)</div>
        </a>
        <a href="/dev/3002" class="port-link">
            <div class="port-number">3002</div>
            <div class="port-name">Next.js (Alt 2)</div>
        </a>
        <a href="/dev/4000" class="port-link">
            <div class="port-number">4000</div>
            <div class="port-name">Firebase UI</div>
        </a>
        <a href="/dev/5001" class="port-link">
            <div class="port-number">5001</div>
            <div class="port-name">Functions</div>
        </a>
        <a href="/dev/8081" class="port-link">
            <div class="port-number">8081</div>
            <div class="port-name">Firestore</div>
        </a>
        <a href="/dev/8085" class="port-link">
            <div class="port-number">8085</div>
            <div class="port-name">Pub/Sub</div>
        </a>
        <a href="/dev/9099" class="port-link">
            <div class="port-number">9099</div>
            <div class="port-name">Auth</div>
        </a>
    </div>

    <div class="controls-section">
        <h2>Dev Services Control</h2>
        <div class="control-buttons">
            <button class="btn btn-status" onclick="checkServicesStatus()" id="statusBtn">Check Status</button>
            <button class="btn btn-restart" onclick="restartServices()" id="restartBtn">Restart Services</button>
        </div>
        <div id="statusContainer"></div>
    </div>

    <div class="handy-urls-section">
        <h2>Temp Handy URLs</h2>
        <div class="urls-grid">
            <a href="https://gabrielpenman.com/dev/3000/schema-test" class="url-link" target="_blank">
                <div class="url-label">Schema Test</div>
                <div>https://gabrielpenman.com/dev/3000/schema-test</div>
            </a>
            <a href="https://gabrielpenman.com/dev/3000/example-seven" class="url-link" target="_blank">
                <div class="url-label">Example Seven</div>
                <div>https://gabrielpenman.com/dev/3000/example-seven</div>
            </a>
        </div>
    </div>
</div>

<script>
const API_TOKEN = 'dev-restart-token';

async function checkServicesStatus() {
    const btn = document.getElementById('statusBtn');
    const container = document.getElementById('statusContainer');

    btn.disabled = true;
    container.innerHTML = '<div class="status-box"><div class="loading-spinner"></div> Checking services...</div>';

    try {
        const response = await fetch('/api/dev/services-status');
        const data = await response.json();

        const isHealthy = data.all_healthy;
        const statusHtml = `
            <div class="status-box ${isHealthy ? 'status-healthy' : 'status-unhealthy'}">
                <strong>${isHealthy ? 'All Services Healthy' : 'Some Services Down'}</strong>
                <ul class="status-list">
                    ${Object.entries(data.services).map(([name, info]) => `
                        <li class="status-item">
                            <span class="status-dot ${info.running ? 'running' : 'offline'}"></span>
                            <strong>${name.replace(/_/g, ' ')}:</strong>
                            ${info.running ? `<a href="http://localhost:${info.port}" target="_blank" style="color: #0066cc; text-decoration: none;">port ${info.port}</a>` : `port ${info.port} (offline)`}
                        </li>
                    `).join('')}
                </ul>
                <div class="status-message">Last checked: ${new Date(data.timestamp).toLocaleTimeString()}</div>
            </div>
        `;
        container.innerHTML = statusHtml;
    } catch (error) {
        container.innerHTML = `<div class="status-box status-unhealthy"><strong>Error</strong><p class="status-message">${error.message}</p></div>`;
    } finally {
        btn.disabled = false;
    }
}

async function restartServices() {
    const btn = document.getElementById('restartBtn');
    const container = document.getElementById('statusContainer');

    const confirmed = confirm('Are you sure you want to restart all dev services?\n\nThis will interrupt:\n- Firebase Emulators\n- Next.js Dev Server\n\nYou\'ll have ~5-10 seconds of downtime.');

    if (!confirmed) return;

    btn.disabled = true;
    container.innerHTML = '<div class="status-box"><div class="loading-spinner"></div> Restarting services...</div>';

    try {
        const response = await fetch('/api/dev/restart-services', {
            method: 'POST',
            headers: {
                'X-Admin-Token': API_TOKEN,
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (response.ok && data.success) {
            container.innerHTML = `
                <div class="status-box status-healthy">
                    <strong>Restart Initiated</strong>
                    <p class="status-message">${data.message}</p>
                    <p class="status-message">${data.details}</p>
                    <p class="status-message"><em>Services should be back online in ~5-10 seconds.</em></p>
                </div>
            `;

            // Auto-check status after 10 seconds
            setTimeout(() => {
                checkServicesStatus();
            }, 10000);
        } else {
            container.innerHTML = `
                <div class="status-box status-unhealthy">
                    <strong>Restart Failed</strong>
                    <p class="status-message">${data.error || 'Unknown error'}</p>
                    <p class="status-message">${data.message || data.details || ''}</p>
                </div>
            `;
        }
    } catch (error) {
        container.innerHTML = `
            <div class="status-box status-unhealthy">
                <strong>Error</strong>
                <p class="status-message">${error.message}</p>
            </div>
        `;
    } finally {
        btn.disabled = false;
    }
}

// Auto-check status on page load
document.addEventListener('DOMContentLoaded', checkServicesStatus);
</script>

</html>
