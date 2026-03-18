<style>
/* Clean Technical Theme - Tailwind Inspired */
* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', system-ui, sans-serif;
    line-height: 1.6;
    color: #291f1e;
    background: #fffbf0;
    margin: 0;
    padding: 24px;
    font-size: 16px;
}

.container {
    max-width: 896px;
    margin: 0 auto;
    background: white;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(41, 31, 30, 0.25);
    overflow: hidden;
}

.content {
    padding: 48px;
}

h1 {
    font-size: 2.25rem;
    font-weight: 800;
    color: #477998;
    margin: 0 0 12px 0;
    line-height: 1.1;
    letter-spacing: -0.025em;
}

h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #291f1e;
    margin: 48px 0 16px 0;
}

h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #477998;
    margin: 32px 0 12px 0;
}

p {
    margin: 16px 0;
    color: #44403c;
}

ul, ol {
    margin: 16px 0;
    padding-left: 24px;
}

li {
    margin: 8px 0;
}

code {
    background: #fef3c7;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 0.9em;
    color: #92400e;
}

pre {
    background: #1e293b;
    color: #e2e8f0;
    padding: 20px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 24px 0;
}

pre code {
    background: none;
    padding: 0;
    color: inherit;
    font-size: 0.875rem;
}

.mermaid {
    background: #f8fafc;
    padding: 24px;
    border-radius: 8px;
    margin: 32px 0;
    border: 1px solid #e2e8f0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
}

th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
}

th {
    background: #f8fafc;
    font-weight: 600;
    color: #477998;
}

.meta {
    color: #78716c;
    font-size: 0.875rem;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 2px solid #e7e5e4;
}

.highlight {
    background: #dbeafe;
    border-left: 4px solid #3b82f6;
    padding: 16px 20px;
    margin: 24px 0;
    border-radius: 4px;
}
</style>

<html>
<div class="container">
    <div class="content">
        <h1>Server Networking Overview - Current State</h1>
        <div class="meta">
            Gabriel Penman • December 30, 2025
        </div>

        <p>With multiple projects running simultaneously on my development server, the networking landscape has grown more complex. This post documents the current state of all running services, their port allocations, and how they interconnect. This is primarily for my own reference as I consider improving the reverse proxy architecture.</p>

        <h2>Architecture Overview</h2>

        <p>The server currently runs a mix of different application types:</p>
        <ul>
            <li><strong>Web Applications</strong>: Two main sites (production Flask blog and development Next.js app)</li>
            <li><strong>Microservices</strong>: Docker Swarm-based arbitrage trading system</li>
            <li><strong>Development Tools</strong>: Firebase emulators for local development</li>
            <li><strong>Database Services</strong>: MongoDB, MySQL with phpMyAdmin</li>
            <li><strong>Gaming</strong>: Minecraft server</li>
            <li><strong>Infrastructure</strong>: Nginx reverse proxy, FTP, custom SSH port</li>
        </ul>

        <h2>Network Architecture Diagram</h2>

        <div class="mermaid">
