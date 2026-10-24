/**
 * Penumbra – Game Engine (v3)
 * Logica pura di gioco, senza DOM.
 * Novità v3: attacco melee, danni, morte, cimitero, vittoria/sconfitta.
 */

const ROWS = 4;
const COLS = 5;

const Game = {
  turn: 1,
  currentPlayer: 'player', // 'player' | 'ai'
  powa: { player: 1, ai: 1 },
  maxPowa: 6,
  gameOver: false,
  winner: null, // 'player' | 'ai' | null

  // Unità sulla griglia: chiave "r-c"
  // Ogni unità: { owner, type, id, hp, maxHp, atk, acted }
  units: {},

  // Cimitero: array di unità morte
  cemetery: [],

  selected: null,       // { r, c }
  possibleMoves: [],    // caselle vuote adiacenti
  possibleAttacks: [],  // caselle con nemici adiacenti

  // ---- Inizializzazione ----
  init() {
    this.turn = 1;
    this.currentPlayer = 'player';
    this.powa = { player: 1, ai: 1 };
    this.units = {};
    this.cemetery = [];
    this.selected = null;
    this.possibleMoves = [];
    this.possibleAttacks = [];
    this.gameOver = false;
    this.winner = null;

    // Magus Player (basso centro)
    this.units['3-2'] = {
      owner: 'player',
      type: 'magus',
      id: 'player-magus',
      hp: 20,
      maxHp: 20,
      atk: 1,
      acted: false
    };

    // Magus AI (alto centro)
    this.units['0-2'] = {
      owner: 'ai',
      type: 'magus',
      id: 'ai-magus',
      hp: 20,
      maxHp: 20,
      atk: 1,
      acted: false
    };
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

  getOrthogonal(r, c) {
    const dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]];
    const result = [];
    for (const [dr, dc] of dirs) {
      const nr = r + dr;
      const nc = c + dc;
      if (this.isInside(nr, nc)) result.push({ r: nr, c: nc });
    }
    return result;
  },

  // ---- Selezione ----
  selectUnit(r, c) {
    if (this.gameOver) return false;

    const unit = this.getUnit(r, c);
    if (!unit) return false;
    if (unit.owner !== this.currentPlayer) return false;
    if (this.currentPlayer !== 'player') return false;
    if (unit.acted) return false; // già ha agito questo turno

    this.selected = { r, c };

    const adj = this.getOrthogonal(r, c);

    this.possibleMoves = adj.filter(pos => this.isEmpty(pos.r, pos.c));

    this.possibleAttacks = adj.filter(pos => {
      const target = this.getUnit(pos.r, pos.c);
      return target && target.owner !== unit.owner;
    });

    return true;
  },

  deselect() {
    this.selected = null;
    this.possibleMoves = [];
    this.possibleAttacks = [];
  },

  canMoveTo(r, c) {
    return this.possibleMoves.some(m => m.r === r && m.c === c);
  },

  canAttack(r, c) {
    return this.possibleAttacks.some(a => a.r === r && a.c === c);
  },

  // ---- Movimento ----
  moveUnit(fromR, fromC, toR, toC) {
    if (this.gameOver) return false;
    if (!this.canMoveTo(toR, toC)) return false;

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

  // ---- Attacco melee ----
  attackUnit(fromR, fromC, toR, toC) {
    if (this.gameOver) return false;
    if (!this.canAttack(toR, toC)) return false;

    const attacker = this.getUnit(fromR, fromC);
    const defender = this.getUnit(toR, toC);
    if (!attacker || !defender) return false;

    // Infligge danno
    defender.hp -= attacker.atk;
    attacker.acted = true;

    // Messaggio di combattimento (la UI lo può mostrare)
    const result = {
      attackerId: attacker.id,
      defenderId: defender.id,
      damage: attacker.atk,
      defenderHpLeft: Math.max(0, defender.hp)
    };

    // Morte?
    if (defender.hp <= 0) {
      this.killUnit(toR, toC);
      result.killed = true;
    } else {
      result.killed = false;
    }

    this.deselect();
    this.checkWin();
    return result;
  },

  killUnit(r, c) {
    const key = this.key(r, c);
    const unit = this.units[key];
    if (!unit) return;

    // Va al cimitero
    this.cemetery.push({
      ...unit,
      diedOnTurn: this.turn
    });

    delete this.units[key];

    // TODO futuro: effetti "on death"
  },

  checkWin() {
    // Cerca se i Magus sono ancora vivi
    let playerAlive = false;
    let aiAlive = false;

    for (const u of Object.values(this.units)) {
      if (u.type === 'magus' && u.owner === 'player') playerAlive = true;
      if (u.type === 'magus' && u.owner === 'ai') aiAlive = true;
    }

    if (!playerAlive) {
      this.gameOver = true;
      this.winner = 'ai';
    } else if (!aiAlive) {
      this.gameOver = true;
      this.winner = 'player';
    }
  },

  // ---- Reset acted a inizio turno ----
  resetActed(owner) {
    for (const u of Object.values(this.units)) {
      if (u.owner === owner) u.acted = false;
    }
  },

  // ---- Turni e Powa ----
  gainPowa(who) {
    const gain = Math.min(this.turn, this.maxPowa);
    this.powa[who] = Math.min(this.powa[who] + gain, this.maxPowa);
  },

  endTurn() {
    if (this.gameOver) return;
    this.deselect();

    if (this.currentPlayer === 'player') {
      this.currentPlayer = 'ai';
      this.gainPowa('ai');
      this.resetActed('ai');
      this.aiTurn();
    }
  },

  // IA v3: se può attaccare lo fa, altrimenti si avvicina
  aiTurn() {
    if (this.gameOver) return;

    // Trova Magus AI
    let aiPos = null;
    let aiUnit = null;
    for (const [k, u] of Object.entries(this.units)) {
      if (u.owner === 'ai' && u.type === 'magus') {
        const [r, c] = k.split('-').map(Number);
        aiPos = { r, c };
        aiUnit = u;
        break;
      }
    }
    if (!aiPos) {
      this.finishAiTurn();
      return;
    }

    // 1. Cerca nemici adiacenti → attacca il primo
    const adj = this.getOrthogonal(aiPos.r, aiPos.c);
    const enemies = adj.filter(pos => {
      const t = this.getUnit(pos.r, pos.c);
      return t && t.owner === 'player';
    });

    if (enemies.length > 0) {
      // Attacca
      const target = enemies[0];
      const defender = this.getUnit(target.r, target.c);
      defender.hp -= aiUnit.atk;
      aiUnit.acted = true;

      if (defender.hp <= 0) {
        this.killUnit(target.r, target.c);
      }
      this.checkWin();
      this.finishAiTurn();
      return;
    }

    // 2. Nessun nemico vicino → muovi verso il player
    const moves = adj.filter(pos => this.isEmpty(pos.r, pos.c));
    if (moves.length > 0) {
      // Preferisci muoverti verso il basso (verso il player)
      moves.sort((a, b) => b.r - a.r);
      const choice = moves[0];
      const keyFrom = this.key(aiPos.r, aiPos.c);
      const keyTo = this.key(choice.r, choice.c);
      aiUnit.acted = true;
      this.units[keyTo] = aiUnit;
      delete this.units[keyFrom];
    }

    this.finishAiTurn();
  },

  finishAiTurn() {
    if (this.gameOver) return;

    this.turn += 1;
    this.currentPlayer = 'player';
    this.gainPowa('player');
    this.resetActed('player');
  },

  // ---- Stato per la UI ----
  getState() {
    // Calcola HP dei Magus dalla griglia (o 0 se morti)
    let playerHp = 0, playerMaxHp = 20;
    let aiHp = 0, aiMaxHp = 20;

    for (const u of Object.values(this.units)) {
      if (u.type === 'magus' && u.owner === 'player') {
        playerHp = u.hp;
        playerMaxHp = u.maxHp;
      }
      if (u.type === 'magus' && u.owner === 'ai') {
        aiHp = u.hp;
        aiMaxHp = u.maxHp;
      }
    }

    return {
      turn: this.turn,
      currentPlayer: this.currentPlayer,
      powa: this.powa.player,
      maxPowa: this.maxPowa,
      units: { ...this.units },
      selected: this.selected,
      possibleMoves: [...this.possibleMoves],
      possibleAttacks: [...this.possibleAttacks],
      playerHp,
      playerMaxHp,
      aiHp,
      aiMaxHp,
      gameOver: this.gameOver,
      winner: this.winner,
      cemeteryCount: this.cemetery.length
    };
  }
};
