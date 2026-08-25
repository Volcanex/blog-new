<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    color: #e6edf3;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    line-height: 1.5;
}

.container {
    max-width: 560px;
    padding: 20px;
    margin: 0 auto;
}

h1 {
    color: #58a6ff;
    font-size: 2.2rem;
    font-weight: 800;
    text-align: center;
    margin: 1.5rem 0 0.5rem;
    letter-spacing: -0.5px;
}

.subtitle {
    text-align: center;
    color: #8b949e;
    margin-bottom: 2rem;
    font-size: 0.95rem;
}

.screen { display: none; }
.screen.active { display: block; }

/* Cards */
.card {
    background: rgba(22, 27, 34, 0.8);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}

/* Buttons */
.btn {
    display: block;
    width: 100%;
    padding: 14px 20px;
    border: none;
    border-radius: 10px;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
    text-align: center;
}
.btn + .btn { margin-top: 0.75rem; }
.btn-primary {
    background: #238636;
    color: #fff;
}
.btn-primary:hover { background: #2ea043; }
.btn-primary:active { transform: scale(0.98); }
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-secondary {
    background: rgba(88, 166, 255, 0.1);
    color: #58a6ff;
    border: 1px solid rgba(88, 166, 255, 0.3);
}
.btn-secondary:hover { background: rgba(88, 166, 255, 0.18); }
.btn-danger {
    background: rgba(248, 81, 73, 0.1);
    color: #f85149;
    border: 1px solid rgba(248, 81, 73, 0.3);
}
.btn-danger:hover { background: rgba(248, 81, 73, 0.18); }
.btn-sm {
    display: inline-block;
    width: auto;
    padding: 6px 14px;
    font-size: 0.85rem;
}

/* Inputs */
.input-group { margin-bottom: 1rem; }
.input-group label {
    display: block;
    color: #8b949e;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.input-group input {
    width: 100%;
    padding: 10px 14px;
    background: rgba(13, 17, 23, 0.8);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 8px;
    color: #e6edf3;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    transition: border-color 0.15s;
}
.input-group input:focus {
    outline: none;
    border-color: #58a6ff;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
}
.input-group input::placeholder { color: #484f58; }

/* ===== HOME SCREEN ===== */
.home-title { margin-bottom: 1.5rem; }

.game-list { margin-bottom: 1rem; }
.game-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.25rem;
    background: rgba(22, 27, 34, 0.8);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 12px;
    margin-bottom: 0.6rem;
    cursor: pointer;
    transition: all 0.15s;
}
.game-item:hover {
    border-color: rgba(88, 166, 255, 0.4);
    background: rgba(88, 166, 255, 0.05);
}
.game-item-info {}
.game-item-name {
    font-weight: 700;
    font-size: 1rem;
    color: #e6edf3;
}
.game-item-meta {
    font-size: 0.8rem;
    color: #8b949e;
    margin-top: 2px;
}
.game-item-actions {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}
.game-item-score {
    font-size: 0.9rem;
    font-weight: 700;
    color: #58a6ff;
}
.delete-btn {
    background: none;
    border: none;
    color: #484f58;
    cursor: pointer;
    padding: 4px 6px;
    border-radius: 6px;
    font-size: 1rem;
    line-height: 1;
    transition: all 0.15s;
}
.delete-btn:hover { color: #f85149; background: rgba(248, 81, 73, 0.1); }

.empty-state {
    text-align: center;
    padding: 2rem;
    color: #484f58;
    font-size: 0.95rem;
}

/* ===== SETUP SCREEN ===== */
.back-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #8b949e;
    font-size: 0.9rem;
    cursor: pointer;
    margin-bottom: 1.5rem;
    border: none;
    background: none;
    padding: 0;
    transition: color 0.15s;
}
.back-btn:hover { color: #58a6ff; }

.players-setup-list { margin-bottom: 1rem; }
.player-setup-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}
.player-setup-row input {
    flex: 1;
    padding: 10px 14px;
    background: rgba(13, 17, 23, 0.8);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 8px;
    color: #e6edf3;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    transition: border-color 0.15s;
}
.player-setup-row input:focus {
    outline: none;
    border-color: #58a6ff;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
}
.remove-player-btn {
    background: none;
    border: none;
    color: #484f58;
    cursor: pointer;
    padding: 8px;
    border-radius: 6px;
    font-size: 1.1rem;
    line-height: 1;
    transition: all 0.15s;
    flex-shrink: 0;
}
.remove-player-btn:hover { color: #f85149; background: rgba(248, 81, 73, 0.1); }

.add-player-btn {
    background: none;
    border: 1px dashed rgba(88, 166, 255, 0.3);
    border-radius: 8px;
    color: #58a6ff;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    padding: 10px;
    width: 100%;
    margin-bottom: 1rem;
    transition: all 0.15s;
}
.add-player-btn:hover { background: rgba(88, 166, 255, 0.08); }

/* ===== GAME SCREEN ===== */
.game-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}
.game-title {
    font-size: 1.3rem;
    font-weight: 700;
}
.round-badge {
    background: rgba(88, 166, 255, 0.15);
    color: #58a6ff;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.8rem;
    font-weight: 700;
}

/* Scoreboard */
.scoreboard { margin-bottom: 1rem; }
.score-row {
    display: flex;
    align-items: center;
    padding: 0.9rem 1.25rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    background: rgba(22, 27, 34, 0.6);
    border: 1px solid rgba(48, 54, 61, 0.6);
    transition: all 0.2s;
}
.score-row.leader {
    background: rgba(35, 134, 54, 0.1);
    border-color: rgba(35, 134, 54, 0.4);
}
.score-row.out {
    opacity: 0.45;
}
.score-rank {
    font-size: 0.85rem;
    font-weight: 700;
    color: #484f58;
    width: 28px;
    flex-shrink: 0;
}
.score-row.leader .score-rank { color: #3fb950; }
.score-name {
    flex: 1;
    font-weight: 600;
    font-size: 1rem;
}
.score-total {
    font-size: 1.4rem;
    font-weight: 800;
    color: #58a6ff;
    min-width: 50px;
    text-align: right;
}
.score-row.leader .score-total { color: #3fb950; }
.score-row.out .score-total { color: #f85149; }
.score-out-label {
    font-size: 0.75rem;
    color: #f85149;
    font-weight: 700;
    margin-left: 8px;
}

/* Rounds history */
.rounds-section { margin-top: 1rem; }
.rounds-toggle {
    background: none;
    border: none;
    color: #8b949e;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    cursor: pointer;
    padding: 0;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 4px;
}
.rounds-toggle:hover { color: #58a6ff; }
.rounds-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    display: none;
}
.rounds-table.visible { display: table; }
.rounds-table th {
    color: #8b949e;
    font-weight: 600;
    text-align: right;
    padding: 6px 10px;
    border-bottom: 1px solid rgba(48, 54, 61, 0.6);
}
.rounds-table th:first-child { text-align: left; }
.rounds-table td {
    text-align: right;
    padding: 6px 10px;
    border-bottom: 1px solid rgba(48, 54, 61, 0.3);
    color: #8b949e;
}
.rounds-table td:first-child {
    text-align: left;
    color: #484f58;
}
.rounds-table tr:last-child td { border-bottom: none; }
.rounds-table .cambio-round td { color: #ffa657; }

/* Add round modal */
.modal-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    z-index: 100;
    align-items: center;
    justify-content: center;
    padding: 20px;
}
.modal-overlay.open { display: flex; }
.modal {
    background: #161b22;
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 16px;
    padding: 1.5rem;
    width: 100%;
    max-width: 420px;
    max-height: 90vh;
    overflow-y: auto;
}
.modal h2 {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
    color: #e6edf3;
}
.score-input-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}
.score-input-row label {
    flex: 1;
    font-weight: 600;
    font-size: 0.95rem;
}
.score-input-row input[type="number"] {
    width: 90px;
    flex-shrink: 0;
    padding: 10px 12px;
    background: rgba(13, 17, 23, 0.8);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 8px;
    color: #e6edf3;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
    transition: border-color 0.15s;
}
.score-input-row input[type="number"]:focus {
    outline: none;
    border-color: #58a6ff;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
}
.cambio-caller-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 0;
    border-top: 1px solid rgba(48, 54, 61, 0.4);
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}
.cambio-caller-row label {
    font-size: 0.9rem;
    color: #8b949e;
    flex: 1;
}
.cambio-caller-row select {
    padding: 8px 10px;
    background: rgba(13, 17, 23, 0.8);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 8px;
    color: #e6edf3;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
}
.modal-buttons {
    display: flex;
    gap: 0.75rem;
    margin-top: 1rem;
}
.modal-buttons .btn { margin: 0; flex: 1; }

/* Winner screen */
.winner-card {
    text-align: center;
    padding: 2.5rem 1.5rem;
}
.winner-trophy { font-size: 4rem; margin-bottom: 1rem; }
.winner-label { color: #8b949e; font-size: 0.9rem; margin-bottom: 0.5rem; }
.winner-name { font-size: 2.5rem; font-weight: 800; color: #ffa657; margin-bottom: 0.5rem; }
.winner-score { font-size: 1.2rem; color: #8b949e; margin-bottom: 2rem; }

/* Stakes */
.score-cost {
    font-size: 0.75rem;
    color: #8b949e;
    font-weight: 500;
    margin-top: 1px;
    text-align: right;
}
.score-row.out .score-cost { color: #f85149; }
.settlement-list { margin-top: 1rem; }
.settlement-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 1.25rem;
    border-radius: 8px;
    margin-bottom: 0.4rem;
    background: rgba(22, 27, 34, 0.6);
    border: 1px solid rgba(48, 54, 61, 0.5);
    font-size: 0.9rem;
}
.settlement-row .pays { color: #8b949e; }
.settlement-row .amount { font-weight: 700; color: #ffa657; }

@media (max-width: 480px) {
    h1 { font-size: 1.8rem; }
    .score-total { font-size: 1.2rem; }
}
</style>

<html>
<div class="container">
    <h1>Cambio</h1>
    <p class="subtitle">Points tracker</p>

    <!-- HOME: list of saved games -->
    <div id="homeScreen" class="screen active">
        <div id="gameList" class="game-list"></div>
        <button class="btn btn-primary" onclick="goToSetup()">+ New Game</button>
    </div>

    <!-- SETUP: configure new game -->
    <div id="setupScreen" class="screen">
        <button class="back-btn" onclick="goHome()">← Back</button>
        <div class="card">
            <div class="input-group">
                <label>Game Name (optional)</label>
                <input type="text" id="setupGameName" placeholder="e.g. Sunday Night Cambio" />
            </div>
            <div class="input-group">
                <label>Point Limit</label>
                <input type="number" id="setupThreshold" value="100" min="50" max="500" step="50" />
            </div>
            <div class="input-group">
                <label>Stake — pence per point (optional)</label>
                <input type="number" id="setupStake" min="0" max="100" step="0.5" placeholder="e.g. 5" />
            </div>
        </div>
        <div class="card">
            <div style="color:#8b949e;font-size:0.85rem;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:0.75rem;">Players</div>
            <div id="playersSetupList" class="players-setup-list"></div>
            <button class="add-player-btn" onclick="addPlayerRow()">+ Add Player</button>
        </div>
        <button class="btn btn-primary" id="createGameBtn" onclick="createGame()" disabled>Start Game</button>
    </div>

    <!-- GAME: active scoreboard -->
    <div id="gameScreen" class="screen">
        <button class="back-btn" onclick="goHome()">← All Games</button>
        <div class="game-header">
            <div class="game-title" id="gameScreenTitle"></div>
            <div class="round-badge" id="roundBadge">Round 0</div>
        </div>

        <div id="scoreboard" class="scoreboard"></div>

        <button class="btn btn-primary" id="addRoundBtn" onclick="openAddRound()">+ Add Round</button>
        <button class="btn btn-secondary" style="margin-top:0.75rem;" onclick="promptDeleteGame()">Delete Game</button>

        <div class="rounds-section">
            <button class="rounds-toggle" onclick="toggleRounds()">
                <span id="roundsToggleIcon">▶</span> Round History
            </button>
            <table class="rounds-table" id="roundsTable">
                <thead><tr id="roundsTableHeader"></tr></thead>
                <tbody id="roundsTableBody"></tbody>
            </table>
        </div>
    </div>

    <!-- WINNER screen -->
    <div id="winnerScreen" class="screen">
        <button class="back-btn" onclick="goHome()">← All Games</button>
        <div class="card winner-card">
            <div class="winner-trophy">🏆</div>
            <div class="winner-label">Winner</div>
            <div class="winner-name" id="winnerName"></div>
            <div class="winner-score" id="winnerScore"></div>
        </div>
        <div id="finalScoreboard" class="scoreboard"></div>
        <div id="settlementSection" style="display:none;">
            <div style="color:#8b949e;font-size:0.85rem;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin:1.25rem 0 0.5rem;">Settlement</div>
            <div id="settlementList" class="settlement-list"></div>
        </div>
        <button class="btn btn-secondary" style="margin-top:1rem;" onclick="promptDeleteGame()">Delete Game</button>
    </div>
</div>

<!-- Add Round Modal -->
<div class="modal-overlay" id="addRoundModal">
    <div class="modal">
        <h2>Add Round</h2>
        <div id="roundScoreInputs"></div>
        <div class="cambio-caller-row">
            <label>Who called Cambio?</label>
            <select id="cambioCaller">
                <option value="">— nobody —</option>
            </select>
        </div>
        <div class="modal-buttons">
            <button class="btn btn-secondary" onclick="closeAddRound()">Cancel</button>
            <button class="btn btn-primary" onclick="submitRound()">Save Round</button>
        </div>
    </div>
</div>

<script>
const STORAGE_KEY = 'cambio_games_v1';

// ── Storage ──────────────────────────────────────────────────────────────────

function loadGames() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch { return []; }
}

function saveGames(games) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(games));
}

function getGame(id) {
    return loadGames().find(g => g.id === id);
}

function updateGame(updated) {
    const games = loadGames();
    const idx = games.findIndex(g => g.id === updated.id);
    if (idx !== -1) games[idx] = updated;
    saveGames(games);
}

// ── State ─────────────────────────────────────────────────────────────────────

let activeGameId = null;
let roundsVisible = false;

// ── Screens ───────────────────────────────────────────────────────────────────

function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

function goHome() {
    activeGameId = null;
    roundsVisible = false;
    renderHome();
    showScreen('homeScreen');
}

function goToSetup() {
    renderSetup();
    showScreen('setupScreen');
}

// ── Home ──────────────────────────────────────────────────────────────────────

function renderHome() {
    const games = loadGames();
    const list = document.getElementById('gameList');

    if (!games.length) {
        list.innerHTML = '<div class="empty-state">No games yet. Start one!</div>';
        return;
    }

    list.innerHTML = games.map(g => {
        const totals = playerTotals(g);
        const leader = g.players[totals.indexOf(Math.min(...totals))];
        const roundCount = g.rounds.length;
        return `
            <div class="game-item" onclick="openGame('${g.id}')">
                <div class="game-item-info">
                    <div class="game-item-name">${esc(g.name)}</div>
                    <div class="game-item-meta">${roundCount} round${roundCount !== 1 ? 's' : ''} · limit ${g.threshold} · leading: ${esc(leader)}</div>
                </div>
                <div class="game-item-actions">
                    <span class="game-item-score">${Math.min(...totals)}</span>
                    <button class="delete-btn" onclick="event.stopPropagation(); deleteGame('${g.id}')">✕</button>
                </div>
            </div>
        `;
    }).join('');
}

function deleteGame(id) {
    if (!confirm('Delete this game?')) return;
    const games = loadGames().filter(g => g.id !== id);
    saveGames(games);
    renderHome();
}

function promptDeleteGame() {
    if (!confirm('Delete this game?')) return;
    const games = loadGames().filter(g => g.id !== activeGameId);
    saveGames(games);
    goHome();
}

// ── Setup ─────────────────────────────────────────────────────────────────────

function renderSetup() {
    document.getElementById('setupGameName').value = '';
    document.getElementById('setupThreshold').value = '100';
    const list = document.getElementById('playersSetupList');
    list.innerHTML = '';
    ['', '', ''].forEach(() => addPlayerRow());
    validateSetup();
}

function addPlayerRow() {
    const list = document.getElementById('playersSetupList');
    const row = document.createElement('div');
    row.className = 'player-setup-row';
    const idx = list.children.length + 1;
    row.innerHTML = `
        <input type="text" placeholder="Player ${idx}" oninput="validateSetup()" />
        <button class="remove-player-btn" onclick="removePlayerRow(this)">✕</button>
    `;
    list.appendChild(row);
    validateSetup();
}

function removePlayerRow(btn) {
    btn.parentElement.remove();
    validateSetup();
}

function validateSetup() {
    const names = getSetupPlayerNames();
    document.getElementById('createGameBtn').disabled = names.length < 2;
}

function getSetupPlayerNames() {
    return Array.from(document.querySelectorAll('#playersSetupList input'))
        .map(i => i.value.trim()).filter(Boolean);
}

function createGame() {
    const players = getSetupPlayerNames();
    if (players.length < 2) return;

    const name = document.getElementById('setupGameName').value.trim()
        || players.join(', ');
    const threshold = parseInt(document.getElementById('setupThreshold').value) || 100;

    const stakeVal = parseFloat(document.getElementById('setupStake').value);
    const stake = isNaN(stakeVal) || stakeVal <= 0 ? 0 : stakeVal;

    const game = {
        id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
        name,
        players,
        threshold,
        stake,
        rounds: [],
        created: Date.now(),
    };

    const games = loadGames();
    games.push(game);
    saveGames(games);

    openGame(game.id);
}

// ── Game ──────────────────────────────────────────────────────────────────────

function openGame(id) {
    activeGameId = id;
    roundsVisible = false;
    renderGame();
    const game = getGame(id);
    if (isGameOver(game)) {
        showScreen('winnerScreen');
    } else {
        showScreen('gameScreen');
    }
}

function playerTotals(game) {
    return game.players.map((_, pi) =>
        game.rounds.reduce((sum, r) => sum + (r.scores[pi] || 0), 0)
    );
}

function isGameOver(game) {
    if (!game.rounds.length) return false;
    const totals = playerTotals(game);
    return totals.some(t => t >= game.threshold);
}

function renderGame() {
    const game = getGame(activeGameId);
    if (!game) return;

    const totals = playerTotals(game);
    const over = isGameOver(game);

    // Header
    document.getElementById('gameScreenTitle').textContent = game.name;
    document.getElementById('roundBadge').textContent = `Round ${game.rounds.length}`;

    // Scoreboard
    const ranked = game.players.map((p, i) => ({ name: p, total: totals[i], idx: i }))
        .sort((a, b) => a.total - b.total);

    const sb = document.getElementById('scoreboard');
    sb.innerHTML = ranked.map((p, rank) => {
        const isLeader = rank === 0;
        const isOut = p.total >= game.threshold;
        const costLine = game.stake > 0
            ? `<div class="score-cost">${formatPence(p.total * game.stake)}</div>`
            : '';
        return `
            <div class="score-row${isLeader && !over ? ' leader' : ''}${isOut ? ' out' : ''}">
                <div class="score-rank">${rank + 1}</div>
                <div class="score-name">${esc(p.name)}</div>
                ${isOut ? '<span class="score-out-label">OUT</span>' : ''}
                <div>
                    <div class="score-total">${p.total}</div>
                    ${costLine}
                </div>
            </div>
        `;
    }).join('');

    // Add round button
    const btn = document.getElementById('addRoundBtn');
    if (btn) btn.disabled = over;

    // Rounds history
    renderRoundsTable(game);

    // Winner screen
    if (over) {
        const winner = ranked.find(p => p.total < game.threshold) || ranked[0];
        document.getElementById('winnerName').textContent = winner.name;
        document.getElementById('winnerScore').textContent = `${winner.total} points`;
        document.getElementById('finalScoreboard').innerHTML = sb.innerHTML;

        const settlementSection = document.getElementById('settlementSection');
        const settlementList = document.getElementById('settlementList');
        if (game.stake > 0) {
            settlementSection.style.display = 'block';
            settlementList.innerHTML = ranked
                .filter(p => p.name !== winner.name)
                .map(p => {
                    const owes = (p.total - winner.total) * game.stake;
                    return `
                        <div class="settlement-row">
                            <span class="pays">${esc(p.name)} owes ${esc(winner.name)}</span>
                            <span class="amount">${formatPence(owes)}</span>
                        </div>
                    `;
                }).join('');
        } else {
            settlementSection.style.display = 'none';
        }
    }
}

function renderRoundsTable(game) {
    const header = document.getElementById('roundsTableHeader');
    const body = document.getElementById('roundsTableBody');

    header.innerHTML = '<th>#</th>' + game.players.map(p => `<th>${esc(p)}</th>`).join('');

    body.innerHTML = game.rounds.map((r, ri) => {
        const isCambio = r.cambio !== undefined && r.cambio !== '';
        return `<tr class="${isCambio ? 'cambio-round' : ''}">
            <td>${ri + 1}${isCambio ? ' ★' : ''}</td>
            ${r.scores.map(s => `<td>${s}</td>`).join('')}
        </tr>`;
    }).join('');

    const table = document.getElementById('roundsTable');
    if (roundsVisible) table.classList.add('visible');
    else table.classList.remove('visible');
}

function toggleRounds() {
    roundsVisible = !roundsVisible;
    document.getElementById('roundsToggleIcon').textContent = roundsVisible ? '▼' : '▶';
    document.getElementById('roundsTable').classList.toggle('visible', roundsVisible);
}

// ── Add Round Modal ───────────────────────────────────────────────────────────

function openAddRound() {
    const game = getGame(activeGameId);
    if (!game) return;

    // Build score inputs
    const inputs = document.getElementById('roundScoreInputs');
    inputs.innerHTML = game.players.map((p, i) => `
        <div class="score-input-row">
            <label>${esc(p)}</label>
            <input type="number" id="score_${i}" min="0" max="100" placeholder="0" />
        </div>
    `).join('');

    // Build cambio caller select
    const sel = document.getElementById('cambioCaller');
    sel.innerHTML = '<option value="">— nobody —</option>' +
        game.players.map((p, i) => `<option value="${i}">${esc(p)}</option>`).join('');

    document.getElementById('addRoundModal').classList.add('open');

    // Focus first input
    setTimeout(() => {
        const first = document.getElementById('score_0');
        if (first) first.focus();
    }, 50);
}

function closeAddRound() {
    document.getElementById('addRoundModal').classList.remove('open');
}

function submitRound() {
    const game = getGame(activeGameId);
    if (!game) return;

    const scores = game.players.map((_, i) => {
        const val = parseInt(document.getElementById(`score_${i}`).value);
        return isNaN(val) ? 0 : val;
    });

    const callerIdx = document.getElementById('cambioCaller').value;
    const round = { scores };
    if (callerIdx !== '') round.cambio = parseInt(callerIdx);

    game.rounds.push(round);
    updateGame(game);
    closeAddRound();

    renderGame();

    if (isGameOver(game)) {
        showScreen('winnerScreen');
    }
}

// Close modal on backdrop click
document.getElementById('addRoundModal').addEventListener('click', function(e) {
    if (e.target === this) closeAddRound();
});

// ── Utils ─────────────────────────────────────────────────────────────────────

function formatPence(p) {
    if (p < 100) return `${Math.round(p)}p`;
    return `£${(p / 100).toFixed(2)}`;
}

function esc(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

// ── Init ──────────────────────────────────────────────────────────────────────

renderHome();
</script>
</html>
