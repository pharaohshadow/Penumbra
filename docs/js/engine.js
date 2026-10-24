/**
 * Penumbra – Game Engine (v7)
 * Novità v7: Maledizioni (danno immediato) e Trappole (scattano all’attacco nemico).
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
  hands: { player: [], ai: [] },

  // Trappole posate (non sulla griglia)
  traps: { player: [], ai: [] },

  selected: null,
  selectedCardIndex: null,
  possibleMoves: [],
  possibleAttacks: [],
  possibleSummons: [],
  possibleEquips: [],
  possibleCurseTargets: [], // nemici per maledizione

  init() {
    this.turn = 1;
    this.currentPlayer = 'player';
    this.powa = { player: 1, ai: 1 };
    this.units = {};
    this.cemetery = [];
    this.traps = { player: [], ai: [] };
    this.selected = null;
    this.selectedCardIndex = null;
    this.possibleMoves = [];
    this.possibleAttacks = [];
    this.possibleSummons = [];
    this.possibleEquips = [];
    this.possibleCurseTargets = [];
    this.gameOver = false;
    this.winner = null;

    this.units['3-2'] = {
      owner: 'player', type: 'magus', id: 'player-magus',
      hp: 20, maxHp: 20, atk: 1, hands: 2, acted: false, symbol: '𓁹',
      weapons: []
    };
    this.units['0-2'] = {
      owner: 'ai', type: 'magus', id: 'ai-magus',
      hp: 20, maxHp: 20, atk: 1, hands: 2, acted: false, symbol: '𓀀',
      weapons: []
    };

    this.hands.player = createStartingHand();
    this.hands.ai = createStartingHand();
  },

  key(r, c) { return `${r}-${c}`; },
  isInside(r, c) { return r >= 0 && r < ROWS && c >= 0 && c < COLS; },
  isEmpty(r, c) { return !this.units[this.key(r, c)]; },
  getUnit(r, c) { return this.units[this.key(r, c)] || null; },

  getOrthogonal(r, c) {
    const dirs = [[-1,0],[1,0],[0,-1],[0,1]];
    return dirs.map(([dr,dc]) => ({ r: r+dr, c: c+dc })).filter(p => this.isInside(p.r, p.c));
  },

  findMagus(owner) {
    for (const [k, u] of Object.entries(this.units)) {
      if (u.owner === owner && u.type === 'magus') {
        const [r, c] = k.split('-').map(Number);
        return { r, c, unit: u };
      }
    }
    return null;
  },

  getUsedHands(unit) {
    if (!unit.weapons || !unit.weapons.length) return 0;
    return unit.weapons.reduce((s, w) => s + (w.handsRequired || 1), 0);
  },
  getFreeHands(unit) {
    return Math.max(0, (unit.hands || 0) - this.getUsedHands(unit));
  },

  getAuraAtkBonus(r, c, owner) {
    let bonus = 0;
    for (const pos of this.getOrthogonal(r, c)) {
      const u = this.getUnit(pos.r, pos.c);
      if (u && u.owner === owner && u.type === 'tower' && u.passive === 'aura_atk') {
        bonus += (u.passiveValue || 1);
      }
    }
    return bonus;
  },

  getWeaponAtkBonus(unit) {
    if (!unit.weapons || !unit.weapons.length) return 0;
    return unit.weapons.reduce((s, w) => s + (w.atkBonus || 0), 0);
  },

  getEffectiveAtk(r, c) {
    const unit = this.getUnit(r, c);
    if (!unit || unit.type === 'tower') return 0;
    return unit.atk + this.getWeaponAtkBonus(unit) + this.getAuraAtkBonus(r, c, unit.owner);
  },

  // ---- Selezione unità ----
  selectUnit(r, c) {
    if (this.gameOver) return false;
    this.clearCardSelection();
    const unit = this.getUnit(r, c);
    if (!unit || unit.owner !== this.currentPlayer) return false;
    if (this.currentPlayer !== 'player') return false;
    if (unit.acted || unit.type === 'tower') return false;

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
    this.possibleEquips = [];
    this.possibleCurseTargets = [];
  },

  canMoveTo(r, c) { return this.possibleMoves.some(m => m.r === r && m.c === c); },
  canAttack(r, c) { return this.possibleAttacks.some(a => a.r === r && a.c === c); },
  canSummonTo(r, c) { return this.possibleSummons.some(s => s.r === r && s.c === c); },
  canEquipTo(r, c) { return this.possibleEquips.some(e => e.r === r && e.c === c); },
  canCurse(r, c) { return this.possibleCurseTargets.some(t => t.r === r && t.c === c); },

  // ---- Movimento ----
  moveUnit(fromR, fromC, toR, toC) {
    if (this.gameOver || !this.canMoveTo(toR, toC)) return false;
    const keyFrom = this.key(fromR, fromC);
    const keyTo = this.key(toR, toC);
    const unit = this.units[keyFrom];
    if (!unit || unit.type === 'tower') return false;
    unit.acted = true;
    delete this.units[keyFrom];
    this.units[keyTo] = unit;
    this.deselect();
    return true;
  },

  // ---- Attacco (con trigger trappole) ----
  attackUnit(fromR, fromC, toR, toC) {
    if (this.gameOver || !this.canAttack(toR, toC)) return false;
    const attacker = this.getUnit(fromR, fromC);
    const defender = this.getUnit(toR, toC);
    if (!attacker || !defender || attacker.type === 'tower') return false;

    const damage = this.getEffectiveAtk(fromR, fromC);
    defender.hp -= damage;
    attacker.acted = true;

    const result = {
      damage,
      defenderHpLeft: Math.max(0, defender.hp),
      killed: false,
      trapTriggered: null
    };

    if (defender.hp <= 0) {
      this.killUnit(toR, toC);
      result.killed = true;
    }

    // Trappole del difensore: scattano sull’attaccante
    const trapResult = this.triggerTrap(defender.owner, fromR, fromC);
    if (trapResult) result.trapTriggered = trapResult;

    this.deselect();
    this.checkWin();
    return result;
  },

  /** Attiva la prima trappola del proprietario contro l’attaccante */
  triggerTrap(trapOwner, attackerR, attackerC) {
    const list = this.traps[trapOwner];
    if (!list || !list.length) return null;

    const trap = list.shift(); // consuma la prima
    const attacker = this.getUnit(attackerR, attackerC);
    if (!attacker) return { name: trap.name, damage: trap.damage, killed: false };

    attacker.hp -= trap.damage;
    const killed = attacker.hp <= 0;
    if (killed) this.killUnit(attackerR, attackerC);

    return { name: trap.name, damage: trap.damage, killed };
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

  // ---- Carte ----
  selectCard(index) {
    if (this.gameOver || this.currentPlayer !== 'player') return false;
    this.deselect();

    const hand = this.hands.player;
    if (index < 0 || index >= hand.length) return false;
    const card = hand[index];
    if (this.powa.player < card.cost) return false;

    this.selectedCardIndex = index;
    this.possibleSummons = [];
    this.possibleEquips = [];
    this.possibleCurseTargets = [];

    if (card.type === 'creature' || card.type === 'tower') {
      const magus = this.findMagus('player');
      if (!magus) return false;
      this.possibleSummons = this.getOrthogonal(magus.r, magus.c)
        .filter(p => this.isEmpty(p.r, p.c));
      return true;
    }

    if (card.type === 'weapon') {
      for (const [k, u] of Object.entries(this.units)) {
        if (u.owner !== 'player' || u.type === 'tower') continue;
        if (this.getFreeHands(u) >= (card.handsRequired || 1)) {
          const [r, c] = k.split('-').map(Number);
          this.possibleEquips.push({ r, c });
        }
      }
      return this.possibleEquips.length > 0;
    }

    if (card.type === 'curse') {
      // Tutti i nemici sulla griglia
      for (const [k, u] of Object.entries(this.units)) {
        if (u.owner === 'player') continue;
        const [r, c] = k.split('-').map(Number);
        this.possibleCurseTargets.push({ r, c });
      }
      return this.possibleCurseTargets.length > 0;
    }

    if (card.type === 'trap') {
      // Si posa subito, senza target
      return true;
    }

    return false;
  },

  summonCard(r, c) {
    if (this.gameOver || this.selectedCardIndex === null) return false;
    if (!this.canSummonTo(r, c)) return false;
    const hand = this.hands.player;
    const card = hand[this.selectedCardIndex];
    if (!card || this.powa.player < card.cost) return false;
    if (card.type !== 'creature' && card.type !== 'tower') return false;

    this.powa.player -= card.cost;
    this.units[this.key(r, c)] = {
      owner: 'player', type: card.type, id: card.id + '-' + Date.now(),
      name: card.name, hp: card.hp, maxHp: card.hp, atk: card.atk || 0,
      hands: card.hands || 0, acted: true, symbol: card.symbol || '👾',
      cardId: card.id, passive: card.passive || null, passiveValue: card.passiveValue || 0,
      weapons: []
    };
    hand.splice(this.selectedCardIndex, 1);
    this.clearCardSelection();
    return true;
  },

  equipWeapon(r, c) {
    if (this.gameOver || this.selectedCardIndex === null) return false;
    if (!this.canEquipTo(r, c)) return false;
    const hand = this.hands.player;
    const card = hand[this.selectedCardIndex];
    if (!card || card.type !== 'weapon' || this.powa.player < card.cost) return false;
    const unit = this.getUnit(r, c);
    if (!unit || unit.owner !== 'player') return false;
    if (this.getFreeHands(unit) < (card.handsRequired || 1)) return false;

    this.powa.player -= card.cost;
    if (!unit.weapons) unit.weapons = [];
    unit.weapons.push({
      id: card.id, name: card.name, atkBonus: card.atkBonus || 0,
      handsRequired: card.handsRequired || 1, symbol: card.symbol
    });
    hand.splice(this.selectedCardIndex, 1);
    this.clearCardSelection();
    return true;
  },

  /** Lancia maledizione su un nemico */
  castCurse(r, c) {
    if (this.gameOver || this.selectedCardIndex === null) return false;
    if (!this.canCurse(r, c)) return false;
    const hand = this.hands.player;
    const card = hand[this.selectedCardIndex];
    if (!card || card.type !== 'curse' || this.powa.player < card.cost) return false;

    const target = this.getUnit(r, c);
    if (!target || target.owner === 'player') return false;

    this.powa.player -= card.cost;
    const dmg = card.damage || 3;
    target.hp -= dmg;

    const result = { damage: dmg, killed: false, name: card.name };
    if (target.hp <= 0) {
      this.killUnit(r, c);
      result.killed = true;
    }

    hand.splice(this.selectedCardIndex, 1);
    this.clearCardSelection();
    this.checkWin();
    return result;
  },

  /** Posa una trappola (nessun target) */
  setTrap() {
    if (this.gameOver || this.selectedCardIndex === null) return false;
    const hand = this.hands.player;
    const card = hand[this.selectedCardIndex];
    if (!card || card.type !== 'trap' || this.powa.player < card.cost) return false;

    this.powa.player -= card.cost;
    this.traps.player.push({
      id: card.id, name: card.name, damage: card.damage || 2, symbol: card.symbol
    });
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

  // ---- IA ----
  aiTurn() {
    if (this.gameOver) return;
    this.aiTrySetTrap();
    this.aiTryCurse();
    this.aiTryEquip();
    this.aiTrySummon();

    const aiUnits = [];
    for (const [k, u] of Object.entries(this.units)) {
      if (u.owner === 'ai' && !u.acted && u.type !== 'tower') {
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

  aiTrySetTrap() {
    const hand = this.hands.ai;
    const idx = hand.findIndex(c => c.type === 'trap' && c.cost <= this.powa.ai);
    if (idx < 0) return;
    const card = hand[idx];
    this.powa.ai -= card.cost;
    this.traps.ai.push({
      id: card.id, name: card.name, damage: card.damage || 2, symbol: card.symbol
    });
    hand.splice(idx, 1);
  },

  aiTryCurse() {
    const hand = this.hands.ai;
    const idx = hand.findIndex(c => c.type === 'curse' && c.cost <= this.powa.ai);
    if (idx < 0) return;
    // Mira al Magus player se vivo, altrimenti prima unità
    let targetKey = null;
    for (const [k, u] of Object.entries(this.units)) {
      if (u.owner === 'player' && u.type === 'magus') { targetKey = k; break; }
    }
    if (!targetKey) {
      for (const [k, u] of Object.entries(this.units)) {
        if (u.owner === 'player') { targetKey = k; break; }
      }
    }
    if (!targetKey) return;

    const card = hand[idx];
    const [r, c] = targetKey.split('-').map(Number);
    const target = this.getUnit(r, c);
    this.powa.ai -= card.cost;
    target.hp -= (card.damage || 3);
    if (target.hp <= 0) this.killUnit(r, c);
    hand.splice(idx, 1);
    this.checkWin();
  },

  aiTryEquip() {
    const hand = this.hands.ai;
    const weapons = hand.map((card, idx) => ({ card, idx }))
      .filter(({ card }) => card.type === 'weapon' && card.cost <= this.powa.ai);
    for (const { card, idx } of weapons) {
      for (const u of Object.values(this.units)) {
        if (u.owner !== 'ai' || u.type === 'tower') continue;
        if (this.getFreeHands(u) >= (card.handsRequired || 1)) {
          this.powa.ai -= card.cost;
          if (!u.weapons) u.weapons = [];
          u.weapons.push({
            id: card.id, name: card.name, atkBonus: card.atkBonus || 0,
            handsRequired: card.handsRequired || 1, symbol: card.symbol
          });
          hand.splice(idx, 1);
          return;
        }
      }
    }
  },

  aiTrySummon() {
    const hand = this.hands.ai;
    const affordable = hand.map((card, idx) => ({ card, idx }))
      .filter(({ card }) =>
        (card.type === 'creature' || card.type === 'tower') && card.cost <= this.powa.ai
      )
      .sort((a, b) => a.card.cost - b.card.cost);
    if (!affordable.length) return;
    const { card, idx } = affordable[0];
    const magus = this.findMagus('ai');
    if (!magus) return;
    const spots = this.getOrthogonal(magus.r, magus.c).filter(p => this.isEmpty(p.r, p.c));
    if (!spots.length) return;
    spots.sort((a, b) => b.r - a.r);
    const pos = spots[0];
    this.powa.ai -= card.cost;
    this.units[this.key(pos.r, pos.c)] = {
      owner: 'ai', type: card.type, id: card.id + '-ai-' + Date.now(),
      name: card.name, hp: card.hp, maxHp: card.hp, atk: card.atk || 0,
      hands: card.hands || 0, acted: true, symbol: card.symbol || '👾',
      cardId: card.id, passive: card.passive || null, passiveValue: card.passiveValue || 0,
      weapons: []
    };
    hand.splice(idx, 1);
  },

  aiActUnit(r, c, unit) {
    const adj = this.getOrthogonal(r, c);
    const enemies = adj.filter(p => {
      const t = this.getUnit(p.r, p.c);
      return t && t.owner === 'player';
    });
    if (enemies.length > 0) {
      enemies.sort((a, b) => {
        const ua = this.getUnit(a.r, a.c), ub = this.getUnit(b.r, b.c);
        if (ua.type === 'magus') return -1;
        if (ub.type === 'magus') return 1;
        return 0;
      });
      const target = enemies[0];
      const defender = this.getUnit(target.r, target.c);
      const damage = this.getEffectiveAtk(r, c);
      defender.hp -= damage;
      unit.acted = true;
      if (defender.hp <= 0) this.killUnit(target.r, target.c);
      // Trappola del player
      this.triggerTrap('player', r, c);
      this.checkWin();
      return;
    }
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

  getState() {
    let playerHp = 0, playerMaxHp = 20, aiHp = 0, aiMaxHp = 20;
    for (const u of Object.values(this.units)) {
      if (u.type === 'magus' && u.owner === 'player') { playerHp = u.hp; playerMaxHp = u.maxHp; }
      if (u.type === 'magus' && u.owner === 'ai') { aiHp = u.hp; aiMaxHp = u.maxHp; }
    }
    const unitsWithBonus = {};
    for (const [k, u] of Object.entries(this.units)) {
      const [r, c] = k.split('-').map(Number);
      unitsWithBonus[k] = {
        ...u,
        effectiveAtk: this.getEffectiveAtk(r, c),
        freeHands: this.getFreeHands(u)
      };
    }
    return {
      turn: this.turn,
      currentPlayer: this.currentPlayer,
      powa: this.powa.player,
      maxPowa: this.maxPowa,
      units: unitsWithBonus,
      selected: this.selected,
      selectedCardIndex: this.selectedCardIndex,
      possibleMoves: [...this.possibleMoves],
      possibleAttacks: [...this.possibleAttacks],
      possibleSummons: [...this.possibleSummons],
      possibleEquips: [...this.possibleEquips],
      possibleCurseTargets: [...this.possibleCurseTargets],
      hand: this.hands.player.map(c => ({ ...c })),
      trapsPlayer: this.traps.player.length,
      trapsAi: this.traps.ai.length,
      playerHp, playerMaxHp, aiHp, aiMaxHp,
      gameOver: this.gameOver,
      winner: this.winner,
      cemeteryCount: this.cemetery.length
    };
  }
};
