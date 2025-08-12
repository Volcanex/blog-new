/**
 * Canvas Renderer - Handles visual rendering of the Immigration Game grid
 * Responsible for drawing the grid, cells, and visual effects
 */

class ConwayRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.cellSize = 0;
        this.gridSize = 32;
        
        // Colors for Immigration mode
        this.COLORS = {
            0: '#0d1117',    // Empty
            1: '#58a6ff',    // Player 1 (Blue)
            2: '#ff7b72'     // Player 2 (Red)
        };
        
        this.GRID_COLOR = '#333333';
        this.CELL_BORDER_COLOR = '#30363d';
        
        this.resizeCanvas();
    }
    
    
    updatePlayerColors(player1Hex, player2Hex) {
        this.COLORS[1] = player1Hex;
        this.COLORS[2] = player2Hex;
    }
    
    setGridSize(gridSize) {
        this.gridSize = gridSize;
        this.resizeCanvas();
    }
    
    resizeCanvas() {
        const maxSize = Math.min(800, window.innerWidth - 100);
        this.cellSize = Math.floor(maxSize / this.gridSize);
        
        this.canvas.width = this.gridSize * this.cellSize;
        this.canvas.height = this.gridSize * this.cellSize;
        
        // Update canvas style for better mobile display
        this.canvas.style.width = this.canvas.width + 'px';
        this.canvas.style.height = this.canvas.height + 'px';
    }
    
    renderCell(x, y, cellValue) {
        const color = this.COLORS[cellValue] || this.COLORS[0];
        
        this.ctx.fillStyle = color;
        this.ctx.fillRect(x * this.cellSize, y * this.cellSize, this.cellSize, this.cellSize);
        
        // Add border for non-empty cells
        if (cellValue !== 0) {
            this.ctx.strokeStyle = this.CELL_BORDER_COLOR;
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(x * this.cellSize, y * this.cellSize, this.cellSize, this.cellSize);
        }
    }
    
    render(grid) {
        // Clear canvas
        this.ctx.fillStyle = this.COLORS[0];
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw grid lines (subtle)
        this.ctx.strokeStyle = this.GRID_COLOR;
        this.ctx.lineWidth = 0.5;
        
        for (let i = 0; i <= this.gridSize; i++) {
            this.ctx.beginPath();
            this.ctx.moveTo(i * this.cellSize, 0);
            this.ctx.lineTo(i * this.cellSize, this.canvas.height);
            this.ctx.stroke();
            
            this.ctx.beginPath();
            this.ctx.moveTo(0, i * this.cellSize);
            this.ctx.lineTo(this.canvas.width, i * this.cellSize);
            this.ctx.stroke();
        }
        
        // Draw cells
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                const cellValue = grid[y][x];
                if (cellValue !== 0) {
                    this.renderCell(x, y, cellValue);
                }
            }
        }
    }
    
    getMousePos(e) {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.canvas.width / rect.width;
        const scaleY = this.canvas.height / rect.height;
        
        return {
            x: Math.floor((e.clientX - rect.left) * scaleX / this.cellSize),
            y: Math.floor((e.clientY - rect.top) * scaleY / this.cellSize)
        };
    }
    
    getTouchPos(e) {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.canvas.width / rect.width;
        const scaleY = this.canvas.height / rect.height;
        
        const touch = e.touches[0];
        return {
            x: Math.floor((touch.clientX - rect.left) * scaleX / this.cellSize),
            y: Math.floor((touch.clientY - rect.top) * scaleY / this.cellSize)
        };
    }
    
    getCanvas() {
        return this.canvas;
    }
}