/**
 * UI Controls - Handles all user interface interactions and updates
 * Manages buttons, sliders, statistics display, and drawing interactions
 */

class ConwayUIControls {
    constructor(gameEngine, renderer, stateDetector) {
        this.gameEngine = gameEngine;
        this.renderer = renderer;
        this.stateDetector = stateDetector;
        
        // UI State
        this.drawMode = 1; // 1 = Player 1, 2 = Player 2, 0 = Eraser
        this.isDrawing = false;
        this.gameSpeed = 2.5;
        this.isRunning = false;
        this.gameLoop = null;
        
        // Speed values mapping
        this.SPEED_VALUES = [0.1, 0.25, 0.5, 1, 2.5, 5, 10, 20];
        
        this.setupEventListeners();
        this.updateButtonColors();
        this.updateStats();
        this.updateGameState();
    }
    
    setupEventListeners() {
        // Drawing mode buttons
        document.getElementById('player1Btn').addEventListener('click', () => this.setDrawMode(1));
        document.getElementById('player2Btn').addEventListener('click', () => this.setDrawMode(2));
        document.getElementById('eraserBtn').addEventListener('click', () => this.setDrawMode(0));
        
        // Game control buttons
        document.getElementById('playBtn').addEventListener('click', () => this.playGame());
        document.getElementById('pauseBtn').addEventListener('click', () => this.pauseGame());
        document.getElementById('stepBtn').addEventListener('click', () => this.stepGame());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearGrid());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetToGenZero());
        document.getElementById('downloadBtn').addEventListener('click', () => this.downloadFrame());
        
        // Settings
        document.getElementById('gridSize').addEventListener('change', (e) => this.handleGridSizeChange(e));
        document.getElementById('speedSlider').addEventListener('input', (e) => this.handleSpeedChange(e));
        
        // Color pickers
        document.getElementById('player1Color').addEventListener('change', (e) => this.handleColorChange(1, e.target.value));
        document.getElementById('player2Color').addEventListener('change', (e) => this.handleColorChange(2, e.target.value));
        
        // Canvas drawing events
        const canvas = this.renderer.getCanvas();
        canvas.addEventListener('mousedown', (e) => this.startDrawing(e));
        canvas.addEventListener('mousemove', (e) => this.draw(e));
        canvas.addEventListener('mouseup', () => this.stopDrawing());
        canvas.addEventListener('mouseleave', () => this.stopDrawing());
        
        // Touch events for mobile
        canvas.addEventListener('touchstart', (e) => this.handleTouchStart(e), { passive: false });
        canvas.addEventListener('touchmove', (e) => this.handleTouchMove(e), { passive: false });
        canvas.addEventListener('touchend', () => this.stopDrawing(), { passive: false });
        
        // Window resize
        window.addEventListener('resize', () => {
            this.renderer.resizeCanvas();
            this.renderer.render(this.gameEngine.grid);
        });
    }
    
    setDrawMode(mode) {
        this.drawMode = mode;
        
        // Update button states
        document.querySelectorAll('.btn.player1, .btn.player2, .btn.eraser').forEach(btn => {
            btn.classList.remove('active');
        });
        
        if (mode === 1) {
            document.getElementById('player1Btn').classList.add('active');
        } else if (mode === 2) {
            document.getElementById('player2Btn').classList.add('active');
        } else {
            document.getElementById('eraserBtn').classList.add('active');
        }
    }
    
    handleGridSizeChange(e) {
        const newSize = parseInt(e.target.value);
        if (newSize !== this.gameEngine.gridSize) {
            this.gameEngine.setGridSize(newSize);
            this.renderer.setGridSize(newSize);
            this.stateDetector.reset();
            this.renderer.render(this.gameEngine.grid);
            this.updateStats();
            this.updateGameState();
        }
    }
    
    handleSpeedChange(e) {
        const speedIndex = parseInt(e.target.value);
        this.gameSpeed = this.SPEED_VALUES[speedIndex];
        document.getElementById('speedValue').textContent = `${this.gameSpeed} FPS`;
        
        if (this.isRunning) {
            clearInterval(this.gameLoop);
            this.startGameLoop();
        }
    }
    
    startDrawing(e) {
        e.preventDefault();
        this.isDrawing = true;
        const pos = this.renderer.getMousePos(e);
        this.drawCell(pos.x, pos.y);
    }
    
    draw(e) {
        if (!this.isDrawing) return;
        e.preventDefault();
        
        const pos = this.renderer.getMousePos(e);
        this.drawCell(pos.x, pos.y);
    }
    
    stopDrawing() {
        this.isDrawing = false;
    }
    
    handleTouchStart(e) {
        e.preventDefault();
        this.isDrawing = true;
        const pos = this.renderer.getTouchPos(e);
        this.drawCell(pos.x, pos.y);
    }
    
    handleTouchMove(e) {
        if (!this.isDrawing) return;
        e.preventDefault();
        
        const pos = this.renderer.getTouchPos(e);
        this.drawCell(pos.x, pos.y);
    }
    
    drawCell(x, y) {
        const oldValue = this.gameEngine.getCell(x, y);
        if (this.gameEngine.setCell(x, y, this.drawMode)) {
            // Re-render the entire grid to ensure proper display in both modes
            this.renderer.render(this.gameEngine.grid);
            this.updateStats();
            // Reset game state detection when user draws
            this.stateDetector.reset();
            this.updateGameState();
        }
    }
    
    playGame() {
        if (!this.isRunning) {
            this.isRunning = true;
            this.startGameLoop();
            this.updateGameStatus();
        }
    }
    
    pauseGame() {
        if (this.isRunning) {
            this.isRunning = false;
            clearInterval(this.gameLoop);
            this.updateGameStatus();
        }
    }
    
    stepGame() {
        this.gameEngine.stepGeneration();
        this.renderer.render(this.gameEngine.grid);
        this.updateStats();
        this.checkGameState();
        this.updateGameStatus();
    }
    
    clearGrid() {
        this.pauseGame();
        this.gameEngine.clear();
        this.stateDetector.reset();
        this.renderer.render(this.gameEngine.grid);
        this.updateStats();
        this.updateGameState();
        this.updateGameStatus();
    }
    
    resetToGenZero() {
        this.pauseGame();
        this.gameEngine.generation = 0;
        this.stateDetector.reset();
        this.updateStats();
        this.updateGameState();
        this.updateGameStatus();
    }
    
    downloadFrame() {
        // Create download link for canvas as PNG
        const canvas = this.renderer.getCanvas();
        const link = document.createElement('a');
        link.download = `immigration-game-gen-${this.gameEngine.generation}.png`;
        link.href = canvas.toDataURL('image/png');
        
        // Trigger download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    startGameLoop() {
        this.gameLoop = setInterval(() => {
            this.gameEngine.stepGeneration();
            this.renderer.render(this.gameEngine.grid);
            this.updateStats();
            this.checkGameState();
            this.updateGameStatus();
        }, 1000 / this.gameSpeed);
    }
    
    checkGameState() {
        const gameSnapshot = this.gameEngine.getGridSnapshot();
        const cellCounts = this.gameEngine.countCells();
        
        this.stateDetector.detectGameState(gameSnapshot, cellCounts);
        this.updateGameState();
        
        // Auto-pause when first detecting static, periodic, or extinct states
        if (this.stateDetector.shouldAutoPause(this.isRunning)) {
            setTimeout(() => {
                const state = this.stateDetector.getState();
                if ((state.gameState === 'static' || state.gameState === 'periodic' || state.gameState === 'extinct') && this.isRunning) {
                    this.pauseGame();
                }
            }, 1000); // Pause after 1 second to let user see the final state
        }
    }
    
    updateStats() {
        const counts = this.gameEngine.countCells();
        
        document.getElementById('player1Count').textContent = counts.player1;
        document.getElementById('player2Count').textContent = counts.player2;
        document.getElementById('generation').textContent = this.gameEngine.generation;
        document.getElementById('totalCells').textContent = counts.player1 + counts.player2;
    }
    
    updateGameState() {
        const state = this.stateDetector.getState();
        const counts = this.gameEngine.countCells();
        
        const gameStateEl = document.getElementById('gameState');
        const periodRowEl = document.getElementById('periodRow');
        const periodLengthEl = document.getElementById('periodLength');
        const currentWinnerEl = document.getElementById('currentWinner');
        
        // Update game state display
        gameStateEl.textContent = state.gameState.charAt(0).toUpperCase() + state.gameState.slice(1);
        gameStateEl.className = `stat-value ${state.gameState}`;
        
        // Show/hide period information
        if (state.gameState === 'periodic') {
            periodRowEl.style.display = 'flex';
            periodLengthEl.textContent = `${state.periodLength} generations`;
        } else {
            periodRowEl.style.display = 'none';
        }
        
        // Update winner
        const winner = this.stateDetector.calculateWinner(counts, this.isRunning);
        currentWinnerEl.textContent = winner;
        
        // Color winner text based on leading player
        currentWinnerEl.className = 'stat-value';
        if (winner.includes('Player 1')) {
            currentWinnerEl.classList.add('player1');
        } else if (winner.includes('Player 2')) {
            currentWinnerEl.classList.add('player2');
        }
    }
    
    updateGameStatus() {
        const statusEl = document.getElementById('gameStatus');
        const counts = this.gameEngine.countCells();
        const totalCells = counts.player1 + counts.player2;
        
        if (totalCells === 0) {
            statusEl.className = 'game-status status-extinct';
            statusEl.textContent = 'Extinct - All cells died!';
            this.pauseGame();
        } else if (this.isRunning) {
            statusEl.className = 'game-status status-running';
            if (counts.player1 > counts.player2) {
                statusEl.textContent = `Running - Player 1 leads ${counts.player1}-${counts.player2}`;
            } else if (counts.player2 > counts.player1) {
                statusEl.textContent = `Running - Player 2 leads ${counts.player2}-${counts.player1}`;
            } else {
                statusEl.textContent = `Running - Tied at ${counts.player1}-${counts.player2}`;
            }
        } else {
            statusEl.className = 'game-status status-paused';
            if (totalCells === 0) {
                statusEl.textContent = 'Paused - Draw cells to start!';
            } else if (counts.player1 > counts.player2) {
                statusEl.textContent = `Paused - Player 1 leads ${counts.player1}-${counts.player2}`;
            } else if (counts.player2 > counts.player1) {
                statusEl.textContent = `Paused - Player 2 leads ${counts.player2}-${counts.player1}`;
            } else {
                statusEl.textContent = `Paused - Tied at ${counts.player1}-${counts.player2}`;
            }
        }
    }
    
    handleColorChange(player, hexColor) {
        // Update renderer colors
        const player1Hex = document.getElementById('player1Color').value;
        const player2Hex = document.getElementById('player2Color').value;
        this.renderer.updatePlayerColors(player1Hex, player2Hex);
        
        // Update button styling
        this.updateButtonColors();
        
        // Re-render with new colors
        this.renderer.render(this.gameEngine.grid);
    }
    
    updateButtonColors() {
        const player1Color = document.getElementById('player1Color').value;
        const player2Color = document.getElementById('player2Color').value;
        
        const player1Btn = document.getElementById('player1Btn');
        const player2Btn = document.getElementById('player2Btn');
        
        // Update button colors to match selected colors
        player1Btn.style.setProperty('--player-color', player1Color);
        player2Btn.style.setProperty('--player-color', player2Color);
        
        // Update statistics text colors too
        const player1Counts = document.querySelectorAll('.stat-value.player1');
        const player2Counts = document.querySelectorAll('.stat-value.player2');
        
        player1Counts.forEach(el => el.style.color = player1Color);
        player2Counts.forEach(el => el.style.color = player2Color);
    }
}