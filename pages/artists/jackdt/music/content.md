<style>
@font-face {
    font-family: 'Inter';
    font-style: normal;
    font-weight: 300 900;
    font-display: fallback;
    src: url('../assets/fonts/Inter-Variable.woff2') format('woff2');
}
@font-face {
    font-family: 'Cardo';
    font-style: normal;
    font-weight: 400;
    font-display: fallback;
    src: url('../assets/fonts/Cardo-Regular.woff2') format('woff2');
}
@font-face {
    font-family: 'Cardo';
    font-style: italic;
    font-weight: 400;
    font-display: fallback;
    src: url('../assets/fonts/Cardo-Italic.woff2') format('woff2');
}
@font-face {
    font-family: 'Cardo';
    font-style: normal;
    font-weight: 700;
    font-display: fallback;
    src: url('../assets/fonts/Cardo-Bold.woff2') format('woff2');
}

:root {
    --primary: #2a2a28;
    --accent: #7a8a6e;
    --accent-hover: #5d7050;
    --bg: #f5f2ed;
    --border: #e5e0d8;
    --text-muted: #6b6860;
    --text-light: #9a958c;
    --text-font: 'Inter', sans-serif;
    --heading-font: 'Cardo', serif;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: var(--text-font);
    color: var(--primary);
    background: var(--bg);
    line-height: 1.7;
    font-size: 1.05rem;
    font-weight: 400;
    min-height: 100vh;
    display: flex;
    opacity: 0;
    animation: pageIn 1s ease-out forwards;
}

body::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 9999;
    opacity: 0.03;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
    background-repeat: repeat;
    background-size: 256px 256px;
}

@keyframes pageIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideRight { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }

h1, h2, h3 { font-family: var(--heading-font); color: var(--primary); line-height: 1.4; }
a { color: var(--primary); text-decoration: none; transition: color 0.4s ease; }
a:hover { color: var(--accent); }

.sidebar {
    width: 260px; min-width: 260px; min-height: 100vh;
    padding: 48px 36px; display: flex; flex-direction: column; gap: 28px;
    animation: slideRight 0.8s ease-out 0.1s both;
}
.site-name { font-family: var(--text-font); font-weight: 600; font-size: 18px; display: block; letter-spacing: 0.2px; transition: color 0.4s ease; }
.site-name:hover { color: var(--accent); }

.nav-links { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 10px; }
.nav-links a { font-size: 14px; font-weight: 400; display: block; transition: color 0.3s ease, padding-left 0.3s ease; }
.nav-links a:hover { color: var(--accent); padding-left: 6px; }

.social-links { display: flex; gap: 16px; margin-top: auto; }
.social-links a { font-size: 12px; color: var(--text-light); letter-spacing: 0.5px; transition: color 0.4s ease; }
.social-links a:hover { color: var(--accent); }

.menu-toggle { display: none; background: none; border: none; cursor: pointer; width: 28px; height: 20px; position: relative; z-index: 1001; }
.menu-toggle span { display: block; width: 100%; height: 1.5px; background: var(--primary); position: absolute; left: 0; transition: transform 0.35s ease, opacity 0.25s ease; }
.menu-toggle span:nth-child(1) { top: 4px; }
.menu-toggle span:nth-child(2) { bottom: 4px; }
.menu-toggle.active span:nth-child(1) { top: 50%; transform: translateY(-50%) rotate(45deg); }
.menu-toggle.active span:nth-child(2) { bottom: auto; top: 50%; transform: translateY(-50%) rotate(-45deg); }
.mobile-header { display: none; }

@media (max-width: 768px) {
    body { flex-direction: column; font-size: 14px; }
    .mobile-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; position: sticky; top: 0; background: var(--bg); z-index: 1000; border-bottom: 1px solid var(--border); }
    .mobile-header .site-name { font-size: 16px; animation: none; }
    .menu-toggle { display: block; }
    .sidebar { width: 100%; min-width: 100%; min-height: 0; padding: 0 20px; gap: 16px; overflow: hidden; display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.45s ease; }
    .sidebar.open { grid-template-rows: 1fr; border-bottom: 1px solid var(--border); }
    .sidebar > .sidebar-inner { overflow: hidden; }
    .sidebar .site-name { display: none; }
    .sidebar .nav-links { padding-top: 16px; flex-direction: column; gap: 8px; }
    .sidebar .nav-links a { font-size: 12px; }
    .sidebar .social-links { padding-bottom: 20px; margin-top: 8px; }
}

