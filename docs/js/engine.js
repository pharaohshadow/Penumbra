/**
 * Penumbra – Game Engine (v4)
 * Novità v4: mano di 10 carte, evocazione Creature pagando Powa.
 */

const ROWS = 4;
const COLS = 5;

const Game = {
  turn: 1,
  currentPlayer: 'player',
  powa: { player: 1, ai: 1 },
  maxPowa: 6,
  gameOver: false,
  winner: null,

  units: {},
  cemetery: [],

  // Mani
  hands: {
    player: [],
    ai: []
  },

  selected: null,          // { r, c } unità selezionata
  selectedCardIndex: null, // indice carta in mano selezionata
  possibleMoves: [],
  possibleAttacks: [],
  possibleSummons: [],     // caselle dove si può piazzare la carta

  init() {
    this.turn = 1;
    this.currentPlayer = 'player';
    this.powa = { player: 1, ai: 1 };
    this.units = {};
    this.cemetery = [];
    this.selected = null;
    this.selectedCardIndex = null;
    this.possibleMoves = [];
    this.possibleAttacks = [];
    this.possibleSummons = [];
    this.gameOver = false;
    this.winner = null;

    // Magus
    this.units['3-2'] = {
      owner: 'player', type: 'magus', id: 'player-magus',
      hp: 20, maxHp: 20, atk: 1, acted: false, symbol: '𓁹'
    };
    this.units['0-2'] = {
      owner: 'ai', type: 'magus', id: 'ai-magus',
      hp: 20, maxHp: 20, atk: 1, acted: false, symbol: '𓀀'
    };

    // Mani iniziali (10 carte ciascuno)
    this.hands.player = createStartingHand();
    this.hands.ai = createStartingHand();
  },

  // ---- Utilità griglia ----
  key(r, c) { return `${r}-${c}`; },
  isInside(r, c) { return r >= 0 && r < ROWS && c >= 0 && c < COLS; },
  isEmpty(r, c) { return !this.units[this.key(r, c)]; },
  getUnit(r, c) { return this.units[this.key(r, c)] || null; },

  getOrthogonal(r, c) {
    const dirs = [[-1,0],[1,0],[0,-1],[0,1]];
    return dirs
      .map(([dr,dc]) => ({ r: r+dr, c: c+dc }))
      .filter(p => this.isInside(p.r, p.c));
  },

  // Trova la posizione del Magus di un giocatore
  findMagus(owner) {
    for (const [k, u] of Object.entries(this.units)) {
      if (u.owner === owner && u.type === 'magus') {
        const [r, c] = k.split('-').map(Number);
        return { r, c, unit: u };
      }
    }
    return null;
  },

  // ---- Selezione unità ----
  selectUnit(r, c) {
    if (this.gameOver) return false;
    this.clearCardSelection();

    const unit = this.getUnit(r, c);
    if (!unit || unit.owner !== this.currentPlayer) return false;
    if (this.currentPlayer !== 'player') return false;
    if (unit.acted) return false;

    this.selected = { r, c };
    const adj = this.getOrthogonal(r, c);
    this.possibleMoves = adj.filter(p => this.isEmpty(p.r, p.c));
    this.possibleAttacks = adj.filter(p => {
      const t = this.getUnit(p.r, p.c);
      return t && t.owner !== unit.owner;
    });
    return true;
  },

  deselect() {
    this.selected = null;
    this.possibleMoves = [];
    this.possibleAttacks = [];
  },

  clearCardSelection() {
    this.selectedCardIndex = null;
    this.possibleSummons = [];
  },

  canMoveTo(r, c) {
    return this.possibleMoves.some(m => m.r === r && m.c === c);
  },
  canAttack(r, c) {
    return this.possibleAttacks.some(a => a.r === r && a.c === c);
  },
  canSummonTo(r, c) {
    return this.possibleSummons.some(s => s.r === r && s.c === c);
  },

  // ---- Movimento ----
  moveUnit(fromR, fromC, toR, toC) {
    if (this.gameOver || !this.canMoveTo(toR, toC)) return false;
    const keyFrom = this.key(fromR, fromC);
    const keyTo = this.key(toR, toC);
    const unit = this.units[keyFrom];
    if (!unit) return false;

    unit.acted = true;
    delete this.units[keyFrom];
    this.units[keyTo] = unit;
    this.deselect();
    return true;
  },

  // ---- Attacco ----
  attackUnit(fromR, fromC, toR, toC) {
    if (this.gameOver || !this.canAttack(toR, toC)) return false;
    const attacker = this.getUnit(fromR, fromC);
    const defender = this.getUnit(toR, toC);
    if (!attacker || !defender) return false;

    defender.hp -= attacker.atk;
    attacker.acted = true;

    const result = {
      damage: attacker.atk,
      defenderHpLeft: Math.max(0, defender.hp),
      killed: false
    };

    if (defender.hp <= 0) {
      this.killUnit(toR, toC);
      result.killed = true;
    }

    this.deselect();
    this.checkWin();
    return result;
  },

  killUnit(r, c) {
    const key = this.key(r, c);
    const unit = this.units[key];
    if (!unit) return;
    this.cemetery.push({ ...unit, diedOnTurn: this.turn });
    delete this.units[key];
  },

  checkWin() {
    let playerAlive = false, aiAlive = false;
    for (const u of Object.values(this.units)) {
      if (u.type === 'magus' && u.owner === 'player') playerAlive = true;
      if (u.type === 'magus' && u.owner === 'ai') aiAlive = true;
    }
    if (!playerAlive) { this.gameOver = true; this.winner = 'ai'; }
    else if (!aiAlive) { this.gameOver = true; this.winner = 'player'; }
  },

  // ---- Carte e evocazione ----
  selectCard(index) {
    if (this.gameOver || this.currentPlayer !== 'player') return false;
    this.deselect();

    const hand = this.hands.player;
    if (index < 0 || index >= hand.length) return false;

    const card = hand[index];
    if (card.type !== 'creature') return false; // solo creature per ora
    if (this.powa.player < card.cost) return false;

    this.selectedCardIndex = index;

    // Caselle di evocazione: vuote e adiacenti al proprio Magus
    const magus = this.findMagus('player');
    if (!magus) {
      this.possibleSummons = [];
      return false;
    }

    this.possibleSummons = this.getOrthogonal(magus.r, magus.c)
      .filter(p => this.isEmpty(p.r, p.c));

    return true;
  },

  summonCreature(r, c) {
    if (this.gameOver || this.selectedCardIndex === null) return false;
    if (!this.canSummonTo(r, c)) return false;

    const hand = this.hands.player;
    const card = hand[this.selectedCardIndex];
    if (!card || this.powa.player < card.cost) return false;

    // Paga Powa
    this.powa.player -= card.cost;

    // Crea unità
    const unit = {
      owner: 'player',
      type: 'creature',
      id: card.id + '-' + Date.now(),
      name: card.name,
      hp: card.hp,
      maxHp: card.hp,
      atk: card.atk,
      hands: card.hands || 1,
      acted: true, // appena evocata non può agire nello stesso turno
      symbol: card.symbol || '👾',
      cardId: card.id
    };

    this.units[this.key(r, c)] = unit;

    // Rimuovi dalla mano
    hand.splice(this.selectedCardIndex, 1);

    this.clearCardSelection();
    return true;
  },

  // ---- Turni ----
  resetActed(owner) {
    for (const u of Object.values(this.units)) {
      if (u.owner === owner) u.acted = false;
    }
  },

  gainPowa(who) {
    const gain = Math.min(this.turn, this.maxPowa);
    this.powa[who] = Math.min(this.powa[who] + gain, this.maxPowa);
  },

  endTurn() {
    if (this.gameOver) return;
    this.deselect();
    this.clearCardSelection();

    if (this.currentPlayer === 'player') {
      this.currentPlayer = 'ai';
      this.gainPowa('ai');
      this.resetActed('ai');
      this.aiTurn();
    }
  },

  // IA v4: prova a evocare una creatura economica, poi attacca o muove
  aiTurn() {
    if (this.gameOver) return;

    // 1. Prova a evocare una creatura se ha Powa
    this.aiTrySummon();

    // 2. Azioni di tutte le unità AI (Magus + creature)
    const aiUnits = [];
    for (const [k, u] of Object.entries(this.units)) {
      if (u.owner === 'ai' && !u.acted) {
        const [r, c] = k.split('-').map(Number);
        aiUnits.push({ r, c, unit: u });
      }
    }

    for (const { r, c, unit } of aiUnits) {
      if (this.gameOver) break;
      this.aiActUnit(r, c, unit);
    }

    this.finishAiTurn();
  },

  aiTrySummon() {
    const hand = this.hands.ai;
    if (!hand.length) return;

    // Prendi la creatura più economica che può permettersi
    const affordable = hand
      .map((card, idx) => ({ card, idx }))
      .filter(({ card }) => card.type === 'creature' && card.cost <= this.powa.ai)
      .sort((a, b) => a.card.cost - b.card.cost);

    if (!affordable.length) return;

    const { card, idx } = affordable[0];
    const magus = this.findMagus('ai');
    if (!magus) return;

    const spots = this.getOrthogonal(magus.r, magus.c)
      .filter(p => this.isEmpty(p.r, p.c));
    if (!spots.length) return;

    // Preferisci caselle più in basso (verso il player)
    spots.sort((a, b) => b.r - a.r);
    const pos = spots[0];

    this.powa.ai -= card.cost;
    this.units[this.key(pos.r, pos.c)] = {
      owner: 'ai',
      type: 'creature',
      id: card.id + '-ai-' + Date.now(),
      name: card.name,
      hp: card.hp,
      maxHp: card.hp,
      atk: card.atk,
      hands: card.hands || 1,
      acted: true,
      symbol: card.symbol || '👾',
      cardId: card.id
    };
    hand.splice(idx, 1);
  },

  aiActUnit(r, c, unit) {
    const adj = this.getOrthogonal(r, c);

    // Attacca se possibile
    const enemies = adj.filter(p => {
      const t = this.getUnit(p.r, p.c);
      return t && t.owner === 'player';
    });
    if (enemies.length > 0) {
      // Preferisci attaccare il Magus se presente
      enemies.sort((a, b) => {
        const ua = this.getUnit(a.r, a.c);
        const ub = this.getUnit(b.r, b.c);
        if (ua.type === 'magus') return -1;
        if (ub.type === 'magus') return 1;
        return 0;
      });
      const target = enemies[0];
      const defender = this.getUnit(target.r, target.c);
      defender.hp -= unit.atk;
      unit.acted = true;
      if (defender.hp <= 0) this.killUnit(target.r, target.c);
      this.checkWin();
      return;
    }

    // Altrimenti muovi verso il basso
    const moves = adj.filter(p => this.isEmpty(p.r, p.c));
    if (moves.length > 0) {
      moves.sort((a, b) => b.r - a.r);
      const choice = moves[0];
      const keyFrom = this.key(r, c);
      const keyTo = this.key(choice.r, choice.c);
      unit.acted = true;
      this.units[keyTo] = unit;
      delete this.units[keyFrom];
    }
  },

  finishAiTurn() {
    if (this.gameOver) return;
    this.turn += 1;
    this.currentPlayer = 'player';
    this.gainPowa('player');
    this.resetActed('player');
  },

  // ---- Stato UI ----
  getState() {
    let playerHp = 0, playerMaxHp = 20;
    let aiHp = 0, aiMaxHp = 20;
    for (const u of Object.values(this.units)) {
      if (u.type === 'magus' && u.owner === 'player') {
        playerHp = u.hp; playerMaxHp = u.maxHp;
      }
      if (u.type === 'magus' && u.owner === 'ai') {
        aiHp = u.hp; aiMaxHp = u.maxHp;
      }
    }

    return {
      turn: this.turn,
      currentPlayer: this.currentPlayer,
      powa: this.powa.player,
      maxPowa: this.maxPowa,
      units: { ...this.units },
      selected: this.selected,
      selectedCardIndex: this.selectedCardIndex,
      possibleMoves: [...this.possibleMoves],
      possibleAttacks: [...this.possibleAttacks],
      possibleSummons: [...this.possibleSummons],
      hand: this.hands.player.map(c => ({ ...c })),
      playerHp, playerMaxHp, aiHp, aiMaxHp,
      gameOver: this.gameOver,
      winner: this.winner,
      cemeteryCount: this.cemetery.length
    };
  }
};
