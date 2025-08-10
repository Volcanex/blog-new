<style>
/* Clean Technical Theme - Tailwind Inspired */
* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', system-ui, sans-serif;
    line-height: 1.6;
    color: #291f1e;
    background: #fffbf0; /* floral white */
    margin: 0;
    padding: 24px;
    font-size: 16px;
}

.container {
    max-width: 896px; /* max-w-4xl */
    margin: 0 auto;
    background: white;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(41, 31, 30, 0.25);
    overflow: hidden;
}

.content {
    padding: 48px;
}

/* Typography */
h1 {
    font-size: 2.25rem; /* text-4xl */
    font-weight: 800;
    color: #477998;
    margin: 0 0 12px 0;
    line-height: 1.1;
    letter-spacing: -0.025em;
}

h2 {
    font-size: 1.5rem; /* text-2xl */
    font-weight: 700;
    color: #291f1e;
    margin: 48px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

h3 {
    font-size: 1.125rem; /* text-lg */
    font-weight: 600;
    color: #477998;
    margin: 24px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 6px;
}

p {
    margin-bottom: 20px;
    color: #291f1e;
    leading: 1.7;
}

/* Meta information */
.meta {
    background: #f1d2d5; /* auburn-900 */
    color: #a3333d;
    padding: 16px 20px;
    border-radius: 8px;
    border-left: 4px solid #a3333d;
    margin-bottom: 32px;
    font-weight: 500;
    font-size: 14px;
}

/* Highlights */
.highlight {
    background: #e7eedf; /* tea_green-800 equivalent but using floral white tones */
    color: #291f1e;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 600;
}

/* Architecture Diagram - Simplified */
.architecture-diagram {
    background: #d8e5ed; /* cerulean-900 */
    border: 2px solid #477998;
    border-radius: 12px;
    padding: 32px;
    margin: 40px 0;
}

.diagram-title {
    text-align: center;
    font-size: 1.25rem;
    font-weight: 700;
    color: #477998;
    margin-bottom: 24px;
}

.diagram-flow {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

.diagram-step {
    background: white;
    border: 2px solid #477998;
    border-radius: 8px;
    padding: 16px 20px;
    text-align: center;
    min-width: 120px;
    transition: all 0.2s ease;
}

.diagram-step:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(71, 121, 152, 0.15);
}

.diagram-step-title {
    font-weight: 700;
    color: #291f1e;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0;
}

.diagram-step-desc {
    color: #6496b6; /* cerulean-600 */
    font-size: 12px;
    margin: 4px 0 0 0;
}

.diagram-arrow {
    color: #a3333d;
    font-size: 20px;
    font-weight: bold;
}

/* Feature Grid */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    margin: 32px 0;
}

.feature-card {
    background: white;
    border: 2px solid #d8e5ed; /* cerulean-900 */
    border-radius: 12px;
    padding: 24px;
    transition: all 0.3s ease;
}

.feature-card:hover {
    border-color: #477998;
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(71, 121, 152, 0.15);
}

.feature-card h3 {
    margin-top: 0;
    margin-bottom: 16px;
}

.feature-card ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.feature-card li {
    padding: 6px 0;
    color: #291f1e;
    position: relative;
    padding-left: 16px;
}

.feature-card li:before {
    content: "•";
    color: #477998;
    font-weight: bold;
    position: absolute;
    left: 0;
}

/* Code Blocks */
.code-snippet {
    background: #291f1e;
    color: #d8e5ed; /* cerulean-900 */
    padding: 24px;
    border-radius: 8px;
    font-family: 'JetBrains Mono', 'SF Mono', 'Monaco', 'Cascadia Code', monospace;
    font-size: 14px;
    line-height: 1.5;
    margin: 24px 0;
    overflow-x: auto;
    border: 1px solid #477998;
    white-space: pre-line;
}

code {
    background: #f0f0f0;
    color: #291f1e;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
}

/* Links */
a {
    color: #477998;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s ease;
}

a:hover {
    color: #a3333d;
    text-decoration: underline;
}

/* Repository Link */
.repo-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #477998, #6496b6);
    color: white;
    padding: 16px 24px;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(71, 121, 152, 0.3);
}

