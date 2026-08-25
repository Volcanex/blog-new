<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Fraunces:ital,opsz,wght,SOFT@0,144,500,100;1,144,400,100&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --bg: #fcfaf3;
  --bg-sunk: #f5f1e4;
  --fg: #1a1a1a;
  --fg-muted: #6b6b6b;
  --fg-faint: #a0a0a0;
  --rule: #e8e2cf;
  --accent: #2d4a6b;
  --accent-alt: #a04628;

  --food-fill:   #ffd9c2;
  --food-ink:    #7a2e10;
  --food-border: #e8a07a;
  --act-fill:    #cfe1d0;
  --act-ink:     #2a4a30;
  --act-border:  #8db59a;

  --font-serif: 'Newsreader', Georgia, serif;
  --font-sans:  'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

  --measure: 680px;
  --gutter: 16px;
  --radius-1: 2px;
}

* { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

html, body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: var(--font-serif);
  font-size: 18px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  overscroll-behavior: none;
}

.page {
  max-width: var(--measure);
  margin: 0 auto;
  padding: 24px var(--gutter) 12px;
}

h1 {
  font-family: 'Fraunces', var(--font-serif);
  font-size: 40px;
  font-weight: 500;
  font-style: italic;
  font-variation-settings: 'opsz' 144, 'SOFT' 100;
  line-height: 1.05;
  margin: 0 0 2px;
  letter-spacing: -0.02em;
  color: var(--accent);
}

.sublabel {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--fg-muted);
  margin: 0 0 16px;
}

/* ----- entry form ----- */
.entry {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}
.entry input {
  flex: 1;
  font-family: var(--font-sans);
  font-size: 16px;
  color: var(--fg);
  background: #fff;
  border: 1px solid var(--rule);
  border-radius: 999px;
  padding: 12px 16px;
  min-width: 0;
}
.entry input:focus { outline: none; border-color: var(--accent); }
.entry button {
  font-family: var(--font-sans);
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  background: var(--accent);
  border: none;
  border-radius: 999px;
  padding: 0 18px;
  cursor: pointer;
}
.entry button:active { transform: scale(0.96); }

.kind-toggle {
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
  font-family: var(--font-sans);
  font-size: 13px;
}
.kind-toggle label {
  flex: 1;
  text-align: center;
  padding: 8px 10px;
  border: 1px solid var(--rule);
  border-radius: 999px;
  cursor: pointer;
  color: var(--fg-muted);
  background: #fff;
  font-weight: 500;
  user-select: none;
  transition: all 120ms ease;
}
.kind-toggle input { display: none; }
.kind-toggle input[value="food"]:checked + .pill-food {
  background: var(--food-fill);
  color: var(--food-ink);
  border-color: var(--food-border);
}
.kind-toggle input[value="activity"]:checked + .pill-act {
  background: var(--act-fill);
  color: var(--act-ink);
  border-color: var(--act-border);
}

/* ----- bubble canvas ----- */
#stage {
  position: relative;
  width: 100%;
  height: calc(100vh - 220px);
  min-height: 380px;
  background: var(--bg-sunk);
  border-radius: 14px;
  overflow: hidden;
  touch-action: manipulation;
}

.bubble {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-family: var(--font-sans);
  font-weight: 600;
  border-radius: 50%;
  border: 1.5px solid;
  padding: 6px;
  cursor: pointer;
  user-select: none;
  transition: transform 140ms cubic-bezier(.34,1.56,.64,1);
  word-break: break-word;
  hyphens: auto;
  line-height: 1.15;
  will-change: transform, left, top;
}
.bubble .label {
  display: block;
  overflow-wrap: anywhere;
  word-break: break-word;
  max-width: 90%;
}
.bubble .tally {
  display: flex;
  gap: 6px;
  align-items: center;
  justify-content: center;
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 500;
  margin-top: 3px;
  opacity: 0.75;
}
.bubble .tally svg { width: 11px; height: 11px; display: block; }
.bubble .tally span { display: inline-flex; align-items: center; gap: 2px; }
.bubble.food     { background: var(--food-fill); color: var(--food-ink); border-color: var(--food-border); }
.bubble.activity { background: var(--act-fill);  color: var(--act-ink);  border-color: var(--act-border); }
.bubble:active   { transform: scale(0.92); }
.bubble.pop      { animation: pop 360ms cubic-bezier(.34,1.56,.64,1); }
@keyframes pop {
  0%   { transform: scale(0); opacity: 0; }
  60%  { transform: scale(1.12); opacity: 1; }
  100% { transform: scale(1); }
}