.main-content {
    flex: 1; padding: 80px 60px; max-width: 800px;
    animation: pageIn 1s ease-out 0.3s both;
}
.main-content h1 { font-style: italic; font-weight: 400; font-size: 2rem; margin-bottom: 12px; }
.main-content p { color: var(--text-muted); margin-bottom: 24px; font-size: 14px; line-height: 1.8; }

.music-player {
    margin-top: 32px;
}

.track {
    padding: 24px;
    margin-bottom: 20px;
    background: rgba(122, 138, 110, 0.06);
    border: 1px solid var(--border);
    border-radius: 8px;
    transition: all 0.3s ease;
}

.track:hover {
    background: rgba(122, 138, 110, 0.10);
    border-color: var(--accent);
}

.track-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
}

.track-info h3 {
    font-family: var(--heading-font);
    font-size: 18px;
    font-weight: 600;
    color: var(--primary);
    margin-bottom: 4px;
}

.track-meta {
    font-size: 13px;
    color: var(--text-light);
}

.track-duration {
    font-size: 13px;
    color: var(--text-muted);
    font-family: 'Courier New', monospace;
}

.waveform {
    height: 80px;
    display: flex;
    align-items: flex-end;
    gap: 3px;
    margin-bottom: 16px;
}

.waveform-bar {
    flex: 1;
    background: var(--accent);
    border-radius: 2px;
    transition: all 0.2s ease;
    opacity: 0.6;
}

.track:hover .waveform-bar {
    opacity: 0.9;
}

.play-button {
    width: 100%;
    padding: 12px;
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 6px;
    font-family: var(--text-font);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.play-button:hover {
    background: var(--accent-hover);
}

.platform-note {
    margin-top: 48px;
    padding: 20px 24px;
    background: rgba(122, 138, 110, 0.06);
    border-left: 3px solid var(--accent);
    font-size: 13px;
    line-height: 1.7;
    color: var(--text-muted);
}

.platform-note strong {
    color: var(--primary);
    font-weight: 600;
}

@media (max-width: 768px) {
    .main-content { padding: 32px 20px; }
    .main-content h1 { font-size: 1.5rem; }
    .track { padding: 16px; }
    .waveform { height: 60px; gap: 2px; }
    .track-header { flex-direction: column; gap: 8px; }
}
</style>

<html>
<div class="mobile-header">
    <a href="../home/" class="site-name">Jack</a>
    <button class="menu-toggle" onclick="this.classList.toggle('active'); document.querySelector('.sidebar').classList.toggle('open');" aria-label="Menu">
        <span></span>
        <span></span>
    </button>
</div>

<div class="sidebar">
    <div class="sidebar-inner">
    <a href="../home/" class="site-name">Jack</a>
    <ul class="nav-links">
        <li><a href="../about/">About</a></li>
        <li><a href="../music/">Music</a></li>
    </ul>
    <div class="social-links">
        <a href="#">Instagram</a>
    </div>
    </div>
</div>

<main class="main-content">
    <h1>Music</h1>
    <p>Listen to tracks from Keskesay on SoundCloud.</p>

    <div class="soundcloud-embed">
        <iframe width="100%" height="450" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//soundcloud.com/user-216694930&color=%237a8a6e&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>
    </div>

    <div class="platform-note">
        <strong>This SoundCloud embed pulls your real tracks automatically</strong>
        <br><br>
        We could also build a custom player that:
        <ul style="margin-top: 12px;">
            <li>Fetches tracks via SoundCloud API with authentication</li>
            <li>Displays real waveform data for each track</li>
            <li>Adds custom play/pause controls matching your site design</li>
            <li>Shows track metadata, comments, and stats</li>
            <li>Or integrate with Spotify, Bandcamp, or host files directly</li>
        </ul>
        <br>
        The platform is flexible—we can create exactly what you need.
    </div>
</main>
</html>