.repo-link:hover {
    background: linear-gradient(135deg, #a3333d, #f64740);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(71, 121, 152, 0.4);
    color: white;
    text-decoration: none;
}

/* API Endpoints */
.api-endpoints {
    background: #d8e5ed; /* cerulean-900 */
    border-left: 4px solid #477998;
    border-radius: 0 8px 8px 0;
    padding: 24px;
    margin: 24px 0;
}

.api-endpoints h4 {
    color: #477998;
    margin: 0 0 16px 0;
    font-weight: 600;
}

.endpoint-list {
    list-style: none;
    padding: 0;
    margin: 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
}

.endpoint-list li {
    background: white;
    border: 1px solid #b1cbda; /* cerulean-800 */
    border-radius: 6px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #291f1e;
}

.endpoint-list strong {
    color: #477998;
    font-weight: 700;
}

/* Icons */
svg {
    width: 20px;
    height: 20px;
    stroke: currentColor;
    stroke-width: 2;
    fill: none;
}

h2 svg {
    width: 24px;
    height: 24px;
    color: #477998;
}

h3 svg {
    width: 18px;
    height: 18px;
    color: #477998;
}

.repo-link svg {
    width: 20px;
    height: 20px;
    color: white;
}

/* Lists */
ul {
    padding-left: 24px;
}

ul li {
    margin-bottom: 8px;
    color: #291f1e;
}

/* Responsive */
@media (max-width: 768px) {
    body {
        padding: 16px;
    }
    
    .content {
        padding: 32px 24px;
    }
    
    h1 {
        font-size: 1.875rem; /* text-3xl */
    }
    
    .diagram-flow {
        flex-direction: column;
        gap: 12px;
    }
    
    .diagram-arrow {
        transform: rotate(90deg);
    }
    
    .feature-grid {
        grid-template-columns: 1fr;
    }
}
</style>

<html>
<div class="container">
    <div class="content">
        <div class="meta">Published on January 15, 2025 | Categories: architecture, web-development, technical</div>

        <h1>Modular Blog Architecture</h1>

        <p>This blog runs on a modular system where each page is completely self-contained. I built it this way because I wanted the freedom to experiment with different designs and functionality without worrying about breaking other pages.</p>

        <h2>
            <svg viewBox="0 0 24 24"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h2"/><path d="M20 10h-2v2h2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2h-2"/></svg>
            Why Modular?
        </h2>

        <p>After working with AI for a few years, I've noticed that things designed to help human developers often slow down AI. Reusable components and frameworks create complex coupling. Ask an AI to design a blog and it'll probably direct you towards some bloated CMS like WordPress. Using AI to write code like a human is inefficient - it doesn't know what design patterns actually suit it best since it's trained on human-built data.</p>

        <p>This system runs on an e2-micro instance on GCP. I have Claude Code running in a tmux session that I can easily jump in and out of. It loads up the small amount of information it needs from a system prompt and can essentially draw a new page with full dynamic functionality in less than a minute.</p>

        <div class="architecture-diagram">
            <div class="diagram-title">Page Architecture</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                <div style="text-align: center;">
                    <h4 style="color: #477998; margin: 0 0 10px 0;">Development</h4>
                    <div class="diagram-step" style="margin: 8px 0;">
                        <div class="diagram-step-title">HTML Blueprint</div>
                        <div class="diagram-step-desc">config.json + content.md</div>
                    </div>
                    <div class="diagram-step" style="margin: 8px 0;">
                        <div class="diagram-step-title">API Blueprint</div>
                        <div class="diagram-step-desc">api.py with Flask routes</div>
                    </div>
                    <div class="diagram-step" style="margin: 8px 0;">
                        <div class="diagram-step-title">Data Namespace</div>
                        <div class="diagram-step-desc">data/page-name/</div>
                    </div>
                </div>
                <div style="text-align: center;">
                    <h4 style="color: #477998; margin: 0 0 10px 0;">Runtime</h4>
                    <div class="diagram-step" style="margin: 8px 0;">
                        <div class="diagram-step-title">Static HTML</div>
                        <div class="diagram-step-desc">Compiled page output</div>
                    </div>
                    <div class="diagram-step" style="margin: 8px 0;">
                        <div class="diagram-step-title">API Endpoints</div>
                        <div class="diagram-step-desc">/api/page-name/*</div>
                    </div>
                    <div class="diagram-step" style="margin: 8px 0;">
                        <div class="diagram-step-title">JSON Storage</div>
                        <div class="diagram-step-desc">Thread-safe file ops</div>
                    </div>
                </div>
            </div>
        </div>

        <h2>
            <svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>
            Directory Structure
        </h2>

        <p>Each page follows a consistent, modular structure:</p>

        <div class="code-snippet">pages/first-post/
├── config.json      # Page metadata & settings
├── content.md       # HTML content + CSS styling
├── api.py          # Custom Flask API endpoints
└── assets/         # Page-specific resources
    ├── images/
    ├── documents/
    └── data/</div>

        <h2>
            <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
            Key Features
        </h2>

        <div class="feature-grid">
            <div class="feature-card">
                <h3>
                    <svg viewBox="0 0 24 24"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/><rect x="7" y="7" width="10" height="10" rx="1"/></svg>
                    Complete Style Independence
                </h3>
                <ul>
                    <li>Each page has its own CSS</li>
                    <li>No shared stylesheets</li>
                    <li>Zero style conflicts</li>
                    <li>Full design freedom</li>
                </ul>
            </div>

            <div class="feature-card">
                <h3>
                    <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></svg>
                    Custom API Endpoints
                </h3>
                <ul>
                    <li>Page-specific Flask routes</li>
                    <li>Automatic blueprint registration</li>
                    <li>RESTful endpoint patterns</li>
                    <li>Database integration</li>
                </ul>
            </div>

            <div class="feature-card">
                <h3>
                    <svg viewBox="0 0 24 24"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>
                    Asset Management
                </h3>
                <ul>
                    <li>Per-page asset directories</li>
                    <li>Automatic compilation</li>
                    <li>Organized file structure</li>
                    <li>CDN-ready organization</li>
                </ul>
            </div>

            <div class="feature-card">
                <h3>
                    <svg viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M5 12c0 1.66 3.13 3 7 3s7-1.34 7-3"/><path d="M5 5v14c0 1.66 3.13 3 7 3s7-1.34 7-3V5"/></svg>
                    Scoped Data Storage
                </h3>
                <ul>
                    <li>NoSQL file-based database</li>
                    <li>Page-isolated collections</li>
                    <li>Thread-safe operations</li>
                    <li>Firestore-like API</li>
                </ul>
            </div>
        </div>

        <h2>
            <svg viewBox="0 0 24 24"><path d="M9 17H7A5 5 0 0 1 7 7h2"/><path d="M15 7h2a5 5 0 1 1 0 10h-2"/><path d="M11 11h2"/></svg>
            API Integration
        </h2>

        <p>Each page can have its own API endpoints. The system automatically registers Flask blueprints, so you get dynamic functionality without any setup.</p>

        <p>For example, I recently used this to add a pool ELO system I had running on the server with friends. Claude Code made a complete UI with animations in about 10 minutes. If I have an idea for a post, it can easily clip on interactive elements and give it some life pretty quickly.</p>

        <div class="api-endpoints">
            <h4>Health Check:</h4>
            <p>API Status: <a href="/api/health" target="_blank">Test the health endpoint</a></p>
        </div>

        <h2>
            <svg viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M5 12c0 1.66 3.13 3 7 3s7-1.34 7-3"/><path d="M5 5v14c0 1.66 3.13 3 7 3s7-1.34 7-3V5"/></svg>
            Database System
        </h2>

        <p>The database is just JSON files organized by page. Each page gets its own data namespace, so there's no chance of conflicts. It's thread-safe and simple:</p>

        <div class="code-snippet">data/
├── pool-leaderboard/
│   ├── players.json
│   └── game_history.json
└── shared/
    └── config.json</div>

        <p>Pages can store data with simple calls like <code>db.get_page_data('pool-leaderboard', 'players', {})</code> or <code>db.append_to_page_collection('pool-leaderboard', 'game_history', new_game)</code>. No schemas, no migrations, just JSON.</p>

        <h2>
            <svg viewBox="0 0 24 24"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/><path d="M16 18h.01"/></svg>
            Simple Benefits
        </h2>

        <p>The modular approach has some nice benefits:</p>

        <ul>
            <li>Pages can't break each other</li>
            <li>Each page loads only what it needs</li>
            <li>Easy to experiment with different designs</li>
            <li>AI can work on pages independently</li>
        </ul>

        <h2>
            <svg viewBox="0 0 24 24"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.582a.5.5 0 0 1 0 .962L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/></svg>
            Technical Stack
        </h2>

        <p>Simple Python setup:</p>
        <ul>
            <li><strong>Python compiler</strong> - Generates static HTML</li>
            <li><strong>Flask</strong> - API endpoints with auto-registration</li>
            <li><strong>File-based storage</strong> - JSON files, no database needed</li>
            <li><strong>GCP e2-micro</strong> - Cheap and effective</li>
        </ul>


        <div style="text-align: center; margin: 40px 0;">
            <a href="https://github.com/Volcanex/blog-new" class="repo-link" target="_blank">
                <svg viewBox="0 0 24 24"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
                View Source Code on GitHub
            </a>
        </div>

        <p>It's a choice that gives me freedom. Each page can have completely different styling and functionality without affecting others. The whole thing is pretty straightforward - just a Python compiler that generates static HTML and a Flask server for APIs when needed.</p>
    </div>
</div>
</html>