.empty {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--fg-faint);
  text-align: center;
  padding: 20px;
  pointer-events: none;
}

/* ----- modal ----- */
.scrim {
  position: fixed; inset: 0;
  background: rgba(28, 30, 34, 0.32);
  display: none;
  align-items: flex-end;
  justify-content: center;
  z-index: 50;
  -webkit-backdrop-filter: blur(2px);
  backdrop-filter: blur(2px);
}
.scrim.open { display: flex; animation: fade 160ms ease; }
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }

.sheet {
  width: 100%;
  max-width: var(--measure);
  background: var(--bg);
  border-radius: 18px 18px 0 0;
  padding: 20px 20px 28px;
  animation: rise 220ms cubic-bezier(.34,1.56,.64,1);
}
@keyframes rise { from { transform: translateY(100%); } to { transform: translateY(0); } }

.sheet .kindlabel {
  display: inline-block;
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1.5px solid;
  margin-bottom: 12px;
}
.sheet .kindlabel.food     { background: var(--food-fill); color: var(--food-ink); border-color: var(--food-border); }
.sheet .kindlabel.activity { background: var(--act-fill);  color: var(--act-ink);  border-color: var(--act-border); }
.sheet .text {
  font-family: var(--font-serif);
  font-size: 24px;
  line-height: 1.25;
  margin-bottom: 4px;
}
.sheet .addedby {
  font-family: var(--font-sans);
  font-size: 12px;
  color: var(--fg-muted);
  margin-bottom: 18px;
}
.sheet .addedby strong { color: var(--fg); font-weight: 600; }

