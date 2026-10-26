"""
FastAPI Penumbra v7 – partite multiple, vs IA o base PvP (join by game_id).
"""

from __future__ import annotations
import sys
import uuid
from pathlib import Path
from typing import Optional, List, Dict

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from core.game_state import GameState
from core.constants import Phase, pos_to_coord, coord_to_pos
from ai.basic_ai import BasicAI
from api import supabase_store

app = FastAPI(title="Penumbra Tactical Card Game", version="0.7")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_games: Dict[str, GameState] = {}
_modes: Dict[str, dict] = {}


def _new_engine(p0_name: str = "Giocatore 1", p1_name: str = "AI Overlord", p1_is_ai: bool = True) -> GameState:
    gs = GameState(human_name=p0_name, ai_name=p1_name)
    gs.players[1].is_ai = p1_is_ai
    if not p1_is_ai:
        gs.players[1].name = p1_name
    gs.start_draft()
    while gs.phase == Phase.DRAFT:
        pack = gs.get_current_pack()
        if not pack:
            break
        for pid in (0, 1):
            if gs.phase != Phase.DRAFT:
                break
            pack = gs.get_current_pack()
            if not pack:
                break
            gs.draft_pick(pid, 0)
    gs.start_turn()
    units = gs.board.get_units_of_player(0)
    if units:
        gs.players[0].place_fragment(units[0])
    return gs


def serialize_state(gs: GameState, game_id: str) -> dict:
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
                    "text": (c.text or "")[:80],
                }
                for i, c in enumerate(p.hand)
            ],
            "crown": p.crown_unit.coord if p.crown_unit and p.crown_unit.is_alive else None,
            "is_ai": p.is_ai,
            "lost": p.has_lost,
        }

    eldrazi = [
        {"index": i, "name": e.name, "atk": e.atk, "hp": e.hp, "sacrifice": e.sacrifice_cost}
        for i, e in enumerate(gs.eldrazi_pool)
    ]
    mode = _modes.get(game_id, {"p1_ai": True})
    return {
        "game_id": game_id,
        "turn": gs.turn,
        "phase": gs.phase.name,
        "current_player": gs.current_player_id,
        "winner": gs.winner,
        "main_quest": gs.main_quest,
        "board": board,
        "players": [player_data(p) for p in gs.players],
        "eldrazi": eldrazi,
        "log": gs.log[-15:],
        "supabase": supabase_store.enabled(),
        "p1_is_ai": mode.get("p1_ai", True),
    }


def _persist(game_id: str, gs: GameState, action: str = "update", payload: Optional[dict] = None):
    if not supabase_store.enabled():
        return
    snap = serialize_state(gs, game_id)
    supabase_store.update_game(game_id, snap)
    if action != "update":
        supabase_store.log_move(game_id, snap.get("current_player", 0), action, payload or {})


def _require_game(game_id: str) -> GameState:
    if game_id not in _games:
        raise HTTPException(404, "Partita non trovata. Crea una nuova partita.")
    return _games[game_id]


class MoveReq(BaseModel):
    game_id: str
    from_coord: str
    to_coord: str
    player_id: int = 0


class PlayReq(BaseModel):
    game_id: str
    hand_index: int
    target_coord: Optional[str] = None
    player_id: int = 0


class EldraziReq(BaseModel):
    game_id: str
    eldrazi_index: int
    sacrifice_coords: List[str]
    player_id: int = 0


class EndReq(BaseModel):
    game_id: str
    player_id: int = 0


class NewReq(BaseModel):
    vs_ai: bool = True
    name: str = "Giocatore 1"


class JoinReq(BaseModel):
    game_id: str
    name: str = "Giocatore 2"


@app.get("/")
def index():
    static = ROOT / "static" / "index.html"
    if static.exists():
        return FileResponse(static)
    return JSONResponse({"error": "static/index.html mancante"}, status_code=404)


@app.get("/api/health")
def health():
    return {"ok": True, "version": "0.7", "games_in_memory": len(_games), "supabase": supabase_store.enabled()}


