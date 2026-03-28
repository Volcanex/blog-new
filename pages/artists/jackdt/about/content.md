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
    flex: 1; padding: 80px 60px; max-width: 720px;
    animation: pageIn 1s ease-out 0.3s both;
}
.main-content h1 { font-style: italic; font-weight: 400; font-size: 2rem; margin-bottom: 24px; }
.main-content h2 { font-style: italic; font-weight: 400; font-size: 1.5rem; margin-top: 48px; margin-bottom: 20px; }
.main-content p { color: var(--text-muted); margin-bottom: 16px; font-size: 14px; line-height: 1.8; }
.main-content a { color: var(--accent); }
.main-content ul { color: var(--text-muted); margin-bottom: 16px; font-size: 14px; line-height: 1.8; margin-left: 20px; }
.main-content li { margin-bottom: 8px; }

.bio-intro {
    font-size: 15px;
    line-height: 1.9;
    margin-bottom: 20px;
}

.music-player {
    margin-top: 24px;
    padding: 24px;
    background: rgba(122, 138, 110, 0.08);
    border: 1px solid var(--border);
    border-radius: 8px;
}

.track {
    padding: 16px 0;
    border-bottom: 1px solid var(--border);
    cursor: pointer;
    transition: all 0.3s ease;
}
.track:last-child { border-bottom: none; }
.track:hover { padding-left: 8px; }

.track-title {
    font-family: var(--heading-font);
    font-size: 15px;
    font-weight: 600;
    color: var(--primary);
    margin-bottom: 4px;
}

.track-meta {
    font-size: 12px;
    color: var(--text-light);
}

.waveform {
    margin-top: 12px;
    height: 60px;
    display: flex;
    align-items: flex-end;
    gap: 2px;
    opacity: 0.7;
}

.waveform-bar {
    flex: 1;
    background: var(--accent);
    border-radius: 2px;
    transition: all 0.3s ease;
}

.track:hover .waveform-bar {
    opacity: 0.8;
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
    .main-content h2 { font-size: 1.3rem; margin-top: 36px; }
    .music-player { padding: 16px; }
    .waveform { height: 50px; }
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
    <h1>Jack Dennison-Thompson</h1>

    <div class="bio-intro">
        <p><strong>MA Magazine Journalism student at City, University of London</strong>, with a passion for storytelling across music, culture, and current affairs.</p>

        <p>I have hands-on experience at <a href="https://maghrebi.org" target="_blank">maghrebi.org</a>, where I reported on North African current events under award-winning journalist Martin Jay, and through music journalism for The Indiependent and Folk and Honey, where I wrote reviews, features and interviews.</p>

        <p>My work spans news reporting, cultural features, and music journalism—from covering political developments to profiling emerging artists. I'm particularly interested in stories that sit at the intersection of culture, politics, and community.</p>

        <p>Beyond writing, I bring multimedia skills from producing content for my YouTube channel and radio show, alongside proficiency in Adobe Creative Suite, Ableton, and WordPress.</p>
    </div>

    <h2>Experience Highlights</h2>
    <ul>
        <li><strong>Contributing Writer</strong> at Clash Music Group (2026-Present)</li>
        <li><strong>Deputy Multi Media Editor</strong> at GTFO Magazine</li>
        <li><strong>News Intern</strong> at Campaign UK</li>
        <li>Contributor to Maghrebi.org, Folk and Honey, The Indiependent</li>
    </ul>

    <div class="platform-note">
        <strong>This site is an example of what you can build on this platform.</strong>
        <br><br>
        You can create portfolio sites, journalism hubs, music showcases, or custom tools—all hosted for free on Gabriel's servers. The only cost? A custom domain, if you want one.
        <br><br>
        We could pull data directly from your SoundCloud API, create custom audio players with real waveforms, integrate your latest articles, or build any interactive tool you need. The possibilities are endless.
    </div>
</main>
</html>