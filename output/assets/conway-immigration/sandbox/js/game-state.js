/**
 * Game State Detection - Pattern recognition and winner calculation
 * Handles detection of static, periodic, and extinct states with intelligent winner logic
 */

class GameStateDetector {
    constructor() {
        this.gameHistory = [];
        this.maxHistoryLength = 100;
        this.gameState = 'active'; // active, static, periodic, extinct
        this.periodLength = 0;
        this.lastAlivePlayer = null;
        this.hasAutoPausedForState = false;
    }
    
    reset() {
        this.gameHistory = [];
        this.gameState = 'active';
        this.periodLength = 0;
        this.lastAlivePlayer = null;
        this.hasAutoPausedForState = false;
    }
    
    detectGameState(gridSnapshot, cellCounts) {
        // Check for extinction
        if (cellCounts.player1 + cellCounts.player2 === 0) {
            this.gameState = 'extinct';
            this.periodLength = 0;
            return this.gameState;
        }
        
        // Update last alive player for extinction tracking
        if (cellCounts.player1 > 0 && cellCounts.player2 === 0) {
            this.lastAlivePlayer = 1;
        } else if (cellCounts.player2 > 0 && cellCounts.player1 === 0) {
            this.lastAlivePlayer = 2;
        } else if (cellCounts.player1 > 0 && cellCounts.player2 > 0) {
            this.lastAlivePlayer = null; // Both alive
        }
        
        // Add current state to history
        this.gameHistory.push(gridSnapshot);
        if (this.gameHistory.length > this.maxHistoryLength) {
            this.gameHistory.shift();
        }
        
        // Look for static patterns (grid hasn't changed)
        if (this.gameHistory.length >= 2 && 
            this.gameHistory[this.gameHistory.length - 1] === this.gameHistory[this.gameHistory.length - 2]) {
            this.gameState = 'static';
            this.periodLength = 0;
            return this.gameState;
        }
        
        // Look for periodic patterns
        if (this.gameHistory.length >= 4) {
            for (let period = 2; period <= Math.floor(this.gameHistory.length / 2); period++) {
                let isPeriodicPattern = true;
                const checkLength = Math.min(period * 3, this.gameHistory.length);
                
                for (let i = 0; i < checkLength - period; i++) {
                    const currentIndex = this.gameHistory.length - 1 - i;
                    const compareIndex = currentIndex - period;
                    
                    if (compareIndex < 0 || this.gameHistory[currentIndex] !== this.gameHistory[compareIndex]) {
                        isPeriodicPattern = false;
                        break;
                    }
                }
                
                if (isPeriodicPattern) {
                    this.gameState = 'periodic';
                    this.periodLength = period;
                    return this.gameState;
                }
            }
        }
        
        // Default to active
        this.gameState = 'active';
        this.periodLength = 0;
        return this.gameState;
    }
    
    calculateWinner(cellCounts, isRunning) {
        switch (this.gameState) {
            case 'extinct':
                if (this.lastAlivePlayer === 1) {
                    return 'Player 1 (Last alive)';
                } else if (this.lastAlivePlayer === 2) {
                    return 'Player 2 (Last alive)';
                } else {
                    return 'Draw (Simultaneous extinction)';
                }
                
            case 'static':
                if (cellCounts.player1 > cellCounts.player2) {
                    return `Player 1 (${cellCounts.player1} vs ${cellCounts.player2})`;
                } else if (cellCounts.player2 > cellCounts.player1) {
                    return `Player 2 (${cellCounts.player2} vs ${cellCounts.player1})`;
                } else {
                    return `Draw (${cellCounts.player1}-${cellCounts.player2})`;
                }
                
            case 'periodic':
                // For periodic patterns, use current cell counts as the period is maintained
                if (cellCounts.player1 > cellCounts.player2) {
                    return `Player 1 (${cellCounts.player1} vs ${cellCounts.player2})`;
                } else if (cellCounts.player2 > cellCounts.player1) {
                    return `Player 2 (${cellCounts.player2} vs ${cellCounts.player1})`;
                } else {
                    return `Draw (${cellCounts.player1}-${cellCounts.player2})`;
                }
                
            case 'active':
            default:
                if (!isRunning) {
                    return 'None yet';
                }
                if (cellCounts.player1 > cellCounts.player2) {
                    return `Player 1 leading (${cellCounts.player1} vs ${cellCounts.player2})`;
                } else if (cellCounts.player2 > cellCounts.player1) {
                    return `Player 2 leading (${cellCounts.player2} vs ${cellCounts.player1})`;
                } else {
                    return `Currently tied (${cellCounts.player1}-${cellCounts.player2})`;
                }
        }
    }
    
    shouldAutoPause(isRunning) {
        const shouldPause = (this.gameState === 'static' || this.gameState === 'periodic' || this.gameState === 'extinct') 
                          && isRunning && !this.hasAutoPausedForState;
        if (shouldPause) {
            this.hasAutoPausedForState = true;
        }
        return shouldPause;
    }
    
    getState() {
        return {
            gameState: this.gameState,
            periodLength: this.periodLength,
            lastAlivePlayer: this.lastAlivePlayer,
            hasAutoPausedForState: this.hasAutoPausedForState
        };
    }
}