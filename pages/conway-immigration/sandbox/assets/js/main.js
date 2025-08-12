/**
 * Main Application - Initialization and coordination
 * Orchestrates all modules and handles application startup
 */

class ConwayVersusGame {
    constructor() {
        this.gameEngine = null;
        this.renderer = null;
        this.stateDetector = null;
        this.uiControls = null;
    }
    
    init() {
        // Initialize all modules
        this.gameEngine = new ConwayGameEngine(32);
        this.renderer = new ConwayRenderer('gameCanvas');
        this.stateDetector = new GameStateDetector();
        this.uiControls = new ConwayUIControls(this.gameEngine, this.renderer, this.stateDetector);
        
        // Initial render
        this.renderer.render(this.gameEngine.grid);
        
        // Initialize Lucide icons
        lucide.createIcons();
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    const game = new ConwayVersusGame();
    game.init();
});