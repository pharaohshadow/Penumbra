# Architettura – Tactical Card Game 5×5 (v3)

Documento di riferimento per qualsiasi chat futura.

---

## 1. Struttura cartelle (backend)

```
backend/
├── README.md
├── architettura.md           # QUESTO FILE
├── main.py                   # CLI + loop (umano vs IA)
├── core/                     # Motore puro
│   ├── constants.py
│   ├── card.py               # 180 carte
│   ├── unit.py
│   ├── tile.py
│   ├── map_board.py
│   ├── player.py
│   └── game_state.py         # Turni, draft, combattimento, carte, quest, eldrazi
├── ai/
│   ├── __init__.py
│   └── basic_ai.py           # IA con priorità
├── api/                      # (vuoto – FastAPI)
├── data/
├── tests/
└── ui/
```

Repo root previsto:

```
Penumbra/
├── backend/     ← questa cartella
└── docs/        ← GitHub Pages (già creato)
```

---

## 2. Dipendenze

```
constants.py
    ↑
card.py ← unit.py
tile.py
map_board.py ← unit, tile
player.py ← card, unit
game_state.py ← tutto il core
    ↑
basic_ai.py ← game_state, unit, player, constants
    ↑
main.py ← GameState, BasicAI
```

---

## 3. Dove trovare le funzioni

### core/ (invariato rispetto a v2 + piccole aggiunte)

| File | Funzioni chiave |
|------|-----------------|
| `game_state.py` | `start_draft`, `draft_pick`, `start_turn`, `end_turn`, `try_move`, `_resolve_combat`, `play_card`, `_summon_monster`, `_play_trap`, `_play_curse`, `summon_eldrazi`, `_on_enter_tile`, `_check_main_quest`, `_apply_start_of_turn_effects` |
| `map_board.py` | `place_unit`, `move_unit`, `get_adjacent_diagonal`, `print_board` |
| `player.py` | `place_fragment`, `spend_mana`, `next_fragment_cost` |
| `card.py` | `get_card_db()`, `CardDatabase._load_all` |

### ai/basic_ai.py (nuovo)

| Metodo | Ruolo |
|--------|-------|
| `BasicAI.take_turn()` | Esegue l’intero turno IA e chiama `end_turn()` |
| `_try_place_fragment()` | Assegna Corona se manca |
| `_try_play_cards()` | Gioca 1-2 carte economiche |
| `_try_combat_or_move()` | Attacca corona/nemici o muove verso obiettivi |
| `_try_eldrazi()` | Sacrifici + Cerchio Rituale → Mostrissimo |
| `_choose_move_target()` | Scoring caselle (Altare, corona nemica, avanzata) |

---

## 4. Flusso partita (con IA)

1. Draft automatico (snake)
2. Turno umano (P0) → comandi CLI
3. `e` → `end_turn()` → `start_turn()` per P1
4. `main.py` vede `player.is_ai` → `BasicAI.take_turn()`
5. IA esegue azioni → `end_turn()` → di nuovo umano
6. Vittoria: Frammento perso senza rimpiazzo **oppure** Main Quest

---

## 5. Convenzioni

- P0 = umano (basso, Tempio1)
- P1 = IA (alto, Tempio2)
- Movimento solo diagonale, 1 mana
- Evocazione Mostri solo zona Tempio
- Mostrissimi: 0 mana, N sacrifici, uno su `tile.is_ritual`
- Coordinate `A1`–`E5`

---

## 6. Roadmap residua

| Priorità | Feature | Dove |
|----------|---------|------|
| Alta | FastAPI + WebSocket | `api/` |
| Alta | Schema Supabase | SQL + docs |
| Media | Frontend griglia | repo `/frontend` |
| Media | Deploy Render | — |
| Bassa | Effetti avanzati carta per carta | `game_state` / `effects.py` |
| Bassa | Teletrasporto portali completo | `_on_enter_tile` |

---

## 7. Come usare in una nuova chat

1. Leggi `README.md` (versione + comandi)
2. Leggi `architettura.md` (questo file)
3. Dettaglio regole → `core/game_state.py`
4. Database carte → `core/card.py`
5. Comportamento IA → `ai/basic_ai.py`

**Versione corrente: v3**
