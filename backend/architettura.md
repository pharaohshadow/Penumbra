# Architettura – Tactical Card Game 5×5

Documento di riferimento per qualsiasi chat futura.  
Contiene: struttura cartelle, responsabilità di ogni file, dipendenze, dove trovare le funzioni principali, flusso di una partita.

---

## 1. Struttura cartelle (backend)

```
backend/
├── README.md                 # Panoramica + comandi CLI
├── architettura.md           # QUESTO FILE
├── main.py                   # Entry-point CLI (loop di gioco interattivo)
├── core/                     # Motore puro (nessuna dipendenza esterna)
│   ├── __init__.py
│   ├── constants.py          # Enum, coordinate, mana, frammenti, ANSI
│   ├── card.py               # Card + CardDatabase (180 carte)
│   ├── unit.py               # Unit sul tabellone
│   ├── tile.py               # Singola casella
│   ├── map_board.py          # Board 5×5 + layout fisso + path
│   ├── player.py             # Stato giocatore (mana, mano, frammenti, corona)
│   └── game_state.py         # Orchestratore: turni, draft, combattimento, carte, quest
├── ai/                       # (vuoto – prossimo)
├── api/                      # (vuoto – FastAPI futuro)
├── data/                     # (vuoto – eventuali JSON)
├── tests/                    # (vuoto)
└── ui/                       # (vuoto – frontend futuro)
```

---

## 2. Dipendenze tra moduli (core)

```
constants.py
    ↑
    ├── card.py  ←── unit.py
    │                 ↑
    ├── tile.py       │
    │                 │
    ├── map_board.py ←┘
    │       ↑
    ├── player.py
    │       ↑
    └── game_state.py  ←── main.py
```

- `constants.py` non importa nessuno.
- `card.py` importa solo `constants`.
- `unit.py` importa `card` + `constants`.
- `tile.py` importa `constants` (+ type hint Unit).
- `map_board.py` importa `tile`, `unit`, `constants`.
- `player.py` importa `card`, `unit`, `constants`.
- `game_state.py` importa tutto il resto del core.
- `main.py` importa solo `GameState` e `Phase`.

---

## 3. Dove trovare le funzioni importanti

### constants.py
| Funzione / Costante | Ruolo |
|---------------------|-------|
| `pos_to_coord(row, col)` | (2,2) → `"C3"` |
| `coord_to_pos("C3")` | → `(2, 2)` |
| `Color`, `CardType`, `TileType`, `Phase`, `Direction` | Enum centrali |
| `MANA_CAP = 6`, `FRAGMENT_COSTS = [0,3,6]` | Regole mana e vite |
| `ALTAR_POS`, `TEMPLE_P1_POSITIONS`, `TEMPLE_P2_POSITIONS` | Layout |

### card.py
| Classe / Funzione | Ruolo |
|-------------------|-------|
| `Card` | Dataclass di una carta |
| `CardDatabase` | Carica tutte le 180 carte |
| `get_card_db()` | Singleton del database |
| `CardDatabase.get_draftable()` | Carte usabili nel draft |
| `CardDatabase.eldrazi` / `.bosses` | Liste filtrate |

### unit.py
| Metodo | Ruolo |
|--------|-------|
| `Unit.take_damage(amount)` | Applica danno (scudi, ReduceDamage, invulnerabilità) |
| `Unit.heal(amount)` | Cura rispettando max HP |
| `Unit.has_keyword(kw)` | Controlla keywords della carta |

### map_board.py
| Metodo | Ruolo |
|--------|-------|
| `Board._setup_fixed_layout()` | Costruisce Templi, Altare, Buff, muri, portali |
| `Board.place_unit` / `remove_unit` / `move_unit` | Gestione unità sulla griglia |
| `Board.get_adjacent_diagonal` | Caselle raggiungibili con 1 passo diagonale |
| `Board.print_board()` | ASCII della mappa |
| `Tile.is_ritual` / `is_portal` / `is_walkable` | Query sulla casella |

