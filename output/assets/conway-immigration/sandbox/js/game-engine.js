/**
 * Conway's Immigration Game Engine - Core game logic and rules
 * Immigration Game: Two player Conway's Game of Life variant
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
        
        // History for reset functionality
        this.history = [];
        this.initialGrid = null;
        
        this.initGrid();
    }
    
    initGrid() {
        this.grid = Array(this.gridSize).fill().map(() => Array(this.gridSize).fill(this.EMPTY));
        this.generation = 0;
        this.history = [];
        this.initialGrid = null;
    }
    
    saveCurrentAsInitial() {
        // Save the current grid state as generation 0
        this.initialGrid = this.deepCopyGrid(this.grid);
        console.log('Saved initial state with', this.countCells().total, 'total cells');
    }
    
    deepCopyGrid(grid) {
        return grid.map(row => [...row]);
    }
    
    resetToInitialState() {
        if (this.initialGrid) {
            this.grid = this.deepCopyGrid(this.initialGrid);
            this.generation = 0;
            console.log('Reset to initial state with', this.countCells().total, 'total cells');
            return true;
        }
        console.log('No initial state saved yet');
        return false;
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
                    const neighborValue = this.grid[ny][nx];
                    if (neighborValue === this.PLAYER1) player1Neighbors++;
                    if (neighborValue === this.PLAYER2) player2Neighbors++;
                }
            }
        }
        
        return { 
            player1: player1Neighbors, 
            player2: player2Neighbors, 
            total: player1Neighbors + player2Neighbors 
        };
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
                        // Immigration mode - majority rule
                        if (neighbors.player1 > neighbors.player2) {
                            newGrid[y][x] = this.PLAYER1;
                        } else if (neighbors.player2 > neighbors.player1) {
                            newGrid[y][x] = this.PLAYER2;
                        } else {
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
        let totalAlive = 0;
        
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                const cellValue = this.grid[y][x];
                if (cellValue === this.PLAYER1) {
                    player1Count++;
                    totalAlive++;
                }
                if (cellValue === this.PLAYER2) {
                    player2Count++;
                    totalAlive++;
                }
            }
        }
        
        return { player1: player1Count, player2: player2Count, total: totalAlive };
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