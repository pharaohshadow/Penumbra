/**
 * Penumbra – UI (v3)
 * Rendering e input. Usa il motore in engine.js
 * Novità v3: evidenziazione attacchi (rosso), danni, vittoria/sconfitta.
 */

const UI = {
  gridEl: null,
  cells: [],

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
    this.gridEl.addEventListener('click', (e) => {
      const cell = e.target.closest('.cell');
      if (!cell) return;
      const r = parseInt(cell.dataset.r, 10);
      const c = parseInt(cell.dataset.c, 10);
      this.onCellClick(r, c);
    });

    document.getElementById('btn-end-turn').addEventListener('click', () => {
      if (Game.currentPlayer !== 'player' || Game.gameOver) return;
      Game.endTurn();
      this.render();

      if (Game.gameOver) {
        this.showGameOver();
        return;
      }

      this.showHint('Turno dell\'IA…');
      setTimeout(() => {
        this.render();
        if (Game.gameOver) {
          this.showGameOver();
        } else {
          this.showHint('Clicca il tuo Magus per muovere o attaccare');
        }
      }, 500);
    });

    document.getElementById('btn-close-message').addEventListener('click', () => {
      document.getElementById('message-overlay').classList.add('hidden');
      // Se era game over, si può ricominciare in futuro
    });

    // Pulsante Rigioca (appare a fine partita)
    const btnRestart = document.getElementById('btn-restart');
    if (btnRestart) {
      btnRestart.addEventListener('click', () => {
        document.getElementById('message-overlay').classList.add('hidden');
        Game.init();
        this.render();
        this.showHint('Clicca il tuo Magus per muovere o attaccare');
      });
    }
  },

  onCellClick(r, c) {
    if (Game.currentPlayer !== 'player' || Game.gameOver) return;

    const unit = Game.getUnit(r, c);

    // 1. Clic su una nostra unità non ancora agita → seleziona
    if (unit && unit.owner === 'player' && !unit.acted) {
      Game.selectUnit(r, c);
      this.render();
      const hasAtk = Game.possibleAttacks.length > 0;
      const hasMov = Game.possibleMoves.length > 0;
      if (hasAtk && hasMov) {
        this.showHint('Caselle gialle = muovi • Caselle rosse = attacca');
      } else if (hasAtk) {
        this.showHint('Clicca una casella rossa per attaccare');
      } else if (hasMov) {
        this.showHint('Clicca una casella gialla per muoverti');
      } else {
        this.showHint('Nessuna azione possibile con questa unità');
      }
      return;
    }

    // 2. Abbiamo una selezione → prova attacco o movimento
    if (Game.selected) {
      const { r: fr, c: fc } = Game.selected;

      // Attacco
      if (Game.canAttack(r, c)) {
        const result = Game.attackUnit(fr, fc, r, c);
        this.render();

        if (result && result.killed) {
          this.showHint(`Colpo fatale! (${result.damage} danni)`);
        } else if (result) {
          this.showHint(`Inflitti ${result.damage} danni`);
        }

        if (Game.gameOver) {
          setTimeout(() => this.showGameOver(), 400);
        }
        return;
      }

      // Movimento
      if (Game.canMoveTo(r, c)) {
        Game.moveUnit(fr, fc, r, c);
        this.render();
        this.showHint('Unità mossa. Puoi selezionare un\'altra o Fine Turno');
        return;
      }
    }

    // 3. Click a vuoto → deseleziona
    Game.deselect();
    this.render();
    this.showHint('Clicca il tuo Magus per muovere o attaccare');
  },

  showHint(text) {
    document.getElementById('hint').textContent = text;
  },

  showGameOver() {
    const overlay = document.getElementById('message-overlay');
    const text = document.getElementById('message-text');
    const btnClose = document.getElementById('btn-close-message');
    const btnRestart = document.getElementById('btn-restart');

    if (Game.winner === 'player') {
      text.textContent = 'VITTORIA!\nHai sconfitto il Faraone Oscuro';
    } else {
      text.textContent = 'SCONFITTA\nIl Faraone Oscuro ti ha battuto';
    }

    btnClose.classList.add('hidden');
    if (btnRestart) btnRestart.classList.remove('hidden');

    overlay.classList.remove('hidden');
  },

  render() {
    const state = Game.getState();

    // Header
    document.getElementById('turn-label').textContent = `Turno ${state.turn}`;
    document.getElementById('phase-label').textContent =
      state.gameOver ? 'Fine partita' :
      (state.currentPlayer === 'player' ? 'Tuo turno' : 'Turno avversario');
    document.getElementById('powa-value').textContent = state.powa;

    // HP
    const playerPct = state.playerMaxHp > 0 ? (state.playerHp / state.playerMaxHp) * 100 : 0;
    const aiPct = state.aiMaxHp > 0 ? (state.aiHp / state.aiMaxHp) * 100 : 0;
    document.getElementById('player-hp-fill').style.width = Math.max(0, playerPct) + '%';
    document.getElementById('player-hp-text').textContent = `${state.playerHp} / ${state.playerMaxHp}`;
    document.getElementById('ai-hp-fill').style.width = Math.max(0, aiPct) + '%';
    document.getElementById('ai-hp-text').textContent = `${state.aiHp} / ${state.aiMaxHp}`;

    // Bottone Fine Turno
    const btn = document.getElementById('btn-end-turn');
    btn.disabled = state.currentPlayer !== 'player' || state.gameOver;

    // Pulisci griglia
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        const cell = this.cells[r][c];
        cell.innerHTML = '';
        cell.classList.remove('highlight', 'attack-highlight');
      }
    }

    // Evidenzia mosse (giallo)
    for (const m of state.possibleMoves) {
      this.cells[m.r][m.c].classList.add('highlight');
    }

    // Evidenzia attacchi (rosso)
    for (const a of state.possibleAttacks) {
      this.cells[a.r][a.c].classList.add('attack-highlight');
    }

    // Disegna unità
    for (const [key, unit] of Object.entries(state.units)) {
      const [r, c] = key.split('-').map(Number);
      const cell = this.cells[r][c];
      const el = document.createElement('div');
      el.className = `unit ${unit.owner}`;
      if (unit.acted) el.classList.add('acted');
      if (state.selected && state.selected.r === r && state.selected.c === c) {
        el.classList.add('selected');
      }

      // Simbolo + piccolo indicatore HP
      el.innerHTML = `
        <span class="unit-symbol">${unit.owner === 'player' ? '𓁹' : '𓀀'}</span>
        <span class="unit-hp">${unit.hp}</span>
      `;
      el.title = `${unit.owner === 'player' ? 'Il tuo Magus' : 'Faraone Oscuro'} — ATK ${unit.atk} / HP ${unit.hp}`;
      cell.appendChild(el);
    }
  }
};

document.addEventListener('DOMContentLoaded', () => UI.init());
