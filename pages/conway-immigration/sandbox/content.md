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
    max-width: 1200px;
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
    padding: 8px;
    display: grid;
    grid-template-columns: 1fr 320px;
    gap: 12px;
    min-height: 500px;
}

.canvas-panel {
    background: #c0c0c0;
    border: 2px inset #c0c0c0;
    padding: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

#gameCanvas {
    border: 2px inset #c0c0c0;
    background: #000;
}

.controls-panel {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.control-group {
    border: 2px groove #c0c0c0;
    padding: 12px;
    background: #c0c0c0;
}

.control-group legend {
    font-weight: bold;
    padding: 0 4px;
}

.button-row {
    display: flex;
    gap: 4px;
    flex-wrap: wrap;
    margin-top: 4px;
}

button {
    font-family: "MS Sans Serif", sans-serif;
    font-size: 11px;
    min-width: 100px;
    height: 30px;
    padding: 1px 8px;
    background: #c0c0c0;
    border: 1px outset #c0c0c0;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2px;
}

button:active {
    border: 1px inset #c0c0c0;
}

button:disabled {
    color: #808080;
    cursor: default;
}

button.active {
    border: 1px inset #c0c0c0;
    background: #e0e0e0;
}

button.player1.active {
    background: var(--player-color, #cce7ff);
    border-color: var(--player-color, #0066cc);
}

button.player2.active {
    background: var(--player-color, #ffcccc);
    border-color: var(--player-color, #cc0000);
}

button.player1 {
    border-left: 3px solid var(--player-color, #0066cc);
}

button.player2 {
    border-left: 3px solid var(--player-color, #cc0000);
}

select {
    font-family: "MS Sans Serif", sans-serif;
    font-size: 11px;
    background: white;
    border: 1px inset #c0c0c0;
    height: 28px;
    width: 100%;
}

.field-row {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 4px 0;
}

.field-row label {
    min-width: 80px;
    font-weight: bold;
}

input[type="color"] {
    width: 40px;
    height: 28px;
    border: 1px inset #c0c0c0;
    background: white;
    cursor: pointer;
}

.stats-panel {
    background: white;
    border: 1px inset #c0c0c0;
    padding: 4px;
    font-family: "MS Sans Serif", sans-serif;
    font-size: 11px;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    margin: 2px 0;
    padding: 1px 4px;
}

.stat-label {
    color: #000;
}

.stat-value {
    font-weight: bold;
}

.stat-value.player1 {
    color: #0066cc;
}

.stat-value.player2 {
    color: #cc0000;
}

.speed-container {
    margin: 4px 0;
}

.speed-slider {
    width: 100%;
    margin: 4px 0;
}

.speed-value {
    text-align: center;
    font-size: 11px;
    color: #000;
}

.game-title {
    text-align: center;
    margin: 8px 0;
    font-size: 16px;
    font-weight: bold;
    color: #000080;
}

.nav-menu {
    background: #c0c0c0;
    border: 2px groove #c0c0c0;
    padding: 8px;
    margin-bottom: 12px;
}

.nav-menu legend {
    font-weight: bold;
    padding: 0 4px;
}

.nav-buttons {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
}

.nav-btn {
    font-family: "MS Sans Serif", sans-serif;
    font-size: 11px;
    min-width: 120px;
    height: 30px;
    padding: 1px 12px;
    background: #c0c0c0;
    border: 1px outset #c0c0c0;
    cursor: pointer;
    text-decoration: none;
    color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
}

.nav-btn:hover {
    background: #d4d0c8;
}

.nav-btn:active {
    border: 1px inset #c0c0c0;
}

.nav-btn.current {
    border: 1px inset #c0c0c0;
    background: #e0e0e0;
}

@media (max-width: 1000px) {
    .main-window-body {
        grid-template-columns: 1fr;
        gap: 8px;
    }
    
    .controls-panel {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 8px;
    }
}

@media (max-width: 600px) {
    body {
        padding: 10px;
    }
    
    #gameCanvas {
        max-width: 100%;
        height: auto;
    }
}
</style>

<html>
<div class="window main-window">
    <div class="title-bar main-title-bar">
        <div class="title-bar-text">Conway's Immigration Game - Sandbox</div>
    </div>
    
    <div class="window-body main-window-body">
        <!-- Navigation Menu -->
        <div style="grid-column: 1 / -1;">
            <fieldset class="nav-menu">
                <legend>📁 Immigration Game Modes</legend>
                <div class="nav-buttons">
                    <a href="/conway-immigration" class="nav-btn">
                        📋 Menu
                    </a>
                    <a href="/conway-immigration/sandbox" class="nav-btn current">
                        🧪 Sandbox
                    </a>
                    <a href="/conway-immigration/info" class="nav-btn">
                        ℹ️ Information
                    </a>
                </div>
            </fieldset>
        </div>
        
        <div class="canvas-panel">
            <div class="game-title">Immigration Game Sandbox</div>
            <canvas id="gameCanvas" width="800" height="600"></canvas>
        </div>
        
        <div class="controls-panel">
            <!-- Draw Mode Controls -->
            <fieldset class="control-group">
                <legend>Draw Mode</legend>
                <div class="button-row">
                    <button id="player1Btn" class="player1 active">
                        Player 1
                    </button>
                    <button id="player2Btn" class="player2">
                        Player 2
                    </button>
                    <button id="eraserBtn">
                        ✏️ Erase
                    </button>
                </div>
            </fieldset>
            
            <!-- Game Controls -->
            <fieldset class="control-group">
                <legend>Game Controls</legend>
                <div class="button-row">
                    <button id="playBtn">
                        ▶️ Play
                    </button>
                    <button id="pauseBtn">
                        ⏸️ Pause
                    </button>
                    <button id="stepBtn">
                        ⏭️ Step
                    </button>
                    <button id="clearBtn">
                        🗑️ Clear
                    </button>
                </div>
                <div class="button-row">
                    <button id="resetBtn">
                        🔄 Reset to Gen 0
                    </button>
                    <button id="downloadBtn">
                        💾 Download Frame
                    </button>
                </div>
            </fieldset>
            
            <!-- Game Settings -->
            <fieldset class="control-group">
                <legend>Settings</legend>
                <div class="field-row">
                    <label for="gridSize">Grid Size:</label>
                    <select id="gridSize">
                        <option value="16">16x16 (Fast)</option>
                        <option value="32" selected>32x32 (Medium)</option>
                        <option value="64">64x64 (Large)</option>
                    </select>
                </div>
                <div class="field-row">
                    <label>Speed:</label>
                    <div class="speed-container">
                        <input type="range" id="speedSlider" class="speed-slider" 
                               min="0" max="7" value="5" step="1">
                        <div class="speed-value" id="speedValue">2.5 FPS</div>
                    </div>
                </div>
            </fieldset>
            
            <!-- Player Colors -->
            <fieldset class="control-group">
                <legend>Player Colors</legend>
                <div class="field-row">
                    <label for="player1Color">Player 1 Color:</label>
                    <input type="color" id="player1Color" value="#0066ff">
                </div>
                <div class="field-row">
                    <label for="player2Color">Player 2 Color:</label>
                    <input type="color" id="player2Color" value="#ff0000">
                </div>
            </fieldset>
            
            <!-- Statistics -->
            <fieldset class="control-group">
                <legend>Statistics</legend>
                <div class="stats-panel">
                    <div class="stat-row">
                        <span class="stat-label">Player 1 Cells:</span>
                        <span class="stat-value player1" id="player1Count">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Player 2 Cells:</span>
                        <span class="stat-value player2" id="player2Count">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Generation:</span>
                        <span class="stat-value" id="generation">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Total Cells:</span>
                        <span class="stat-value" id="totalCells">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Status:</span>
                        <span class="stat-value" id="gameStatus">Ready</span>
                    </div>
                </div>
            </fieldset>
            
            <!-- Game State & Winner -->
            <fieldset class="control-group">
                <legend>Game State</legend>
                <div class="stats-panel">
                    <div class="stat-row">
                        <span class="stat-label">State:</span>
                        <span class="stat-value" id="gameState">Active</span>
                    </div>
                    <div class="stat-row" id="periodRow" style="display: none;">
                        <span class="stat-label">Period:</span>
                        <span class="stat-value" id="periodLength">-</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Winner:</span>
                        <span class="stat-value" id="currentWinner">None yet</span>
                    </div>
                </div>
            </fieldset>
        </div>
    </div>
</div>

<!-- External Scripts -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>

<!-- Game Modules -->
<script src="/assets/conway-immigration/sandbox/js/game-engine.js"></script>
<script src="/assets/conway-immigration/sandbox/js/game-state.js"></script>
<script src="/assets/conway-immigration/sandbox/js/renderer.js"></script>
<script src="/assets/conway-immigration/sandbox/js/ui-controls.js"></script>
<script src="/assets/conway-immigration/sandbox/js/main.js"></script>
</html>