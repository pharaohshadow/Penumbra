/**
 * Penumbra – Definizione carte (v7)
 * Creature + Torri + Armi + Maledizioni + Trappole.
 * Mano: 10 carte (5 creature + 1 torre + 2 armi + 1 maledizione + 1 trappola).
 */

const CARD_POOL = [
  // --- Creature ---
  {
    id: 'scarab',
    name: 'Scarabeo Guerriero',
    type: 'creature',
    cost: 1,
    atk: 2,
    hp: 2,
    hands: 1,
    symbol: '🪲',
    desc: 'Piccolo ma tenace'
  },
  {
    id: 'cobra',
    name: 'Cobra del Nilo',
    type: 'creature',
    cost: 1,
    atk: 3,
    hp: 1,
    hands: 1,
    symbol: '🐍',
    desc: 'Veloce e velenoso'
  },
  {
    id: 'guardia',
    name: 'Guardia Anubi',
    type: 'creature',
    cost: 2,
    atk: 2,
    hp: 4,
    hands: 2,
    symbol: '🐕',
    desc: 'Difensore fedele • 2 mani'
  },
  {
    id: 'mummia',
    name: 'Mummia Errante',
    type: 'creature',
    cost: 2,
    atk: 1,
    hp: 5,
    hands: 1,
    symbol: '🧟',
    desc: 'Difficile da abbattere'
  },
  {
    id: 'sfinge',
    name: 'Sfinge Minore',
    type: 'creature',
    cost: 3,
    atk: 3,
    hp: 4,
    hands: 2,
    symbol: '🦁',
    desc: 'Potenza e mistero • 2 mani'
  },

  // --- Torre ---
  {
    id: 'obelisco',
    name: 'Obelisco Guardiano',
    type: 'tower',
    cost: 2,
    atk: 0,
    hp: 6,
    hands: 0,
    symbol: '🏛️',
    passive: 'aura_atk',
    passiveValue: 1,
    desc: 'Alleati adiacenti +1 ATK'
  },

  // --- Armi ---
  {
    id: 'khopesh',
    name: 'Khopesh Dorata',
    type: 'weapon',
    cost: 1,
    atkBonus: 2,
    handsRequired: 1,
    symbol: '🗡️',
    desc: '+2 ATK • Richiede 1 mano'
  },
  {
    id: 'scettro',
    name: 'Scettro di Ra',
    type: 'weapon',
    cost: 2,
    atkBonus: 3,
    handsRequired: 1,
    symbol: '🔱',
    desc: '+3 ATK • Richiede 1 mano'
  },

  // --- Maledizione (solo nel proprio turno, effetto immediato) ---
  {
    id: 'maledizione-ankh',
    name: 'Maledizione dell’Ankh',
    type: 'curse',
    cost: 2,
    damage: 4,
    symbol: '💀',
    desc: 'Infligge 4 danni a un nemico a scelta'
  },

  // --- Trappola (si posa nel proprio turno, scatta quando l’avversario attacca) ---
  {
    id: 'trappola-scarabeo',
    name: 'Trappola dello Scarabeo',
    type: 'trap',
    cost: 1,
    damage: 3,
    symbol: '🪤',
    desc: 'Quando un nemico attacca: 3 danni all’attaccante'
  }
];

function createStartingHand() {
  return CARD_POOL.map(c => ({ ...c }));
}
