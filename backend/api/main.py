"""
FastAPI – espone il motore di gioco + serve la UI HTML.
Avvio locale:
  cd backend
  pip install fastapi uvicorn
  uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
Poi apri http://localhost:8000
"""

from __future__ import annotations
import sys
from pathlib import Path

# Permette di importare core/ e ai/ dalla root backend
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from core.game_state import GameState
from core.constants import Phase, pos_to_coord, coord_to_pos
from ai.basic_ai import BasicAI

app = FastAPI(title="Penumbra Tactical Card Game", version="0.4")

# Partita in memoria (una sola sessione per prototipo)
_game: Optional[GameState] = None


def get_game() -> GameState:
    global _game
    if _game is None:
        _game = GameState(human_name="Tu", ai_name="AI Overlord")
        _game.start_draft()
        # Auto-draft rapido
        while _game.phase == Phase.DRAFT:
            pack = _game.get_current_pack()
            if not pack:
                break
            for pid in (0, 1):
                if _game.phase != Phase.DRAFT:
                    break
                pack = _game.get_current_pack()
                if not pack:
                    break
                _game.draft_pick(pid, 0)
        _game.start_turn()
        units = _game.board.get_units_of_player(0)
        if units:
            _game.players[0].place_fragment(units[0])
    return _game


def serialize_state(gs: GameState) -> dict:
    """Stato leggero per il frontend."""
    board = []
    for r in range(5):
        row = []
        for c in range(5):
            tile = gs.board.get_tile(r, c)
            unit = gs.board.get_unit_at(r, c)
            cell = {
                "coord": pos_to_coord(r, c),
                "tile": tile.tile_type.value if tile else "Vuoto",
                "explored": tile.explored if tile else True,
                "trap": tile.trap_card_id is not None if tile else False,
                "unit": None,
            }
            if unit:
                cell["unit"] = {
                    "name": unit.card.name,
                    "atk": unit.current_atk,
                    "hp": unit.current_hp,
                    "owner": unit.owner_id,
                    "crown": unit.has_fragment,
                    "coord": unit.coord,
                }
            row.append(cell)
        board.append(row)

    def player_data(p):
        return {
            "id": p.id,
            "name": p.name,
            "mana": p.mana,
            "mana_max": p.mana_max,
            "fragments": p.fragments_remaining,
            "hand": [
                {
                    "index": i,
                    "id": c.id,
                    "name": c.name,
                    "cost": c.cost,
                    "type": c.card_type.value,
                    "atk": c.atk,
                    "hp": c.hp,
                    "text": c.text[:80] if c.text else "",
                }
                for i, c in enumerate(p.hand)
            ],
            "crown": p.crown_unit.coord if p.crown_unit and p.crown_unit.is_alive else None,
            "is_ai": p.is_ai,
            "lost": p.has_lost,
        }

    eldrazi = [
        {
            "index": i,
            "name": e.name,
            "atk": e.atk,
            "hp": e.hp,
            "sacrifice": e.sacrifice_cost,
        }
        for i, e in enumerate(gs.eldrazi_pool)
    ]

    return {
        "turn": gs.turn,
        "phase": gs.phase.name,
        "current_player": gs.current_player_id,
        "winner": gs.winner,
        "main_quest": gs.main_quest,
        "board": board,
        "players": [player_data(p) for p in gs.players],
        "eldrazi": eldrazi,
        "log": gs.log[-15:],
    }


# ---------- Models ----------
class MoveReq(BaseModel):
    from_coord: str
    to_coord: str


class PlayReq(BaseModel):
    hand_index: int
    target_coord: Optional[str] = None


class EldraziReq(BaseModel):
    eldrazi_index: int
    sacrifice_coords: List[str]


# ---------- Routes ----------
@app.get("/")
def index():
    static = ROOT / "static" / "index.html"
    if static.exists():
        return FileResponse(static)
    return JSONResponse({"error": "static/index.html mancante"}, status_code=404)


@app.get("/api/state")
def api_state():
    return serialize_state(get_game())


@app.post("/api/new")
def api_new():
    global _game
    _game = None
    return serialize_state(get_game())


@app.post("/api/move")
def api_move(body: MoveReq):
    gs = get_game()
    if gs.current_player_id != 0 or gs.phase == Phase.GAME_OVER:
        raise HTTPException(400, "Non è il tuo turno o partita finita")
    try:
        fr, fc = coord_to_pos(body.from_coord.upper())
        tr, tc = coord_to_pos(body.to_coord.upper())
    except Exception:
        raise HTTPException(400, "Coordinate non valide")
    unit = gs.board.get_unit_at(fr, fc)
    if not unit or unit.owner_id != 0:
        raise HTTPException(400, "Nessuna tua unità su quella casella")
    ok = gs.try_move(unit, tr, tc)
    if not ok:
        raise HTTPException(400, "Mossa non valida")
    return serialize_state(gs)


@app.post("/api/play")
def api_play(body: PlayReq):
    gs = get_game()
    if gs.current_player_id != 0 or gs.phase == Phase.GAME_OVER:
        raise HTTPException(400, "Non è il tuo turno o partita finita")
    ok = gs.play_card(0, body.hand_index, body.target_coord.upper() if body.target_coord else None)
    if not ok:
        raise HTTPException(400, "Carta non giocabile")
    return serialize_state(gs)


@app.post("/api/eldrazi")
def api_eldrazi(body: EldraziReq):
    gs = get_game()
    if gs.current_player_id != 0 or gs.phase == Phase.GAME_OVER:
        raise HTTPException(400, "Non è il tuo turno o partita finita")
    coords = [c.upper() for c in body.sacrifice_coords]
    ok = gs.summon_eldrazi(0, body.eldrazi_index, coords)
    if not ok:
        raise HTTPException(400, "Evocazione Mostrissimo fallita")
    return serialize_state(gs)


@app.post("/api/end")
def api_end():
    gs = get_game()
    if gs.phase == Phase.GAME_OVER:
        return serialize_state(gs)
    if gs.current_player_id != 0:
        raise HTTPException(400, "Non è il tuo turno")
    gs.end_turn()
    # Se ora è turno IA, falla giocare
    if gs.phase != Phase.GAME_OVER and gs.current_player_id == 1:
        ai = BasicAI(gs, player_id=1)
        ai.take_turn()
    return serialize_state(gs)


# Static files (CSS/JS se servono)
static_dir = ROOT / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
