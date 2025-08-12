<!-- XP.css CDN -->
<link rel="stylesheet" href="https://unpkg.com/xp.css">

<style>
body {
    font-family: "MS Sans Serif", sans-serif;
    font-size: 11px;
    background: #3a6ea5 url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='4' height='4' viewBox='0 0 4 4'><rect x='0' y='0' width='2' height='2' fill='%23316AC5'/><rect x='2' y='2' width='2' height='2' fill='%23316AC5'/></svg>");
    margin: 0;
    padding: 20px;
}

.main-window {
    margin: 0 auto;
    max-width: 800px;
    box-shadow: inset -1px -1px #0a0a0a, inset 1px 1px #dfdfdf, inset -2px -2px #808080, inset 2px 2px #c0c0c0;
}

.main-title-bar {
    background: linear-gradient(90deg, #0997ff, #0053ee);
    color: white;
    padding: 4px 8px;
    font-weight: bold;
    font-size: 11px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.main-window-body {
    background: #c0c0c0;
    padding: 20px;
    min-height: 400px;
}

.menu-title {
    text-align: center;
    margin: 0 0 20px 0;
    font-size: 18px;
    font-weight: bold;
    color: #000080;
}

.menu-description {
    text-align: center;
    margin-bottom: 30px;
    font-size: 11px;
    color: #000;
    line-height: 1.4;
}

.menu-options {
    display: flex;
    flex-direction: column;
    gap: 15px;
    max-width: 400px;
    margin: 0 auto;
}

.menu-item {
    background: #c0c0c0;
    border: 2px groove #c0c0c0;
    padding: 15px;
    cursor: pointer;
    text-decoration: none;
    color: #000;
    transition: all 0.1s ease;
}

.menu-item:hover {
    background: #d4d0c8;
}

.menu-item:active {
    border: 2px inset #c0c0c0;
}

.menu-item-title {
    font-weight: bold;
    font-size: 12px;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.menu-item-description {
    font-size: 11px;
    color: #333;
    line-height: 1.3;
}

.back-link {
    text-align: center;
    margin-top: 30px;
}

.back-link a {
    color: #000080;
    text-decoration: underline;
    font-size: 11px;
}

.back-link a:hover {
    color: #cc0000;
}

@media (max-width: 600px) {
    body {
        padding: 10px;
    }
    
    .main-window-body {
        padding: 15px;
    }
}
</style>

<html>
<div class="window main-window">
    <div class="title-bar main-title-bar">
        <div class="title-bar-text">Conway's Immigration Game - Menu</div>
    </div>
    
    <div class="window-body main-window-body">
        <div class="menu-title">Conway's Immigration Game</div>
        
        <div class="menu-description">
            Explore Conway's Game of Life through the lens of population dynamics and immigration.<br>
            Choose your preferred mode below to begin.
        </div>
        
        <div class="menu-options">
            <a href="/conway-immigration/sandbox" class="menu-item">
                <div class="menu-item-title">
                    🧪 Sandbox
                </div>
                <div class="menu-item-description">
                    Interactive sandbox for experimenting with two population dynamics. Draw patterns and observe how different colored organisms interact and compete for survival.
                </div>
            </a>
            
            <a href="/conway-immigration/info" class="menu-item">
                <div class="menu-item-title">
                    ℹ️ Information
                </div>
                <div class="menu-item-description">
                    Learn about the Immigration Game variant of Conway's Game of Life, its rules, and historical background.
                </div>
            </a>
            
            <div class="menu-item" style="opacity: 0.6; cursor: not-allowed;">
                <div class="menu-item-title">
                    🎮 Classic Mode
                </div>
                <div class="menu-item-description">
                    Traditional Conway's Game of Life with standard rules. Single-player pattern exploration. (Coming Soon)
                </div>
            </div>
            
            <div class="menu-item" style="opacity: 0.6; cursor: not-allowed;">
                <div class="menu-item-title">
                    🎯 Versus Mode
                </div>
                <div class="menu-item-description">
                    Real-time multiplayer Immigration Game with opponents, bots, or online matches. (Coming Soon)
                </div>
            </div>
        </div>
        
        <div class="back-link">
            <a href="/">← Back to Blog</a>
        </div>
    </div>
</div>
</html>