.vote-row {
  display: flex;
  gap: 10px;
  justify-content: stretch;
}
.vote-row button {
  flex: 1;
  border: none;
  border-radius: 999px;
  padding: 14px 12px;
  font-family: var(--font-sans);
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.vote-row button:active { transform: scale(0.97); }
.vote-row .yes  { background: #2a4a30; color: #cfe1d0; }
.vote-row .no   { background: #7a2e10; color: #ffd9c2; }
.voters {
  margin-top: 14px;
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--fg-muted);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.voters .col-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 3px;
}
.voters .col-yes .col-label { color: #2a4a30; }
.voters .col-no  .col-label { color: #7a2e10; }
.voters .name {
  display: inline-block;
  background: var(--bg-sunk);
  padding: 2px 8px;
  margin: 2px 4px 2px 0;
  border-radius: 999px;
  font-size: 12px;
  color: var(--fg);
  font-weight: 500;
}
.voters .none { color: var(--fg-faint); font-style: italic; }

.vote-row .tally-pill {
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 600;
  background: rgba(255,255,255,0.18);
  padding: 2px 8px;
  border-radius: 999px;
}
.sheet .actions {
  margin-top: 22px;
  display: flex;
  justify-content: space-between;
  font-family: var(--font-sans);
  font-size: 14px;
}
.sheet .actions button {
  background: none; border: none; padding: 8px 4px;
  font-family: inherit; font-size: inherit;
  color: var(--fg-muted); cursor: pointer;
}
.sheet .actions .delete { color: var(--accent-alt); }

.footnote {
  font-family: var(--font-sans);
  font-size: 12px;
  color: var(--fg-faint);
  text-align: center;
  margin-top: 10px;
}

.whoami {
  font-family: var(--font-sans);
  font-size: 12px;
  color: var(--fg-muted);
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 10px;
}
.whoami a { color: var(--accent); cursor: pointer; text-decoration: underline; }

.bubble.banned { filter: saturate(0.6); }
.bubble.banned .label,
.bubble.banned .tally { position: relative; z-index: 2; }
.bubble.banned .ban-x {
  position: absolute;
  inset: 10%;
  pointer-events: none;
  z-index: 1;
}
.bubble.banned .ban-x::before,
.bubble.banned .ban-x::after {
  content: '';
  position: absolute;
  top: 50%; left: 0;
  width: 100%;
  height: 5%;
  background: #e8412a;
  border-radius: 999px;
  opacity: 0.95;
}
.bubble.banned .ban-x::before { transform: translateY(-50%) rotate(45deg); }
.bubble.banned .ban-x::after  { transform: translateY(-50%) rotate(-45deg); }
.bubble.banned .ban-label {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #fff;
  background: #e8412a;
  padding: 2px 8px;
  border-radius: 999px;
  pointer-events: none;
  text-transform: lowercase;
  z-index: 3;
  white-space: nowrap;
}

.bubble.flash { animation: flash 900ms ease-out; }
@keyframes flash {
  0%   { box-shadow: 0 0 0 0 rgba(45, 74, 107, 0.55); }
  50%  { box-shadow: 0 0 0 14px rgba(45, 74, 107, 0); }
  100% { box-shadow: 0 0 0 0 rgba(45, 74, 107, 0); }
}
.bubble.flash.down { animation-name: flashDown; }
@keyframes flashDown {
  0%   { box-shadow: 0 0 0 0 rgba(160, 70, 40, 0.55); }
  50%  { box-shadow: 0 0 0 14px rgba(160, 70, 40, 0); }
  100% { box-shadow: 0 0 0 0 rgba(160, 70, 40, 0); }
}

.toast {
  position: absolute;
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 600;
  padding: 4px 9px;
  border-radius: 999px;
  background: var(--accent);
  color: #fff;
  pointer-events: none;
  z-index: 5;
  transform: translate(-50%, -50%);
  animation: float 1800ms ease-out forwards;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}
.toast.down { background: var(--accent-alt); }
@keyframes float {
  0%   { opacity: 0; transform: translate(-50%, -30%) scale(0.7); }
  20%  { opacity: 1; transform: translate(-50%, -60%) scale(1); }
  100% { opacity: 0; transform: translate(-50%, -180%) scale(1); }
}

/* name modal */
.namebox {
  width: 100%;
  max-width: var(--measure);
  background: var(--bg);
  border-radius: 18px;
  padding: 24px 22px 22px;
  margin: 0 16px;
}
.namebox h2 {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 400;
  margin: 0 0 6px;
  color: var(--fg);
  text-transform: none;
  letter-spacing: 0;
}
.namebox p { font-family: var(--font-sans); font-size: 14px; color: var(--fg-muted); margin: 0 0 14px; }
.namebox form { display: flex; gap: 8px; }
.namebox input {
  flex: 1;
  font-family: var(--font-sans); font-size: 16px;
  border: 1px solid var(--rule); background: #fff;
  border-radius: 999px; padding: 12px 16px;
}
.namebox input:focus { outline: none; border-color: var(--accent); }
.namebox button {
  font-family: var(--font-sans); font-size: 16px; font-weight: 600;
  color: #fff; background: var(--accent); border: none;
  border-radius: 999px; padding: 0 20px; cursor: pointer;
}
</style>

<html>

<div class="page">
  <h1>Lakes trip</h1>

  <div class="whoami" id="whoami"></div>

  <div class="kind-toggle">
    <input type="radio" name="kind" value="food" id="k-food" checked>
    <label for="k-food" class="pill-food">food</label>
    <input type="radio" name="kind" value="activity" id="k-act">
    <label for="k-act" class="pill-act">activity</label>
  </div>

  <form class="entry" id="entryForm" autocomplete="off">
    <input id="ideaInput" type="text" placeholder="pizza night, swim before breakfast..." maxlength="80" required>
    <button type="submit">Add</button>
  </form>

  <div id="stage">
    <div class="empty" id="empty">Be the first to add an idea.</div>
  </div>

  <p class="footnote"><a href="/lakes-shopping-list/">see the plan &amp; shopping list &rarr;</a></p>
</div>

<div class="scrim" id="nameScrim" style="align-items:center">
  <div class="namebox">
    <h2>What's your name?</h2>
    <p>So everyone can see who voted for what.</p>
    <form id="nameForm" autocomplete="off">
      <input id="nameInput" type="text" placeholder="Jess, Oli, ..." maxlength="24" required>
      <button type="submit">Join</button>
    </form>
  </div>
</div>

<div class="scrim" id="scrim">
  <div class="sheet" id="sheet">
    <div class="kindlabel" id="m-kind"></div>
    <div class="text" id="m-text"></div>
    <div class="addedby" id="m-addedby"></div>
    <div class="vote-row">
      <button id="m-up" class="yes" aria-label="vote yes">Vote yes <span class="tally-pill" id="m-ups">0</span></button>
      <button id="m-down" class="no" aria-label="vote no">Vote no <span class="tally-pill" id="m-downs">0</span></button>
    </div>
    <div class="voters" id="m-voters"></div>
    <div class="actions">
      <button id="m-close">Close</button>
      <button id="m-switch">Switch to <span id="m-switch-target">activity</span></button>
      <button id="m-delete" class="delete">Remove</button>
    </div>
  </div>
</div>

<script>
(function () {
  const API = '/api/lakes-meal-planner';
  const NAME_KEY = 'lakes-mp.name';
  const $ = (id) => document.getElementById(id);
  const stage = $('stage');
  const empty = $('empty');
  const scrim = $('scrim');
  let ideas = [];      // server truth
  let nodes = {};      // id -> { el, x, y, vx, vy, r }
  let activeId = null;
  let stageRect = null;
  let myName = (localStorage.getItem(NAME_KEY) || '').trim();
  let lastEventTs = '';
  let seenEvents = new Set();

  function escapeHtml(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  // ---------- name onboarding ----------
  const nameScrim = $('nameScrim');
  function showNamePrompt(prefill) {
    if (prefill) $('nameInput').value = prefill;
    nameScrim.classList.add('open');
    setTimeout(() => $('nameInput').focus(), 50);
  }
  function hideNamePrompt() { nameScrim.classList.remove('open'); }
  function renderWhoami() {
    $('whoami').innerHTML = myName
      ? `Voting as <strong>${escapeHtml(myName)}</strong> · <a id="changeName">change</a>`
      : `<a id="changeName">Set your name</a> to vote`;
    const c = document.getElementById('changeName');
    if (c) c.addEventListener('click', () => showNamePrompt(myName));
  }
  $('nameForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const v = $('nameInput').value.trim().slice(0, 24);
    if (!v) return;
    myName = v;
    localStorage.setItem(NAME_KEY, myName);
    renderWhoami();
    hideNamePrompt();
  });
  function requireName() {
    if (myName) return true;
    showNamePrompt('');
    return false;
  }
  renderWhoami();
  if (!myName) showNamePrompt('');

  // ---------- physics ----------
  function recalcRect() { stageRect = stage.getBoundingClientRect(); }
  window.addEventListener('resize', recalcRect);

  function radiusFor(ups) {
    return Math.round(34 + Math.sqrt(Math.max(ups, 0)) * 14); // px
  }

  function fontSizeFor(r, text) {
    const len = (text || '').length;
    // bubble has ~ pi*r^2 area; fit text by scaling font with sqrt(area/length)
    const base = 9 + r * 0.2;             // would-be size if short text
    const lenPenalty = Math.min(1, 11 / Math.max(len, 1));
    return Math.max(9, Math.min(18, base * lenPenalty));
  }

  function glowFor(ups, downs) {
    const net = (ups || 0) - (downs || 0);
    if (net > 0) {
      const g = Math.min(net, 5);
      return `0 0 ${6 + g*4}px ${1 + g}px rgba(94, 117, 68, ${0.22 + g*0.08})`;
    }
    if ((downs || 0) > 0) {
      const g = Math.min(downs, 5);
      return `0 0 ${6 + g*4}px ${1 + g}px rgba(160, 70, 40, ${0.18 + g*0.08})`;
    }
    return '';
  }

  const PALETTE_FOOD = [
    { fill: '#ffd9c2', ink: '#7a2e10', border: '#e8a07a' }, // peach
    { fill: '#ffe6a8', ink: '#6b4a10', border: '#d9b35e' }, // butter
    { fill: '#ffc9c1', ink: '#7a1f18', border: '#e08d80' }, // coral
    { fill: '#f5cfe0', ink: '#6f1d44', border: '#d68fb1' }, // rose
    { fill: '#ffdfb8', ink: '#7a3e10', border: '#d99a55' }, // apricot
    { fill: '#f0d4a8', ink: '#5e3e14', border: '#c69a55' }, // ochre
  ];
  const PALETTE_ACT = [
    { fill: '#cfe1d0', ink: '#2a4a30', border: '#8db59a' }, // sage
    { fill: '#c6dceb', ink: '#1f3e5a', border: '#80a8c4' }, // sky
    { fill: '#d4d2ec', ink: '#2c2e6b', border: '#9a96d1' }, // lilac
    { fill: '#bfe3d9', ink: '#114a40', border: '#7ec0ad' }, // mint
    { fill: '#d8e5b5', ink: '#3a4a10', border: '#a8bd6e' }, // moss
    { fill: '#c4dee5', ink: '#1c4250', border: '#7eb1bd' }, // teal
  ];

  function hashStr(s) {
    let h = 5381;
    for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
    return Math.abs(h);
  }
  function paletteFor(idea) {
    const arr = idea.kind === 'food' ? PALETTE_FOOD : PALETTE_ACT;
    return arr[hashStr(idea.id) % arr.length];
  }

  const ICON_UP   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H7a2 2 0 0 1-2-2V10a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L15 2"/></svg>';
  const ICON_DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 14V2"/><path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H17a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L9 22"/></svg>';

  function tallyHtml(idea) {
    return `<span>${ICON_UP}${idea.ups || 0}</span><span>${ICON_DOWN}${idea.downs || 0}</span>`;
  }

  function spawnPos(r) {
    const w = stageRect.width, h = stageRect.height;
    return {
      x: r + Math.random() * Math.max(1, w - 2 * r),
      y: r + Math.random() * Math.max(1, h - 2 * r),
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
    };
  }

  function step() {
    if (!stageRect) recalcRect();
    const w = stageRect.width, h = stageRect.height;
    const ids = Object.keys(nodes);

    // collision resolution (cheap O(n^2), n is small)
    for (let i = 0; i < ids.length; i++) {
      const a = nodes[ids[i]];
      for (let j = i + 1; j < ids.length; j++) {
        const b = nodes[ids[j]];
        const dx = b.x - a.x, dy = b.y - a.y;
        const dist = Math.hypot(dx, dy) || 0.01;
        const min = a.r + b.r;
        if (dist < min) {
          const overlap = (min - dist) / 2;
          const nx = dx / dist, ny = dy / dist;
          a.x -= nx * overlap; a.y -= ny * overlap;
          b.x += nx * overlap; b.y += ny * overlap;
          // gentle bounce
          const p = (a.vx * nx + a.vy * ny) - (b.vx * nx + b.vy * ny);
          a.vx -= p * nx * 0.5; a.vy -= p * ny * 0.5;
          b.vx += p * nx * 0.5; b.vy += p * ny * 0.5;
        }
      }
    }

    // integrate + walls + drift + buoyancy
    for (const id of ids) {
      const n = nodes[id];
      n.vx += (Math.random() - 0.5) * 0.08;
      n.vy += (Math.random() - 0.5) * 0.08;
      // buoyancy: votes -10..+10 maps to bottom..top of stage
      const v = Math.max(-10, Math.min(10, n.votes || 0));
      const t = (10 - v) / 20;                       // 0=top, 1=bottom
      const targetY = n.r + t * Math.max(1, (h - 2 * n.r));
      n.vy += (targetY - n.y) * 0.0018;              // gentle spring
      // damping
      n.vx *= 0.975; n.vy *= 0.975;
      // clamp max speed
      const sp = Math.hypot(n.vx, n.vy);
      if (sp > 2.0) { n.vx *= 2.0 / sp; n.vy *= 2.0 / sp; }
      n.x += n.vx; n.y += n.vy;
      // walls
      if (n.x < n.r) { n.x = n.r; n.vx = Math.abs(n.vx); }
      if (n.x > w - n.r) { n.x = w - n.r; n.vx = -Math.abs(n.vx); }
      if (n.y < n.r) { n.y = n.r; n.vy = Math.abs(n.vy); }
      if (n.y > h - n.r) { n.y = h - n.r; n.vy = -Math.abs(n.vy); }
      n.el.style.transform = `translate(${n.x - n.r}px, ${n.y - n.r}px)`;
    }

    requestAnimationFrame(step);
  }

  // ---------- render ----------
  function render() {
    empty.style.display = ideas.length ? 'none' : 'flex';
    const seen = new Set();
    for (const idea of ideas) {
      seen.add(idea.id);
      const r = radiusFor(idea.ups || 0);
      const fs = fontSizeFor(r, idea.text);
      const glow = glowFor(idea.ups || 0, idea.downs || 0);
      const banned = idea.text.trim().toLowerCase() === 'bag';
      const innerExtras = banned ? '<div class="ban-x"></div><div class="ban-label">(banned)</div>' : '';
      const inner = `<span class="label">${escapeHtml(idea.text)}</span><span class="tally">${tallyHtml(idea)}</span>${innerExtras}`;
      const c = paletteFor(idea);
      function paint(el) {
        el.style.background   = c.fill;
        el.style.color        = c.ink;
        el.style.borderColor  = c.border;
      }
      if (nodes[idea.id]) {
        const n = nodes[idea.id];
        n.r = r;
        n.votes = idea.votes || 0;
        const size = r * 2;
        n.el.style.width = size + 'px';
        n.el.style.height = size + 'px';
        n.el.style.fontSize = fs + 'px';
        n.el.style.boxShadow = glow;
        n.el.innerHTML = inner;
        n.el.className = 'bubble ' + idea.kind + (banned ? ' banned' : '');
        paint(n.el);
      } else {
        const el = document.createElement('div');
        el.className = 'bubble ' + idea.kind + ' pop' + (banned ? ' banned' : '');
        el.innerHTML = inner;
        const size = r * 2;
        el.style.width = size + 'px';
        el.style.height = size + 'px';
        el.style.fontSize = fs + 'px';
        el.style.boxShadow = glow;
        paint(el);
        el.addEventListener('click', () => openSheet(idea.id));
        stage.appendChild(el);
        const pos = spawnPos(r);
        nodes[idea.id] = { el, r, votes: idea.votes || 0, ...pos };
        el.style.transform = `translate(${pos.x - r}px, ${pos.y - r}px)`;
      }
    }
    for (const id of Object.keys(nodes)) {
      if (!seen.has(id)) {
        nodes[id].el.remove();
        delete nodes[id];
      }
    }
  }

  // ---------- modal ----------
  function paintModal(idea) {
    $('m-kind').textContent = idea.kind;
    $('m-kind').className = 'kindlabel ' + idea.kind;
    $('m-text').textContent = idea.text;
    $('m-addedby').innerHTML = idea.created_by ? `added by <strong>${escapeHtml(idea.created_by)}</strong>` : '';
    $('m-ups').textContent = idea.ups || 0;
    $('m-downs').textContent = idea.downs || 0;
    $('m-switch-target').textContent = idea.kind === 'food' ? 'activity' : 'food';
    const yes = (idea.who_ups || []).map(n => `<span class="name">${escapeHtml(n)}</span>`).join('') || '<span class="none">no one yet</span>';
    const no  = (idea.who_downs || []).map(n => `<span class="name">${escapeHtml(n)}</span>`).join('') || '<span class="none">no one yet</span>';
    $('m-voters').innerHTML = `
      <div class="col-yes"><div class="col-label">Yes</div>${yes}</div>
      <div class="col-no"><div class="col-label">No</div>${no}</div>
    `;
  }

  function openSheet(id) {
    activeId = id;
    const idea = ideas.find(i => i.id === id);
    if (!idea) return;
    paintModal(idea);
    scrim.classList.add('open');
  }
  function closeSheet() { scrim.classList.remove('open'); activeId = null; }

  scrim.addEventListener('click', (e) => { if (e.target === scrim) closeSheet(); });
  $('m-close').addEventListener('click', closeSheet);

  $('m-up').addEventListener('click', () => sendVote(1));
  $('m-down').addEventListener('click', () => sendVote(-1));
  $('m-delete').addEventListener('click', async () => {
    if (!activeId) return;
    if (!confirm('Remove this idea for everyone?')) return;
    await fetch(`${API}/ideas/${activeId}`, { method: 'DELETE' });
    closeSheet();
    refresh();
  });
  $('m-switch').addEventListener('click', async () => {
    if (!activeId) return;
    const idea = ideas.find(i => i.id === activeId);
    if (!idea) return;
    const target = idea.kind === 'food' ? 'activity' : 'food';
    const r = await fetch(`${API}/ideas/${activeId}/kind`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ kind: target }),
    });
    if (r.ok) { closeSheet(); refresh(); }
  });

  async function sendVote(delta) {
    if (!activeId) return;
    if (!requireName()) return;
    const r = await fetch(`${API}/ideas/${activeId}/vote`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ delta, name: myName }),
    });
    if (r.ok) {
      const updated = await r.json();
      const idx = ideas.findIndex(i => i.id === updated.id);
      if (idx >= 0) ideas[idx] = updated;
      paintModal(updated);
      render();
    }
  }

  // ---------- live events: glow + attribution toast ----------
  function showToast(ideaId, name, delta) {
    const n = nodes[ideaId];
    if (!n) return;
    n.el.classList.remove('flash', 'down');
    void n.el.offsetWidth; // restart animation
    n.el.classList.add('flash');
    if (delta < 0) n.el.classList.add('down');

    const toast = document.createElement('div');
    toast.className = 'toast' + (delta < 0 ? ' down' : '');
    toast.textContent = delta > 0 ? `${name} wants this` : `${name} doesn't`;
    toast.style.left = n.x + 'px';
    toast.style.top  = (n.y - n.r - 6) + 'px';
    stage.appendChild(toast);
    setTimeout(() => toast.remove(), 1900);
  }

  async function pollEvents() {
    try {
      const url = lastEventTs ? `${API}/events?since=${encodeURIComponent(lastEventTs)}` : `${API}/events`;
      const r = await fetch(url, { cache: 'no-store' });
      if (!r.ok) return;
      const data = await r.json();
      const evts = data.events || [];
      if (!evts.length) return;
      // initial load: just record latest timestamp, skip toasts
      if (!lastEventTs) {
        lastEventTs = evts[evts.length - 1].ts;
        evts.forEach(e => seenEvents.add(e.id));
        return;
      }
      for (const e of evts) {
        if (seenEvents.has(e.id)) continue;
        seenEvents.add(e.id);
        if (e.name && e.name !== myName) showToast(e.idea_id, e.name, e.delta);
        if (e.ts > lastEventTs) lastEventTs = e.ts;
      }
    } catch (e) { /* ignore */ }
  }

  // ---------- entry ----------
  $('entryForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!requireName()) return;
    const input = $('ideaInput');
    const text = input.value.trim();
    if (!text) return;
    const kind = document.querySelector('input[name="kind"]:checked').value;
    input.value = '';
    const r = await fetch(`${API}/ideas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, kind, name: myName }),
    });
    if (r.ok) refresh();
  });

  // ---------- sync ----------
  async function refresh() {
    try {
      const r = await fetch(`${API}/ideas`, { cache: 'no-store' });
      if (!r.ok) return;
      const data = await r.json();
      ideas = data.ideas || [];
      render();
    } catch (e) { /* offline; try again next tick */ }
  }

  recalcRect();
  refresh();
  pollEvents();
  setInterval(refresh, 3000);
  setInterval(pollEvents, 2000);
  requestAnimationFrame(step);
})();
</script>