### player.py
| Metodo | Ruolo |
|--------|-------|
| `Player.spend_mana` / `refresh_mana` / `increase_mana_max` | Mana |
| `Player.place_fragment(unit)` | Assegna Corona (paga Commander Tax) |
| `Player.lose_fragment()` | Quando la creatura incoronata muore |
| `Player.next_fragment_cost()` | 0 / 3 / 6 |

### game_state.py (cuore del gioco)
| Metodo | Ruolo |
|--------|-------|
| `start_draft()` / `draft_pick()` / `_finish_draft()` | Snake draft + Boss garantito |
| `start_turn()` / `end_turn()` | Ciclo di turno + progressione mana |
| `_spawn_free_1_1()` | Creatura gratuita in zona Tempio |
| `_spawn_neutral()` | Mostro Neutrale X/X |
| `try_move(unit, row, col)` | Movimento o inizio combattimento |
| `_resolve_combat(attacker, defender)` | First Strike → Contrattacco → Rimbalzo |
| `play_card(player_id, hand_index, target_coord)` | Dispatcher Mostro/Trappola/Maledizione |
| `_summon_monster()` | Evocazione solo in zona Tempio |
| `_play_trap()` | Piazza trappola nascosta |
| `_play_curse()` | Effetti base delle maledizioni |
| `summon_eldrazi(player_id, idx, sacrifice_coords)` | Mostrissimi + sacrifici + Cerchio Rituale |
| `_on_enter_tile(unit)` | Trappole + esplorazione + terreni |
| `_apply_event_tile()` | Trasforma la casella dopo esplorazione |
| `_check_main_quest()` | Dominio / Superiorità |
| `_apply_start_of_turn_effects()` | Santuario, Fenditura, Growth, Regenerate |
| `print_state()` | Debug completo |

---

## 4. Flusso di una partita

1. **Init** → `GameState()` crea Board, 2 Player, pool Mostrissimi, mazzo Eventi.
2. **Draft** → `start_draft()` + `draft_pick()` ripetuti → mano 9 carte + 1 Boss.
3. **Turno** → `start_turn()`:
   - progressione mana
   - spawn 1/1
   - spawn Neutrale
   - effetti inizio turno
   - check Main Quest
4. **Azioni giocatore** (CLI o futura API):
   - `try_move` / `play_card` / `summon_eldrazi`
5. **Fine turno** → `end_turn()`:
   - verifica presenza Frammento (altrimenti sconfitta)
   - passa all’altro giocatore
6. **Vittoria** → eliminazione Comandante senza rimpiazzo **oppure** Main Quest.

---

## 5. Convenzioni importanti

- Giocatore 0 = umano (basso, Tempio1, righe alte della griglia stampata)
- Giocatore 1 = IA (alto, Tempio2)
- Movimento **solo diagonale** di 1 passo = 1 mana
- Evocazione Mostri **solo** nelle 3 caselle del proprio Tempio
- Mostrissimi: 0 mana, N sacrifici, almeno uno su casella con `tile.is_ritual == True`
- Carte giocate o distrutte escono definitivamente (nessun cimitero)
- Coordinate sempre nel formato `A1`…`E5` (lettera colonna, numero riga 1-based)

---

## 6. Cosa manca ancora (roadmap)

| Priorità | Feature | Dove andrà |
|----------|---------|------------|
| Alta | IA con priorità | `ai/basic_ai.py` |
| Alta | FastAPI + WebSocket | `api/main.py` |
| Media | Schema Supabase (games, moves, users) | docs + SQL |
| Media | Frontend griglia | repo root `/frontend` o `ui/` |
| Bassa | Effetti avanzati di ogni singola carta | parser in `game_state` o `effects.py` |
| Bassa | Portali (teletrasporto reale) | `_on_enter_tile` + Board |

---

## 7. Come leggere questo progetto in una nuova chat

1. Leggi `README.md` (stato versione + comandi)
2. Leggi `architettura.md` (questo file)
3. Se serve dettaglio di una regola → apri `core/game_state.py` o `core/constants.py`
4. Database carte → `core/card.py` (metodo `_load_all`)

Versione corrente: **v2**
