/**
 * Conway's Game of Life Engine - Core game logic and rules
 * This module handles the fundamental Conway's Game of Life mechanics with versus rules
 */

class ConwayGameEngine {
    constructor(gridSize = 32) {
        this.gridSize = gridSize;
        this.grid = [];
        this.generation = 0;
        
        // Game constants
        this.EMPTY = 0;
        this.PLAYER1 = 1;
        this.PLAYER2 = 2;
        
        this.initGrid();
    }
    
    initGrid() {
        this.grid = Array(this.gridSize).fill().map(() => Array(this.gridSize).fill(this.EMPTY));
        this.generation = 0;
    }
    
    setGridSize(newSize) {
        this.gridSize = newSize;
        this.initGrid();
    }
    
    setCell(x, y, value) {
        if (x >= 0 && x < this.gridSize && y >= 0 && y < this.gridSize) {
            this.grid[y][x] = value;
            return true;
        }
        return false;
    }
    
    getCell(x, y) {
        if (x >= 0 && x < this.gridSize && y >= 0 && y < this.gridSize) {
            return this.grid[y][x];
        }
        return this.EMPTY;
    }
    
    countNeighbors(x, y) {
        let player1Neighbors = 0;
        let player2Neighbors = 0;
        
        for (let dy = -1; dy <= 1; dy++) {
            for (let dx = -1; dx <= 1; dx++) {
                if (dx === 0 && dy === 0) continue;
                
                const nx = x + dx;
                const ny = y + dy;
                
                if (nx >= 0 && nx < this.gridSize && ny >= 0 && ny < this.gridSize) {
                    if (this.grid[ny][nx] === this.PLAYER1) player1Neighbors++;
                    if (this.grid[ny][nx] === this.PLAYER2) player2Neighbors++;
                }
            }
        }
        
        return { player1: player1Neighbors, player2: player2Neighbors, total: player1Neighbors + player2Neighbors };
    }
    
    stepGeneration() {
        const newGrid = Array(this.gridSize).fill().map(() => Array(this.gridSize).fill(this.EMPTY));
        
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                const neighbors = this.countNeighbors(x, y);
                const currentCell = this.grid[y][x];
                
                // Conway's rules
                if (currentCell !== this.EMPTY) {
                    // Alive cell - survives with 2-3 neighbors
                    if (neighbors.total === 2 || neighbors.total === 3) {
                        newGrid[y][x] = currentCell;
                    }
                } else {
                    // Dead cell - becomes alive with exactly 3 neighbors
                    if (neighbors.total === 3) {
                        // Majority rule: new cell takes color of majority neighbors
                        if (neighbors.player1 > neighbors.player2) {
                            newGrid[y][x] = this.PLAYER1;
                        } else if (neighbors.player2 > neighbors.player1) {
                            newGrid[y][x] = this.PLAYER2;
                        } else {
                            // Tie - randomly choose (or could use other rules)
                            newGrid[y][x] = Math.random() < 0.5 ? this.PLAYER1 : this.PLAYER2;
                        }
                    }
                }
            }
        }
        
        this.grid = newGrid;
        this.generation++;
        return this.grid;
    }
    
    countCells() {
        let player1Count = 0;
        let player2Count = 0;
        
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                if (this.grid[y][x] === this.PLAYER1) player1Count++;
                if (this.grid[y][x] === this.PLAYER2) player2Count++;
            }
        }
        
        return { player1: player1Count, player2: player2Count };
    }
    
    clear() {
        this.initGrid();
    }
    
    getGridSnapshot() {
        return this.grid.map(row => row.join('')).join('');
    }
    
    getState() {
        return {
            grid: this.grid,
            generation: this.generation,
            gridSize: this.gridSize,
            cellCounts: this.countCells()
        };
    }
}