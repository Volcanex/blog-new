<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    background: #0d1117;
    color: #c9d1d9;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    line-height: 1.4;
}

.container {
    max-width: 1200px;
    padding: 20px;
    margin: 0 auto;
}

.header {
    text-align: center;
    margin-bottom: 2rem;
}

.title {
    color: #58a6ff;
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    text-shadow: 0 0 10px rgba(88, 166, 255, 0.3);
}

.subtitle {
    color: #7d8590;
    font-size: 1.1rem;
}

.setup-screen, .game-screen {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.setup-screen {
    max-width: 600px;
    margin: 0 auto;
}

.input-group {
    margin-bottom: 1.5rem;
}

.input-group label {
    display: block;
    color: #c9d1d9;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.input {
    width: 100%;
    padding: 12px 16px;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    color: #c9d1d9;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    transition: all 0.2s ease;
}

.input:focus {
    outline: none;
    border-color: #58a6ff;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.3);
}

.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-primary {
    background: #238636;
    color: white;
}

.btn-primary:hover {
    background: #2ea043;
}

.btn-secondary {
    background: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
}

.btn-secondary:hover {
    background: #30363d;
}

.btn-danger {
    background: #da3633;
    color: white;
}

.btn-danger:hover {
    background: #f85149;
}

.player-list {
    list-style: none;
    padding: 0;
    margin: 1rem 0;
}

.player-item {
    background: #0d1117;
    padding: 12px 16px;
    margin-bottom: 8px;
    border-radius: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #30363d;
}

.player-item .name {
    font-weight: 500;
    color: #58a6ff;
}

.scoreboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.player-card {
    background: #21262d;
    border: 2px solid #30363d;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
}

.player-card.active {
    border-color: #238636;
    box-shadow: 0 0 20px rgba(35, 134, 54, 0.3);
}

.player-card.winner {
    border-color: #f0c800;
    box-shadow: 0 0 20px rgba(240, 200, 0, 0.3);
}

.player-card .player-name {
    font-size: 1.5rem;
    font-weight: 700;
    color: #58a6ff;
    margin-bottom: 0.5rem;
}

.player-card.active .player-name {
    color: #3fb950;
}

.player-card .player-score {
    font-size: 3rem;
    font-weight: 800;
    color: #c9d1d9;
    margin-bottom: 0.5rem;
}

.player-card .last-word {
    font-size: 0.9rem;
    color: #7d8590;
    font-style: italic;
    min-height: 20px;
}

.controls {
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.quick-score {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    align-items: flex-end;
    margin-bottom: 1rem;
}

.quick-score .input-group {
    flex: 1;
    min-width: 200px;
    margin-bottom: 0;
}

.word-checker {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #30363d;
}

.word-checker-result {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 8px;
    font-weight: 500;
    display: none;
}

.word-checker-result.valid {
    background: rgba(35, 134, 54, 0.2);
    border: 1px solid #238636;
    color: #3fb950;
    display: block;
}

.word-checker-result.invalid {
    background: rgba(218, 54, 51, 0.2);
    border: 1px solid #da3633;
    color: #f85149;
    display: block;
}

.action-buttons {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.score-history {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.5rem;
    max-height: 300px;
    overflow-y: auto;
}

.score-history h3 {
    margin-top: 0;
    color: #58a6ff;
}

.history-item {
    padding: 8px 12px;
    background: #21262d;
    border-radius: 6px;
    margin-bottom: 8px;
    font-size: 0.95rem;
}

.history-item .player {
    color: #58a6ff;
    font-weight: 500;
}

.history-item .word {
    color: #3fb950;
    font-weight: 600;
}

.history-item .points {
    color: #c9d1d9;
    font-weight: 700;
}

.hidden {
    display: none;
}

@media (max-width: 768px) {
    .title {
        font-size: 2rem;
    }

    .scoreboard {
        grid-template-columns: 1fr;
    }

    .quick-score {
        flex-direction: column;
    }

    .quick-score .input-group {
        width: 100%;
    }
}
</style>

<div class="container">
    <div class="header">
        <h1 class="title">🎲 Scrabble Tracker</h1>
        <p class="subtitle">Track scores and validate words</p>
    </div>

    <!-- Setup Screen -->
    <div id="setupScreen" class="setup-screen">
        <div class="input-group">
            <label for="playerName">Enter Player Names</label>
            <input type="text" id="playerName" class="input" placeholder="Enter player name and press Enter">
        </div>

        <ul id="playerList" class="player-list"></ul>

        <button id="startGame" class="btn btn-primary" style="width: 100%;" disabled>Start Game</button>
    </div>

    <!-- Game Screen -->
    <div id="gameScreen" class="game-screen hidden">
        <div class="scoreboard" id="scoreboard"></div>

        <div class="controls">
            <h3 style="margin-top: 0; color: #58a6ff;">Quick Score Entry</h3>
            <div class="quick-score">
                <div class="input-group">
                    <label for="wordInput">Word Played</label>
                    <input type="text" id="wordInput" class="input" placeholder="Enter word">
                </div>
                <div class="input-group">
                    <label for="pointsInput">Points</label>
                    <input type="number" id="pointsInput" class="input" placeholder="Points">
                </div>
                <button id="addScore" class="btn btn-primary">Add Score</button>
            </div>

            <div class="word-checker">
                <h4 style="margin-top: 0; color: #c9d1d9;">Word Validator</h4>
                <div style="display: flex; gap: 1rem;">
                    <input type="text" id="checkWord" class="input" placeholder="Check if word is valid" style="flex: 1;">
                    <button id="validateWord" class="btn btn-secondary">Check Word</button>
                </div>
                <div id="wordResult" class="word-checker-result"></div>
            </div>

            <div class="action-buttons">
                <button id="nextPlayer" class="btn btn-secondary">Skip Turn</button>
                <button id="undoLast" class="btn btn-secondary">Undo Last</button>
                <button id="endGame" class="btn btn-danger">End Game</button>
            </div>
        </div>

        <div class="score-history">
            <h3>Score History</h3>
            <div id="historyList"></div>
        </div>
    </div>
</div>

<script>
// Game state
const state = {
    players: [],
    currentPlayerIndex: 0,
    history: [],
    gameStarted: false
};

// Setup screen elements
const setupScreen = document.getElementById('setupScreen');
const gameScreen = document.getElementById('gameScreen');
const playerNameInput = document.getElementById('playerName');
const playerList = document.getElementById('playerList');
const startGameBtn = document.getElementById('startGame');

// Game screen elements
const scoreboard = document.getElementById('scoreboard');
const wordInput = document.getElementById('wordInput');
const pointsInput = document.getElementById('pointsInput');
const addScoreBtn = document.getElementById('addScore');
const checkWordInput = document.getElementById('checkWord');
const validateWordBtn = document.getElementById('validateWord');
const wordResult = document.getElementById('wordResult');
const nextPlayerBtn = document.getElementById('nextPlayer');
const undoLastBtn = document.getElementById('undoLast');
const endGameBtn = document.getElementById('endGame');
const historyList = document.getElementById('historyList');

// Add player on Enter
playerNameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && playerNameInput.value.trim()) {
        addPlayer(playerNameInput.value.trim());
        playerNameInput.value = '';
    }
});

