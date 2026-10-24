/**
 * Penumbra – UI (v4)
 * Novità: mano di carte, selezione carta, evocazione.
 */

const UI = {
  gridEl: null,
  handEl: null,
  cells: [],

  init() {
    this.gridEl = document.getElementById('grid');
    this.handEl = document.getElementById('hand');
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

    // Click sulle carte in mano
    this.handEl.addEventListener('click', (e) => {
      const cardEl = e.target.closest('.card');
      if (!cardEl) return;
      const idx = parseInt(cardEl.dataset.index, 10);
      this.onCardClick(idx);
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
        if (Game.gameOver) this.showGameOver();
        else this.showHint('Clicca una carta o un\'unità');
      }, 550);
    });

    document.getElementById('btn-close-message').addEventListener('click', () => {
      document.getElementById('message-overlay').classList.add('hidden');
    });

    const btnRestart = document.getElementById('btn-restart');
    if (btnRestart) {
      btnRestart.addEventListener('click', () => {
        document.getElementById('message-overlay').classList.add('hidden');
        Game.init();
        this.render();
        this.showHint('Clicca una carta o un\'unità');
      });
    }
  },

  onCardClick(index) {
    if (Game.currentPlayer !== 'player' || Game.gameOver) return;

    const card = Game.hands.player[index];
    const ok = Game.selectCard(index);
    this.render();

    if (ok) {
      if (card && card.type === 'weapon') {
        if (Game.possibleEquips.length > 0) {
          this.showHint('Clicca un\'unità blu per equipaggiare l\'arma');
        } else {
          this.showHint('Nessuna unità con mani libere');
          Game.clearCardSelection();
          this.render();
        }
      } else if (Game.possibleSummons.length > 0) {
        this.showHint('Clicca una casella verde accanto al Magus per evocare');
      } else {
        this.showHint('Nessuna casella libera accanto al Magus');
        Game.clearCardSelection();
        this.render();
      }
    } else {
      if (card && Game.powa.player < card.cost) {
        this.showHint(`Powa insufficiente (serve ${card.cost})`);
      } else if (card && card.type === 'weapon') {
        this.showHint('Nessuna unità con mani libere per questa arma');
      } else {
        this.showHint('Non puoi giocare questa carta ora');
      }
    }
  },

  onCellClick(r, c) {
    if (Game.currentPlayer !== 'player' || Game.gameOver) return;

    // Se abbiamo una carta selezionata → evocazione o equip
    if (Game.selectedCardIndex !== null) {
      const card = Game.hands.player[Game.selectedCardIndex];

      if (Game.canEquipTo(r, c)) {
        Game.equipWeapon(r, c);
        this.render();
        this.showHint('Arma equipaggiata! ATK aumentato');
        return;
      }

      if (Game.canSummonTo(r, c)) {
        const isTower = card && card.type === 'tower';
        Game.summonCard(r, c);
        this.render();
        this.showHint(isTower
          ? 'Torre piazzata! Non si muove, dà bonus agli alleati vicini'
          : 'Creatura evocata! Può agire dal prossimo turno');
        return;
      }

      Game.clearCardSelection();
      this.render();
      this.showHint('Clicca una carta o un\'unità');
      return;
    }

    const unit = Game.getUnit(r, c);

    // Seleziona unità nostra (non torri, non già agite)
    if (unit && unit.owner === 'player' && !unit.acted && unit.type !== 'tower') {
      Game.selectUnit(r, c);
      this.render();
      const hasAtk = Game.possibleAttacks.length > 0;
      const hasMov = Game.possibleMoves.length > 0;
      if (hasAtk && hasMov) this.showHint('Giallo = muovi • Rosso = attacca');
      else if (hasAtk) this.showHint('Clicca una casella rossa per attaccare');
      else if (hasMov) this.showHint('Clicca una casella gialla per muoverti');
      else this.showHint('Nessuna azione possibile');
      return;
    }

    // Azione con unità selezionata
    if (Game.selected) {
      const { r: fr, c: fc } = Game.selected;

      if (Game.canAttack(r, c)) {
        const result = Game.attackUnit(fr, fc, r, c);
        this.render();
        if (result?.killed) this.showHint(`Colpo fatale! (${result.damage} danni)`);
        else if (result) this.showHint(`Inflitti ${result.damage} danni`);
        if (Game.gameOver) setTimeout(() => this.showGameOver(), 400);
        return;
      }

      if (Game.canMoveTo(r, c)) {
        Game.moveUnit(fr, fc, r, c);
        this.render();
        this.showHint('Unità mossa');
        return;
      }
    }

    Game.deselect();
    Game.clearCardSelection();
    this.render();
    this.showHint('Clicca una carta o un\'unità');
  },

  showHint(text) {
    document.getElementById('hint').textContent = text;
  },

  showGameOver() {
    const overlay = document.getElementById('message-overlay');
    const text = document.getElementById('message-text');
    const btnClose = document.getElementById('btn-close-message');
    const btnRestart = document.getElementById('btn-restart');

    text.textContent = Game.winner === 'player'
      ? 'VITTORIA!\nHai sconfitto il Faraone Oscuro'
      : 'SCONFITTA\nIl Faraone Oscuro ti ha battuto';

    btnClose.classList.add('hidden');
    if (btnRestart) btnRestart.classList.remove('hidden');
    overlay.classList.remove('hidden');
  },

  renderHand(state) {
    this.handEl.innerHTML = '';

    state.hand.forEach((card, idx) => {
      const el = document.createElement('div');
      el.className = 'card';
      if (card.type === 'tower') el.classList.add('card-tower');
      if (card.type === 'weapon') el.classList.add('card-weapon');
      el.dataset.index = idx;

      const playableTypes = ['creature', 'tower', 'weapon'];
      const canPlay = state.currentPlayer === 'player' &&
                      !state.gameOver &&
                      card.cost <= state.powa &&
                      playableTypes.includes(card.type);

      if (!canPlay) el.classList.add('disabled');
      if (state.selectedCardIndex === idx) el.classList.add('selected');

      let statsHtml;
      if (card.type === 'tower') {
        statsHtml = `<span class="hp">❤ ${card.hp}</span><span class="passive">+ATK</span>`;
      } else if (card.type === 'weapon') {
        statsHtml = `<span class="atk">⚔ +${card.atkBonus}</span>`;
      } else {
        statsHtml = `<span class="atk">⚔ ${card.atk}</span><span class="hp">❤ ${card.hp}</span>`;
      }

      el.innerHTML = `
        <div class="card-cost">◆ ${card.cost}</div>
        <div class="card-symbol">${card.symbol}</div>
        <div class="card-name">${card.name}</div>
        <div class="card-stats">${statsHtml}</div>
      `;
      el.title = `${card.name} (${card.type})\nCosto: ${card.cost} Powa\n${card.desc || ''}`;
      this.handEl.appendChild(el);
    });
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

    document.getElementById('btn-end-turn').disabled =
      state.currentPlayer !== 'player' || state.gameOver;

    // Griglia
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        const cell = this.cells[r][c];
        cell.innerHTML = '';
        cell.classList.remove('highlight', 'attack-highlight', 'summon-highlight', 'equip-highlight');
      }
    }

    for (const m of state.possibleMoves) {
      this.cells[m.r][m.c].classList.add('highlight');
    }
    for (const a of state.possibleAttacks) {
      this.cells[a.r][a.c].classList.add('attack-highlight');
    }
    for (const s of state.possibleSummons) {
      this.cells[s.r][s.c].classList.add('summon-highlight');
    }
    for (const e of (state.possibleEquips || [])) {
      this.cells[e.r][e.c].classList.add('equip-highlight');
    }

    // Unità
    for (const [key, unit] of Object.entries(state.units)) {
      const [r, c] = key.split('-').map(Number);
      const cell = this.cells[r][c];
      const el = document.createElement('div');
      el.className = `unit ${unit.owner}`;
      if (unit.type === 'creature') el.classList.add('creature');
      if (unit.type === 'tower') el.classList.add('tower');
      if (unit.acted) el.classList.add('acted');
      if (state.selected && state.selected.r === r && state.selected.c === c) {
        el.classList.add('selected');
      }

      const atkShow = unit.type === 'tower' ? 0 : (unit.effectiveAtk ?? unit.atk);
      const bonus = (unit.effectiveAtk != null && unit.effectiveAtk > unit.atk)
        ? ` (+${unit.effectiveAtk - unit.atk})` : '';
      const hasWeapon = unit.weapons && unit.weapons.length > 0;

      el.innerHTML = `
        <span class="unit-symbol">${unit.symbol || (unit.owner === 'player' ? '𓁹' : '𓀀')}</span>
        <span class="unit-hp">${unit.hp}</span>
        ${hasWeapon ? '<span class="unit-weapon">⚔</span>' : ''}
      `;
      el.title = unit.type === 'tower'
        ? `${unit.name} (Torre) — HP ${unit.hp} • Alleati adiacenti +ATK`
        : `${unit.name || (unit.owner === 'player' ? 'Il tuo Magus' : 'Faraone Oscuro')} — ATK ${atkShow}${bonus} / HP ${unit.hp}${hasWeapon ? ' • Armato' : ''}`;
      cell.appendChild(el);
    }

    // Mano
    this.renderHand(state);
  }
};

document.addEventListener('DOMContentLoaded', () => UI.init());
