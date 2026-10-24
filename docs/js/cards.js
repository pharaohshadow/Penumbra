/**
 * Penumbra – Definizione carte (v4)
 * Carte base egizie, parodie leggere.
 * Tutti i giocatori partono con lo stesso mazzo di 10 carte.
 */

const CARD_POOL = [
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
    desc: 'Difensore fedele'
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
    desc: 'Potenza e mistero'
  },
  {
    id: 'scorpione',
    name: 'Scorpione Dorato',
    type: 'creature',
    cost: 1,
    atk: 2,
    hp: 1,
    hands: 1,
    symbol: '🦂',
    desc: 'Punta letale'
  },
  {
    id: 'soldato',
    name: 'Soldato di Ra',
    type: 'creature',
    cost: 2,
    atk: 2,
    hp: 3,
    hands: 1,
    symbol: '⚔️',
    desc: 'Fanteria del sole'
  },
  {
    id: 'gatto',
    name: 'Gatto di Bastet',
    type: 'creature',
    cost: 1,
    atk: 1,
    hp: 3,
    hands: 1,
    symbol: '🐈',
    desc: 'Agile e furbo'
  },
  {
    id: 'ibis',
    name: 'Ibis Saggio',
    type: 'creature',
    cost: 3,
    atk: 2,
    hp: 5,
    hands: 1,
    symbol: '🐦',
    desc: 'Conoscenza antica'
  }
];

/** Crea una copia della mano iniziale (10 carte) */
function createStartingHand() {
  return CARD_POOL.map(c => ({ ...c }));
}