function addPlayer(name) {
    if (state.players.some(p => p.name.toLowerCase() === name.toLowerCase())) {
        alert('Player already exists!');
        return;
    }

    state.players.push({
        name: name,
        score: 0,
        lastWord: ''
    });

    updatePlayerList();
    startGameBtn.disabled = state.players.length < 2;
}

function updatePlayerList() {
    playerList.innerHTML = state.players.map((player, index) => `
        <li class="player-item">
            <span class="name">${player.name}</span>
            <button onclick="removePlayer(${index})" class="btn btn-danger" style="padding: 6px 12px; font-size: 0.85rem;">Remove</button>
        </li>
    `).join('');
}

function removePlayer(index) {
    state.players.splice(index, 1);
    updatePlayerList();
    startGameBtn.disabled = state.players.length < 2;
}

// Start game
startGameBtn.addEventListener('click', () => {
    state.gameStarted = true;
    state.currentPlayerIndex = 0;
    setupScreen.classList.add('hidden');
    gameScreen.classList.remove('hidden');
    updateScoreboard();
    wordInput.focus();
});

function updateScoreboard() {
    const maxScore = Math.max(...state.players.map(p => p.score), 0);

    scoreboard.innerHTML = state.players.map((player, index) => {
        const isActive = index === state.currentPlayerIndex;
        const isWinner = state.players.length > 1 && player.score === maxScore && maxScore > 0;

        return `
            <div class="player-card ${isActive ? 'active' : ''} ${isWinner && !isActive ? 'winner' : ''}">
                <div class="player-name">${player.name}${isActive ? ' ⬅️' : ''}</div>
                <div class="player-score">${player.score}</div>
                <div class="last-word">${player.lastWord ? `"${player.lastWord}"` : ''}</div>
            </div>
        `;
    }).join('');
}