@app.post("/api/new")
def api_new(body: NewReq = NewReq()):
    game_id = str(uuid.uuid4())
    p1_ai = body.vs_ai
    gs = _new_engine(
        p0_name=body.name or "Giocatore 1",
        p1_name="AI Overlord" if p1_ai else "In attesa…",
        p1_is_ai=p1_ai,
    )
    _games[game_id] = gs
    _modes[game_id] = {"p1_ai": p1_ai, "p1_joined": p1_ai}
    if supabase_store.enabled():
        supabase_store.create_game(serialize_state(gs, game_id))
    return serialize_state(gs, game_id)


@app.post("/api/join")
def api_join(body: JoinReq):
    gs = _require_game(body.game_id)
    mode = _modes.get(body.game_id, {})
    if mode.get("p1_ai"):
        raise HTTPException(400, "Questa partita è vs IA, non si può joinare.")
    if mode.get("p1_joined"):
        raise HTTPException(400, "Il posto P1 è già occupato.")
    gs.players[1].name = body.name or "Giocatore 2"
    gs.players[1].is_ai = False
    mode["p1_joined"] = True
    mode["p1_ai"] = False
    _modes[body.game_id] = mode
    gs.log_msg(f"{gs.players[1].name} si è unito alla partita.")
    _persist(body.game_id, gs, "join", {"name": body.name})
    return serialize_state(gs, body.game_id)


@app.get("/api/state")
def api_state(game_id: Optional[str] = Query(None)):
    if not game_id or game_id not in _games:
        return api_new(NewReq(vs_ai=True))
    return serialize_state(_games[game_id], game_id)


@app.post("/api/move")
def api_move(body: MoveReq):
    gs = _require_game(body.game_id)
    if gs.phase == Phase.GAME_OVER:
        raise HTTPException(400, "Partita finita")
    if gs.current_player_id != body.player_id:
        raise HTTPException(400, "Non è il tuo turno")
    try:
        fr, fc = coord_to_pos(body.from_coord.upper())
        tr, tc = coord_to_pos(body.to_coord.upper())
    except Exception:
        raise HTTPException(400, "Coordinate non valide")
    unit = gs.board.get_unit_at(fr, fc)
    if not unit or unit.owner_id != body.player_id:
        raise HTTPException(400, "Nessuna tua unità su quella casella")
    ok = gs.try_move(unit, tr, tc)
    if not ok:
        raise HTTPException(400, "Mossa non valida")
    _persist(body.game_id, gs, "move", {"from": body.from_coord, "to": body.to_coord})
    return serialize_state(gs, body.game_id)


@app.post("/api/play")
def api_play(body: PlayReq):
    gs = _require_game(body.game_id)
    if gs.phase == Phase.GAME_OVER:
        raise HTTPException(400, "Partita finita")
    if gs.current_player_id != body.player_id:
        raise HTTPException(400, "Non è il tuo turno")
    target = body.target_coord.upper() if body.target_coord else None
    ok = gs.play_card(body.player_id, body.hand_index, target)
    if not ok:
        raise HTTPException(400, "Carta non giocabile")
    _persist(body.game_id, gs, "play", {"hand_index": body.hand_index})
    return serialize_state(gs, body.game_id)


@app.post("/api/eldrazi")
def api_eldrazi(body: EldraziReq):
    gs = _require_game(body.game_id)
    if gs.current_player_id != body.player_id:
        raise HTTPException(400, "Non è il tuo turno")
    coords = [c.upper() for c in body.sacrifice_coords]
    ok = gs.summon_eldrazi(body.player_id, body.eldrazi_index, coords)
    if not ok:
        raise HTTPException(400, "Evocazione Mostrissimo fallita")
    _persist(body.game_id, gs, "eldrazi", {"index": body.eldrazi_index})
    return serialize_state(gs, body.game_id)


@app.post("/api/end")
def api_end(body: EndReq):
    gs = _require_game(body.game_id)
    if gs.phase == Phase.GAME_OVER:
        return serialize_state(gs, body.game_id)
    if gs.current_player_id != body.player_id:
        raise HTTPException(400, "Non è il tuo turno")
    gs.end_turn()
    if gs.phase != Phase.GAME_OVER and gs.players[gs.current_player_id].is_ai:
        ai = BasicAI(gs, player_id=gs.current_player_id)
        ai.take_turn()
    _persist(body.game_id, gs, "end_turn")
    return serialize_state(gs, body.game_id)


static_dir = ROOT / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
