/**
 * Penumbra – UI (v2)
 * Rendering e input. Usa il motore in engine.js
 */

const UI = {
  gridEl: null,
  cells: [], // array 4x5 di elementi DOM

  init() {
    this.gridEl = document.getElementById('grid');
    this.buildGrid();
    this.bindEvents();
    Game.init();
    this.render();
  },

  buildGrid() {
    this.gridEl.innerHTML = '';
    this.cells = [];

    for (let r = 0; r < ROWS; r++) {
      const row = [];
      for (let c = 0; c < COLS; c++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.r = r;
        cell.dataset.c = c;
        this.gridEl.appendChild(cell);
        row.push(cell);
      }
      this.cells.push(row);
    }
  },

  bindEvents() {
    // Click sulle celle
    this.gridEl.addEventListener('click', (e) => {
      const cell = e.target.closest('.cell');
      if (!cell) return;
      const r = parseInt(cell.dataset.r, 10);
      const c = parseInt(cell.dataset.c, 10);
      this.onCellClick(r, c);
    });

    // Pulsante Fine Turno
    document.getElementById('btn-end-turn').addEventListener('click', () => {
      if (Game.currentPlayer !== 'player') return;
      Game.endTurn();
      this.render();
      this.showHint('Turno dell\'IA…');
      // Piccolo delay per far vedere la mossa dell'IA
      setTimeout(() => {
        this.render();
        this.showHint('Clicca il tuo Magus per muoverlo');
      }, 600);
    });

    // Chiudi messaggio
    document.getElementById('btn-close-message').addEventListener('click', () => {
      document.getElementById('message-overlay').classList.add('hidden');
    });
  },

  onCellClick(r, c) {
    if (Game.currentPlayer !== 'player') return;

    const unit = Game.getUnit(r, c);

    // Se c'è un'unità nostra → seleziona
    if (unit && unit.owner === 'player') {
      Game.selectUnit(r, c);
      this.render();
      this.showHint('Clicca una casella evidenziata per muoverti');
      return;
    }

    // Se abbiamo qualcosa di selezionato e clicchiamo una casella valida → muovi
    if (Game.selected && Game.canMoveTo(r, c)) {
      const { r: fr, c: fc } = Game.selected;
      Game.moveUnit(fr, fc, r, c);
      this.render();
      this.showHint('Puoi muovere di nuovo o cliccare Fine Turno');
      return;
    }

    // Click a vuoto → deseleziona
    Game.deselect();
    this.render();
    this.showHint('Clicca il tuo Magus per muoverlo');
  },

  showHint(text) {
    document.getElementById('hint').textContent = text;
  },

  render() {
    const state = Game.getState();

    // Header
    document.getElementById('turn-label').textContent = `Turno ${state.turn}`;
    document.getElementById('phase-label').textContent =
      state.currentPlayer === 'player' ? 'Tuo turno' : 'Turno avversario';
    document.getElementById('powa-value').textContent = state.powa;

    // HP
    const playerPct = (state.playerHp / state.playerMaxHp) * 100;
    const aiPct = (state.aiHp / state.aiMaxHp) * 100;
    document.getElementById('player-hp-fill').style.width = playerPct + '%';
    document.getElementById('player-hp-text').textContent = `${state.playerHp} / ${state.playerMaxHp}`;
    document.getElementById('ai-hp-fill').style.width = aiPct + '%';
    document.getElementById('ai-hp-text').textContent = `${state.aiHp} / ${state.aiMaxHp}`;

    // Bottone Fine Turno
    const btn = document.getElementById('btn-end-turn');
    btn.disabled = state.currentPlayer !== 'player';

    // Pulisci griglia
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        const cell = this.cells[r][c];
        cell.innerHTML = '';
        cell.classList.remove('highlight');
      }
    }

    // Evidenzia mosse possibili
    for (const m of state.possibleMoves) {
      this.cells[m.r][m.c].classList.add('highlight');
    }

    // Disegna unità
    for (const [key, unit] of Object.entries(state.units)) {
      const [r, c] = key.split('-').map(Number);
      const cell = this.cells[r][c];
      const el = document.createElement('div');
      el.className = `unit ${unit.owner}`;
      if (state.selected && state.selected.r === r && state.selected.c === c) {
        el.classList.add('selected');
      }
      el.textContent = unit.owner === 'player' ? '𓁹' : '𓀀';
      el.title = unit.owner === 'player' ? 'Il tuo Magus' : 'Faraone Oscuro';
      cell.appendChild(el);
    }
  }
};

// Avvio
document.addEventListener('DOMContentLoaded', () => UI.init());
