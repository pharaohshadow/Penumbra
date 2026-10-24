/**
 * Penumbra – Definizione carte (v6)
 * Creature + Torri + Armi.
 * Mano iniziale: 10 carte (6 creature + 2 torri + 2 armi).
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
    id: 'falco',
    name: 'Falco di Horus',
    type: 'creature',
    cost: 2,
    atk: 3,
    hp: 2,
    hands: 1,
    symbol: '🦅',
    desc: 'Attacco dall’alto'
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

  // --- Torri ---
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
  {
    id: 'pilastro',
    name: 'Pilastro del Nilo',
    type: 'tower',
    cost: 3,
    atk: 0,
    hp: 8,
    hands: 0,
    symbol: '🗿',
    passive: 'aura_atk',
    passiveValue: 1,
    desc: 'Alleati adiacenti +1 ATK • Molto resistente'
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
  }
];

/** Crea una copia della mano iniziale (10 carte) */
function createStartingHand() {
  return CARD_POOL.map(c => ({ ...c }));
}