graph TB
    subgraph Internet["External Traffic"]
        User[User Browser]
        SSH_Client[SSH Client]
        MC_Client[Minecraft Client]
        FTP_Client[FTP Client]
    end

    subgraph Nginx["Nginx Reverse Proxy :80/:443"]
        NginxCore[Nginx Core]
    end

    subgraph WebApps["Web Applications"]
        Flask[Flask Blog :5000]
        NextJS[Next.js geo-butler :3000]
    end

    subgraph Firebase["Firebase Emulators"]
        FB_UI[Firebase UI :4000]
        FB_Functions[Functions :5001]
        FB_Hosting[Hosting :5002]
        FB_Firestore[Firestore :8081]
        FB_Auth[Auth :9099]
    end

    subgraph Arbitrage["Arbitrage Microservices - Docker Swarm"]
        ARB_Web[Webapp :3005]
        ARB_Pool[Pool :7500]
        ARB_Registry[Registry :7503]
        ARB_Config[Config :7504]
        ARB_Telegram[Telegram :7505]
        ARB_Network[Network :8888-8889]
    end

    subgraph Databases["Database Services"]
        MongoDB[MongoDB :27017]
        MySQL[MySQL :3306]
        phpMyAdmin[phpMyAdmin :8080]
    end

    subgraph Other["Other Services"]
        Minecraft[Minecraft Server :25565]
        BlueMap[BlueMap :8100]
        Depopper[Depopper Research :5123]
        SSH[SSH :2222]
        FTP[FTP :21]
    end

    User -->|HTTPS :443| NginxCore
    User -->|HTTP :80| NginxCore
    NginxCore -->|/api/*| Flask
    NginxCore -->|static files| Flask
    NginxCore -->|/dev/3000| NextJS
    NginxCore -->|/dev/3005| ARB_Web
    NginxCore -->|/dev/4000, /dev/5001, etc| Firebase
    NginxCore -->|/dev/8100| BlueMap
    NginxCore -->|/dev/5123| Depopper

    NextJS --> FB_Functions
    NextJS --> FB_Firestore
    NextJS --> FB_Auth

    ARB_Web --> ARB_Pool
    ARB_Web --> ARB_Registry
    ARB_Registry --> ARB_Config
    ARB_Telegram --> ARB_Registry
    ARB_Pool --> MongoDB
    ARB_Registry --> MongoDB

    BlueMap --> Minecraft

    phpMyAdmin --> MySQL

    SSH_Client -->|Port 2222| SSH
    MC_Client -->|Port 25565| Minecraft
    FTP_Client -->|Port 21| FTP

    style NginxCore fill:#3b82f6,color:#fff
    style Flask fill:#22c55e,color:#fff
    style NextJS fill:#06b6d4,color:#fff
    style MongoDB fill:#10b981,color:#fff
    style Minecraft fill:#f59e0b,color:#fff
        </div>

        <h2>Service Inventory</h2>

        <h3>Web Serving Layer</h3>

        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Port</th>
                    <th>Purpose</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Nginx</strong></td>
                    <td>80, 443</td>
                    <td>Reverse proxy for gabrielpenman.com with SSL termination</td>
                    <td>Running (systemd)</td>
                </tr>
                <tr>
                    <td><strong>Flask Blog</strong></td>
                    <td>5000</td>
                    <td>Production blog backend (<code>blog-server.service</code>)</td>
                    <td>Running (systemd)</td>
                </tr>
                <tr>
                    <td><strong>Next.js geo-butler</strong></td>
                    <td>3000</td>
                    <td>Development/experimental SEO tool (<code>geo-butler-dev.service</code>)</td>
                    <td>Running (systemd)</td>
                </tr>
            </tbody>
        </table>

        <h3>Firebase Development Emulators</h3>

        <p>Running as part of the geo-butler development environment:</p>

        <table>
            <thead>
                <tr>
                    <th>Emulator</th>
                    <th>Port</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Firebase UI</strong></td>
                    <td>4000</td>
                    <td>Web interface for emulator suite</td>
                </tr>
                <tr>
                    <td><strong>Cloud Functions</strong></td>
                    <td>5001</td>
                    <td>Serverless function emulation</td>
                </tr>
                <tr>
                    <td><strong>Hosting</strong></td>
                    <td>5002</td>
                    <td>Firebase hosting emulation</td>
                </tr>
                <tr>
                    <td><strong>Firestore</strong></td>
                    <td>8081</td>
                    <td>NoSQL database emulation</td>
                </tr>
                <tr>
                    <td><strong>Authentication</strong></td>
                    <td>9099</td>
                    <td>Auth service emulation</td>
                </tr>
            </tbody>
        </table>

        <h3>Arbitrage Trading Microservices</h3>

        <p>Docker Swarm-based microservice architecture for cryptocurrency arbitrage:</p>

        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Port</th>
                    <th>Container</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Webapp</strong></td>
                    <td>3005</td>
                    <td>arbitrage_webapp</td>
                    <td>Web interface</td>
                </tr>
                <tr>
                    <td><strong>Pool</strong></td>
                    <td>7500</td>
                    <td>arbitrage_pool</td>
                    <td>Liquidity pool monitoring</td>
                </tr>
                <tr>
                    <td><strong>Registry</strong></td>
                    <td>7503</td>
                    <td>arbitrage_registry</td>
                    <td>Service registry and discovery</td>
                </tr>
                <tr>
                    <td><strong>Config</strong></td>
                    <td>7504</td>
                    <td>arbitrage_config</td>
                    <td>Configuration management</td>
                </tr>
                <tr>
                    <td><strong>Telegram</strong></td>
                    <td>7505</td>
                    <td>arbitrage_telegram</td>
                    <td>Telegram bot integration</td>
                </tr>
                <tr>
                    <td><strong>Network</strong></td>
                    <td>8888-8889</td>
                    <td>arbitrage_network</td>
                    <td>Network monitoring</td>
                </tr>
            </tbody>
        </table>

        <h3>Database Services</h3>

        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Port</th>
                    <th>Purpose</th>
                    <th>Access</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>MongoDB</strong></td>
                    <td>27017</td>
                    <td>Primary database for arbitrage services</td>
                    <td>Docker container (mongo:7.0)</td>
                </tr>
                <tr>
                    <td><strong>MySQL</strong></td>
                    <td>3306</td>
                    <td>WordPress database</td>
                    <td>Docker container (internal)</td>
                </tr>
                <tr>
                    <td><strong>phpMyAdmin</strong></td>
                    <td>8080</td>
                    <td>MySQL admin interface</td>
                    <td>http://localhost:8080</td>
                </tr>
            </tbody>
        </table>

        <h3>Other Services</h3>

        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Port</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Minecraft Server</strong></td>
                    <td>25565</td>
                    <td>Multiplayer gaming server (Java edition)</td>
                </tr>
                <tr>
                    <td><strong>BlueMap (Dynmap)</strong></td>
                    <td>8100</td>
                    <td>Live Minecraft world map renderer</td>
                </tr>
                <tr>
                    <td><strong>Depopper Research</strong></td>
                    <td>5123</td>
                    <td>Experimental image processing pipeline playground</td>
                </tr>
                <tr>
                    <td><strong>SSH</strong></td>
                    <td>2222</td>
                    <td>Secure shell access (custom port)</td>
                </tr>
                <tr>
                    <td><strong>FTP</strong></td>
                    <td>21</td>
                    <td>File transfer protocol</td>
                </tr>
                <tr>
                    <td><strong>DNS</strong></td>
                    <td>53</td>
                    <td>Local DNS resolution (systemd-resolved)</td>
                </tr>
            </tbody>
        </table>

        <h3>Nginx Reverse Proxy Routes</h3>

        <p>Many services are exposed through Nginx using <code>/dev/*</code> paths, allowing web access to internal services without direct port exposure:</p>

        <table>
            <thead>
                <tr>
                    <th>Public Path</th>
                    <th>Proxies To</th>
                    <th>Service</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>/dev/3000</code></td>
                    <td>localhost:3000</td>
                    <td>Next.js geo-butler development site</td>
                </tr>
                <tr>
                    <td><code>/dev/3005</code></td>
                    <td>localhost:3005</td>
                    <td>Arbitrage webapp dashboard</td>
                </tr>
                <tr>
                    <td><code>/dev/4000</code></td>
                    <td>localhost:4000</td>
                    <td>Firebase Emulator UI</td>
                </tr>
                <tr>
                    <td><code>/dev/5001</code></td>
                    <td>localhost:5001</td>
                    <td>Firebase Cloud Functions</td>
                </tr>
                <tr>
                    <td><code>/dev/5123</code></td>
                    <td>localhost:5123</td>
                    <td>Depopper research playground</td>
                </tr>
                <tr>
                    <td><code>/dev/8081</code></td>
                    <td>localhost:8081</td>
                    <td>Firebase Firestore emulator</td>
                </tr>
                <tr>
                    <td><code>/dev/8100</code></td>
                    <td>[::1]:8100</td>
                    <td>BlueMap (Minecraft live map)</td>
                </tr>
                <tr>
                    <td><code>/dev/9099</code></td>
                    <td>localhost:9099</td>
                    <td>Firebase Authentication emulator</td>
                </tr>
                <tr>
                    <td><code>/dev/api/</code></td>
                    <td>localhost:3005/api/</td>
                    <td>Arbitrage API endpoints</td>
                </tr>
            </tbody>
        </table>

        <p>This pattern allows accessing services like <code>https://gabrielpenman.com/dev/3005</code> instead of opening additional firewall ports.</p>

        <h2>Traffic Flow Patterns</h2>

        <h3>Public Web Traffic (gabrielpenman.com)</h3>
        <ol>
            <li>HTTPS requests hit Nginx on port 443</li>
            <li>Nginx routes <code>/api/*</code> paths to Flask backend (port 5000)</li>
            <li>Static content served from <code>/home/gabriel/blog-new/output/</code></li>
            <li><code>/dev/*</code> paths proxy to internal services:
                <ul>
                    <li><code>/dev/3000</code> → Next.js geo-butler</li>
                    <li><code>/dev/3005</code> → Arbitrage webapp</li>
                    <li><code>/dev/4000, 5001, 8081, 9099</code> → Firebase emulators</li>
                    <li><code>/dev/8100</code> → BlueMap (Minecraft map)</li>
                    <li><code>/dev/5123</code> → Depopper research playground</li>
                </ul>
            </li>
        </ol>

        <h3>Arbitrage System Communication</h3>
        <ol>
            <li>All services run in Docker Swarm for orchestration</li>
            <li>Internal service discovery via the registry service (port 7503)</li>
            <li>Configuration pulled from config service (port 7504)</li>
            <li>Pool and registry services share MongoDB on port 27017</li>
            <li>Telegram bot provides external notifications</li>
            <li>Web dashboard accessible via <code>/dev/3005</code> proxy path</li>
        </ol>

        <h3>Development Workflow</h3>
        <ol>
            <li>Next.js dev server runs on port 3000, accessible via <code>/dev/3000</code></li>
            <li>Firebase emulators provide backend services locally (all proxied via <code>/dev/*</code>)</li>
            <li>No need to deploy to Firebase for testing</li>
            <li>Auth, Firestore, Functions all emulated locally and web-accessible</li>
        </ol>

        <h3>Gaming & Visualization</h3>
        <ol>
            <li>Minecraft server listens on port 25565 for game clients</li>
            <li>BlueMap plugin generates live world map on port 8100</li>
            <li>Map accessible via web at <code>/dev/8100</code></li>
        </ol>

        <h2>Current Issues & Observations</h2>

        <div class="highlight">
            <strong>Note:</strong> These are observations about the current state, not recommendations for changes yet.
        </div>

        <ul>
            <li><strong>Port sprawl</strong>: 20+ ports in active use across the server</li>
            <li><strong>Mixed orchestration</strong>: Systemd services alongside Docker Swarm</li>
            <li><strong>Microservice exposure</strong>: Arbitrage microservices still use raw ports instead of <code>/dev/*</code> proxying</li>
            <li><strong>Documentation lag</strong>: Hard to track what's running without port scanning</li>
            <li><strong>Docker proxy duplication</strong>: Both standalone and Swarm MongoDB instances</li>
            <li><strong>Dev path proliferation</strong>: 10+ different <code>/dev/*</code> proxy endpoints to manage</li>
        </ul>

        <h2>Port Allocation Summary</h2>

        <pre><code>Web Serving:        80, 443, 3000, 5000
Firebase Emulators: 4000, 5001, 5002, 8081, 9099
Arbitrage Services: 3005, 7500, 7503-7505, 8888-8889
Databases:          3306, 8080, 27017
Gaming:             25565, 8100 (Minecraft + BlueMap)
Research:           5123 (Depopper playground)
Infrastructure:     21, 53, 2222
Docker Swarm:       2377, 7946

Proxied via Nginx:  3000, 3005, 4000, 5001, 5123, 8081, 8100, 9099
Direct Access Only: 7500, 7503-7505, 8888-8889 (microservices)</code></pre>

        <h2>Next Steps</h2>

        <p>This documentation serves as a baseline for future improvements. Potential areas to explore:</p>
        <ul>
            <li>Consolidating more services behind Nginx reverse proxy</li>
            <li>Standardizing on Docker Compose or Swarm for all services</li>
            <li>Implementing proper service discovery</li>
            <li>Adding monitoring and health checks</li>
            <li>Documenting API endpoints and inter-service communication</li>
        </ul>

        <p>For now, this gives me a clear picture of what's running where, which is exactly what I needed.</p>
    </div>
</div>

<script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({
        startOnLoad: true,
        theme: 'default',
        flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            curve: 'basis'
        }
    });
</script>
</html>
