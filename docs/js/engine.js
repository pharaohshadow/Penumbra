/**
 * Penumbra – Game Engine (v2)
 * Logica pura di gioco, senza DOM.
 */

const ROWS = 4;
const COLS = 5;

const Game = {
  turn: 1,
  currentPlayer: 'player', // 'player' | 'ai'
  powa: { player: 1, ai: 1 },
  maxPowa: 6,

  // Unità sulla griglia: chiave "r-c"
  units: {},

  selected: null, // { r, c } della unità selezionata
  possibleMoves: [], // array di { r, c }

  // Stato Magus
  magus: {
    player: { hp: 20, maxHp: 20, atk: 1, hands: 2 },
    ai:     { hp: 20, maxHp: 20, atk: 1, hands: 2 }
  },

  // ---- Inizializzazione ----
  init() {
    this.turn = 1;
    this.currentPlayer = 'player';
    this.powa = { player: 1, ai: 1 };
    this.units = {};
    this.selected = null;
    this.possibleMoves = [];

    // Posizioni iniziali Magus
    // Player in basso al centro (riga 3, colonna 2)
    // AI in alto al centro (riga 0, colonna 2)
    this.units['3-2'] = { owner: 'player', type: 'magus', id: 'player-magus' };
    this.units['0-2'] = { owner: 'ai',     type: 'magus', id: 'ai-magus' };

    this.magus.player.hp = 20;
    this.magus.ai.hp = 20;
  },

  // ---- Utilità griglia ----
  key(r, c) {
    return `${r}-${c}`;
  },

  isInside(r, c) {
    return r >= 0 && r < ROWS && c >= 0 && c < COLS;
  },

  isEmpty(r, c) {
    return !this.units[this.key(r, c)];
  },

  getUnit(r, c) {
    return this.units[this.key(r, c)] || null;
  },

  // Caselle adiacenti ortogonali
  getOrthogonal(r, c) {
    const dirs = [[-1,0], [1,0], [0,-1], [0,1]];
    const result = [];
    for (const [dr, dc] of dirs) {
      const nr = r + dr;
      const nc = c + dc;
      if (this.isInside(nr, nc)) result.push({ r: nr, c: nc });
    }
    return result;
  },

  // ---- Selezione e movimento ----
  selectUnit(r, c) {
    const unit = this.getUnit(r, c);
    if (!unit) return false;
    if (unit.owner !== this.currentPlayer) return false;
    if (this.currentPlayer !== 'player') return false; // solo umano per ora

    this.selected = { r, c };
    this.possibleMoves = this.getOrthogonal(r, c)
      .filter(pos => this.isEmpty(pos.r, pos.c));

    return true;
  },

  deselect() {
    this.selected = null;
    this.possibleMoves = [];
  },

  canMoveTo(r, c) {
    return this.possibleMoves.some(m => m.r === r && m.c === c);
  },

  moveUnit(fromR, fromC, toR, toC) {
    if (!this.canMoveTo(toR, toC)) return false;

    const keyFrom = this.key(fromR, fromC);
    const keyTo = this.key(toR, toC);
    const unit = this.units[keyFrom];
    if (!unit) return false;

    delete this.units[keyFrom];
    this.units[keyTo] = unit;

    this.deselect();
    return true;
  },

  // ---- Turni e Powa ----
  // Guadagna Powa all'inizio del turno del giocatore indicato
  gainPowa(who) {
    const gain = Math.min(this.turn, this.maxPowa);
    this.powa[who] = Math.min(this.powa[who] + gain, this.maxPowa);
  },

  endTurn() {
    this.deselect();

    if (this.currentPlayer === 'player') {
      // Passa all'IA: l'IA guadagna Powa per questo turno e gioca
      this.currentPlayer = 'ai';
      this.gainPowa('ai');
      this.aiTurn();
    }
  },

  // IA molto semplice (v2): muove il Magus verso il basso se possibile, poi passa il turno
  aiTurn() {
    // Trova il Magus AI
    let aiPos = null;
    for (const [k, u] of Object.entries(this.units)) {
      if (u.owner === 'ai' && u.type === 'magus') {
        const [r, c] = k.split('-').map(Number);
        aiPos = { r, c };
        break;
      }
    }

    if (aiPos) {
      const moves = this.getOrthogonal(aiPos.r, aiPos.c)
        .filter(pos => this.isEmpty(pos.r, pos.c));

      if (moves.length > 0) {
        // Preferisci muoverti verso il basso (verso il player)
        moves.sort((a, b) => b.r - a.r);
        const choice = moves[0];
        const keyFrom = this.key(aiPos.r, aiPos.c);
        const keyTo = this.key(choice.r, choice.c);
        this.units[keyTo] = this.units[keyFrom];
        delete this.units[keyFrom];
      }
    }

    // Fine turno IA → inizia nuovo turno del player
    this.turn += 1;
    this.currentPlayer = 'player';
    this.gainPowa('player');
  },

  // ---- Stato per la UI ----
  getState() {
    return {
      turn: this.turn,
      currentPlayer: this.currentPlayer,
      powa: this.powa.player, // mostriamo solo il Powa del player
      maxPowa: this.maxPowa,
      units: { ...this.units },
      selected: this.selected,
      possibleMoves: [...this.possibleMoves],
      playerHp: this.magus.player.hp,
      playerMaxHp: this.magus.player.maxHp,
      aiHp: this.magus.ai.hp,
      aiMaxHp: this.magus.ai.maxHp
    };
  }
};