// Add score
addScoreBtn.addEventListener('click', addScore);
pointsInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addScore();
});
wordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') pointsInput.focus();
});

async function addScore() {
    const word = wordInput.value.trim();
    const points = parseInt(pointsInput.value);

    if (!points || points < 0) {
        alert('Please enter valid points');
        return;
    }

    const currentPlayer = state.players[state.currentPlayerIndex];

    // Validate word if entered
    if (word) {
        const isValid = await checkWordValidity(word);
        if (!isValid) {
            const proceed = confirm(`"${word}" is not in the dictionary. Add score anyway?`);
            if (!proceed) return;
        }
    }

    // Add to history
    state.history.push({
        player: currentPlayer.name,
        word: word,
        points: points,
        timestamp: new Date().toLocaleTimeString()
    });

    // Update player
    currentPlayer.score += points;
    currentPlayer.lastWord = word;

    // Move to next player
    state.currentPlayerIndex = (state.currentPlayerIndex + 1) % state.players.length;

    // Clear inputs
    wordInput.value = '';
    pointsInput.value = '';

    updateScoreboard();
    updateHistory();
    wordInput.focus();
}

function updateHistory() {
    historyList.innerHTML = state.history.slice().reverse().map(entry => `
        <div class="history-item">
            <span class="player">${entry.player}</span>
            ${entry.word ? `played <span class="word">${entry.word}</span>` : ''}
            for <span class="points">+${entry.points}</span> points
            <span style="color: #7d8590; font-size: 0.85rem; margin-left: 8px;">${entry.timestamp}</span>
        </div>
    `).join('') || '<p style="color: #7d8590;">No moves yet</p>';
}

// Word validation
validateWordBtn.addEventListener('click', async () => {
    const word = checkWordInput.value.trim();
    if (!word) return;

    const isValid = await checkWordValidity(word);

    if (isValid) {
        wordResult.className = 'word-checker-result valid';
        wordResult.textContent = `✓ "${word.toUpperCase()}" is a valid Scrabble word!`;
    } else {
        wordResult.className = 'word-checker-result invalid';
        wordResult.textContent = `✗ "${word.toUpperCase()}" is not in the dictionary`;
    }
});

checkWordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') validateWordBtn.click();
});

async function checkWordValidity(word) {
    try {
        const response = await fetch(`/api/scrabble-tracker/check-word?word=${encodeURIComponent(word.toLowerCase())}`);
        const data = await response.json();
        return data.valid;
    } catch (error) {
        console.error('Error checking word:', error);
        return false;
    }
}

// Next player
nextPlayerBtn.addEventListener('click', () => {
    state.currentPlayerIndex = (state.currentPlayerIndex + 1) % state.players.length;
    updateScoreboard();
});

// Undo last
undoLastBtn.addEventListener('click', () => {
    if (state.history.length === 0) {
        alert('No moves to undo!');
        return;
    }

    const lastMove = state.history.pop();
    const player = state.players.find(p => p.name === lastMove.player);

    if (player) {
        player.score -= lastMove.points;
        // Go back one player
        state.currentPlayerIndex = (state.currentPlayerIndex - 1 + state.players.length) % state.players.length;

        // Update last word
        const playerHistory = state.history.filter(h => h.player === player.name);
        player.lastWord = playerHistory.length > 0 ? playerHistory[playerHistory.length - 1].word : '';
    }

    updateScoreboard();
    updateHistory();
});

// End game
endGameBtn.addEventListener('click', () => {
    if (confirm('Are you sure you want to end the game?')) {
        const winner = state.players.reduce((max, player) =>
            player.score > max.score ? player : max
        , state.players[0]);

        alert(`Game Over!\n\n🏆 Winner: ${winner.name}\n📊 Final Score: ${winner.score} points`);

        // Reset
        state.players = [];
        state.currentPlayerIndex = 0;
        state.history = [];
        state.gameStarted = false;

        setupScreen.classList.remove('hidden');
        gameScreen.classList.add('hidden');
        updatePlayerList();
        startGameBtn.disabled = true;
    }
});

// Focus on word input when game starts
wordInput.focus();
</script>
