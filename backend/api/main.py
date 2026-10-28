"""
FastAPI Penumbra – partite multiple, vs IA o base PvP (join by game_id).
4.2.6 – join autenticato: richiede JWT e salva player1_uid.
"""

from __future__ import annotations
import sys
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from core.game_state import GameState
from core.constants import Phase, pos_to_coord, coord_to_pos, GRID_SIZE, hex_to_pixel, HEX_RADIUS, all_hexes, hex_key
from ai.basic_ai import BasicAI
from api import supabase_store
from api.restore import hydrate
from api.auth import require_user, user_id

app = FastAPI(title="Penumbra Tactical Card Game", version="0.28")
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
    gs._draft_ai_if_needed()
    return gs


def _quest_progress(gs: GameState) -> dict:
    """Progresso Main Quest per la UI."""
    q = gs.main_quest
    if not q:
        return {"active": False, "label": "Nessuna Main Quest attiva", "detail": "Esplora tessere evento per rivelarne una."}
    if q == "MainQuest_Dominio":
        players = []
        for pid in (0, 1):
            buff = 0
            altar = False
            for u in gs.board.get_units_of_player(pid):
                tile = gs.board.get_tile(u.row, u.col)
                if not tile:
                    continue
                if tile.tile_type.value == "Buff":
                    buff += 1
                if tile.tile_type.value == "Altare":
                    altar = True
            players.append({"player_id": pid, "buffs": buff, "altar": altar, "done": buff >= 2 and altar})
        return {
            "active": True,
            "id": q,
            "label": "Dominio del Territorio",
            "detail": "Controlla 2 caselle Buff + l'Altare C3 all'inizio del tuo turno.",
            "players": players,
        }
    if q == "MainQuest_Superiorita":
        players = []
        for pid in (0, 1):
            n = len(gs.board.get_units_of_player(pid))
            opp = len(gs.board.get_units_of_player(1 - pid))
            players.append({"player_id": pid, "units": n, "opp": opp, "done": n >= opp + 3})
        return {
            "active": True,
            "id": q,
            "label": "Superiorità Numerica",
            "detail": "A inizio turno: almeno 3 creature in più dell'avversario.",
            "players": players,
        }
    return {"active": True, "id": q, "label": q, "detail": "", "players": []}


def serialize_state(gs: GameState, game_id: str, viewer_id: int = 0) -> dict:
    board = []
    for q, r in all_hexes(HEX_RADIUS):
        tile = gs.board.get_tile(q, r)
        unit = gs.board.get_unit_at(q, r)
        visible = True
        try:
            visible = gs.is_visible_to(viewer_id, r, q)
        except Exception:
            visible = True
        px, py = hex_to_pixel(q, r, size=28.0)
        cell = {
            "coord": gs.board.flavor_of(q, r),
            "qr": hex_key(q, r),
            "q": q,
            "r": r,
            "x": round(px, 1),
            "y": round(py, 1),
            "tile": tile.tile_type.value if tile else "Terreno",
            "flavor": getattr(tile, "flavor_name", "") if tile else "",
            "explored": True,
            "trap": False,
            "ritual": False,
            "altar": bool(tile and tile.tile_type.value == "Altare") if visible else False,
            "unit": None,
            "visible": visible,
            "fog": not visible,
            "artifact": bool(tile and getattr(tile, "has_artifact", False)) if visible else False,
        }
        if visible and unit:
            cell["unit"] = {
                "name": unit.card.name,
                "atk": unit.current_atk,
                "hp": unit.current_hp,
                "owner": unit.owner_id,
                "crown": unit.has_fragment,
                "evolved": "evolved" in unit.statuses,
                "coord": cell["coord"],
                "color": unit.card.color.value if unit.card.color else None,
                "signore": "signore" in unit.statuses,
                "withered": bool(unit.moved_this_turn),
                "ready": (not unit.moved_this_turn) and unit.is_alive,
            }
        if not visible and tile and not str(tile.tile_type.value).startswith("Tempio") and tile.tile_type.value != "Altare":
            cell["tile"] = "?"
            cell["flavor"] = "?"
        board.append(cell)

    eldrazi = [
        {"index": i, "name": e.name, "atk": e.atk, "hp": e.hp, "sacrifice": e.sacrifice_cost}
        for i, e in enumerate(gs.eldrazi_pool)
    ]
    mode = _modes.get(game_id, {"p1_ai": True})
    popups = list(getattr(gs, "pending_popups", []) or [])
    if hasattr(gs, "pending_popups"):
        gs.pending_popups.clear()
    return {
        "game_id": game_id,
        "turn": gs.turn,
        "phase": gs.phase.name,
        "current_player": gs.current_player_id,
        "winner": gs.winner,
        "main_quest": gs.main_quest,
        "quest_progress": _quest_progress(gs),
        "board": board,
        "players": [player_data(p) for p in gs.players],
        "eldrazi": eldrazi,
        "log": gs.log[-15:],
        "supabase": supabase_store.enabled(),
        "p1_is_ai": mode.get("p1_ai", True),
        "draft": gs.get_draft_state() if gs.phase == Phase.DRAFT else None,
        "player0_uid": mode.get("player0_uid"),
        "player1_uid": mode.get("player1_uid"),
        "edge_walls": gs.board.get_edge_walls_for_ui() if hasattr(gs.board, "get_edge_walls_for_ui") else [],
        "grid_size": GRID_SIZE,
        "map_type": "hex",
        "hex_radius": HEX_RADIUS,
        "pending_popups": popups,
    }



def _persist(game_id: str, gs: GameState, action: str = "update", payload: Optional[dict] = None):
    if not supabase_store.enabled():
        return
    snap = serialize_state(gs, game_id)
    mode = _modes.get(game_id, {})
    supabase_store.update_game(
        game_id,
        snap,
        player0_uid=mode.get("player0_uid"),
        player1_uid=mode.get("player1_uid"),
        p1_is_ai=mode.get("p1_ai"),
    )
    if action != "update":
        supabase_store.log_move(game_id, snap.get("current_player", 0), action, payload or {})


def _load_from_supabase(game_id: str) -> Optional[GameState]:
    row = supabase_store.fetch_game(game_id)
    if not row:
        return None
    snap = row.get("state_json") or {}
    if isinstance(snap, str):
        import json
        try:
            snap = json.loads(snap)
        except Exception:
            return None
    gs = hydrate(snap)
    if not gs:
        return None
    _games[game_id] = gs
    p1_ai = True
    if "p1_is_ai" in row:
        p1_ai = bool(row["p1_is_ai"])
    elif snap.get("players") and len(snap["players"]) > 1:
        p1_ai = bool(snap["players"][1].get("is_ai", True))
    elif "p1_is_ai" in snap:
        p1_ai = bool(snap["p1_is_ai"])
    _modes[game_id] = {
        "p1_ai": p1_ai,
        "p1_joined": not p1_ai or bool(row.get("player1_uid")),
        "player0_uid": row.get("player0_uid"),
        "player1_uid": row.get("player1_uid"),
    }
    gs.log_msg("[sistema] Partita ripristinata da Supabase")
    return gs


def _require_game(game_id: str) -> GameState:
    if game_id in _games:
        return _games[game_id]
    gs = _load_from_supabase(game_id)
    if gs:
        return gs
    raise HTTPException(404, "Partita non trovata (né in memoria né su Supabase).")


def _require_membership(game_id: str, uid: Optional[str]) -> None:
    """
    Scelta A: se non sei player0 o player1 → 403.
    Partite senza uid (legacy) → 403.
    """
    if not uid:
        raise HTTPException(401, "Utente non autenticato")
    mode = _modes.get(game_id, {})
    p0 = mode.get("player0_uid")
    p1 = mode.get("player1_uid")
    if p0 is None and p1 is None:
        # Partita legacy / senza ownership → non giocabile (scelta A)
        raise HTTPException(403, "Partita senza proprietario registrato (accesso negato)")
    if uid != p0 and uid != p1:
        raise HTTPException(403, "Non sei un giocatore di questa partita")


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


class FragmentReq(BaseModel):
    game_id: str
    coord: str
    player_id: int = 0


class DraftReq(BaseModel):
    game_id: str
    pack_index: Optional[int] = None
    card_index: Optional[int] = None  # alias legacy = pack_index
    player_id: int = 0


@app.get("/")
def index():
    static = ROOT / "static" / "index.html"
    if static.exists():
        return FileResponse(static)
    return JSONResponse({"error": "static/index.html mancante"}, status_code=404)


@app.get("/api/health")
def health():
    return {"ok": True, "version": "0.28", "games_in_memory": len(_games), "supabase": supabase_store.enabled()}


@app.post("/api/new")
async def api_new(body: NewReq = NewReq(), user: Dict[str, Any] = Depends(require_user)):
    """Crea una nuova partita. Richiede JWT. Il creatore diventa player0_uid."""
    uid = user_id(user)
    if not uid:
        raise HTTPException(401, "Utente non autenticato")

    game_id = str(uuid.uuid4())
    p1_ai = body.vs_ai
    gs = _new_engine(
        p0_name=body.name or "Giocatore 1",
        p1_name="AI Overlord" if p1_ai else "In attesa…",
        p1_is_ai=p1_ai,
    )
    _games[game_id] = gs
    _modes[game_id] = {
        "p1_ai": p1_ai,
        "p1_joined": p1_ai,
        "player0_uid": uid,
        "player1_uid": None,
    }
    if supabase_store.enabled():
        supabase_store.create_game(
            serialize_state(gs, game_id),
            game_id=game_id,
            player0_uid=uid,
            player1_uid=None,
            p1_is_ai=p1_ai,
        )
    return serialize_state(gs, game_id, viewer_id=0)


@app.post("/api/join")
async def api_join(body: JoinReq, user: Dict[str, Any] = Depends(require_user)):
    """
    Unisciti a una partita PvP.
    Richiede JWT. Diventi player1_uid.
    """
    uid = user_id(user)
    if not uid:
        raise HTTPException(401, "Utente non autenticato")

    gs = _require_game(body.game_id)
    mode = _modes.get(body.game_id, {})

    if mode.get("p1_ai"):
        raise HTTPException(400, "Questa partita è vs IA, non si può joinare.")
    if mode.get("p1_joined") or mode.get("player1_uid"):
        raise HTTPException(400, "Il posto P1 è già occupato.")
    if mode.get("player0_uid") == uid:
        raise HTTPException(400, "Non puoi unirti alla partita che hai creato tu.")

    gs.players[1].name = body.name or "Giocatore 2"
    gs.players[1].is_ai = False
    mode["p1_joined"] = True
    mode["p1_ai"] = False
    mode["player1_uid"] = uid
    _modes[body.game_id] = mode
    gs.log_msg(f"{gs.players[1].name} si è unito alla partita.")

    # Salva ownership su Supabase
    if supabase_store.enabled():
        supabase_store.set_ownership(
            body.game_id,
            player1_uid=uid,
            p1_is_ai=False,
        )
    _persist(body.game_id, gs, "join", {"name": body.name, "player1_uid": uid})
    return serialize_state(gs, body.game_id, viewer_id=getattr(body, 'player_id', 0))


@app.get("/api/state")
async def api_state(
    game_id: Optional[str] = Query(None),
    user: Dict[str, Any] = Depends(require_user),
):
    """Stato partita: richiede JWT + membership."""
    if not game_id:
        raise HTTPException(
            400,
            "Fornire game_id oppure creare una partita con POST /api/new",
        )
    uid = user_id(user)
    gs = _require_game(game_id)
    _require_membership(game_id, uid)
    # viewer = player0 se uid match, altrimenti player1
    mode = _modes.get(game_id, {})
    viewer = 0 if mode.get("player0_uid") == uid else (1 if mode.get("player1_uid") == uid else 0)
    return serialize_state(gs, game_id, viewer_id=viewer)


@app.post("/api/move")
async def api_move(body: MoveReq, user: Dict[str, Any] = Depends(require_user)):
    uid = user_id(user)
    gs = _require_game(body.game_id)
    _require_membership(body.game_id, uid)
    if gs.phase == Phase.GAME_OVER:
        raise HTTPException(400, "Partita finita")
    if gs.current_player_id != body.player_id:
        raise HTTPException(400, "Non è il tuo turno")
    from_pos = gs.resolve_coord(body.from_coord)
    to_pos = gs.resolve_coord(body.to_coord)
    if not from_pos or not to_pos:
        raise HTTPException(400, "Coordinate non valide")
    fq, fr = from_pos  # q, r
    tq, tr = to_pos
    unit = gs.board.get_unit_at(fq, fr)
    if not unit or unit.owner_id != body.player_id:
        raise HTTPException(400, "Nessuna tua unità su quella casella")
    ok = gs.try_move(unit, tr, tq)  # try_move(unit, target_row=r, target_col=q)
    if not ok:
        raise HTTPException(400, "Mossa non valida")
    _persist(body.game_id, gs, "move", {"from": body.from_coord, "to": body.to_coord})
    return serialize_state(gs, body.game_id, viewer_id=getattr(body, 'player_id', 0))


@app.post("/api/play")
async def api_play(body: PlayReq, user: Dict[str, Any] = Depends(require_user)):
    uid = user_id(user)
    gs = _require_game(body.game_id)
    _require_membership(body.game_id, uid)
    if gs.phase == Phase.GAME_OVER:
        raise HTTPException(400, "Partita finita")
    if gs.current_player_id != body.player_id:
        raise HTTPException(400, "Non è il tuo turno")
    target = body.target_coord.upper() if body.target_coord else None
    ok = gs.play_card(body.player_id, body.hand_index, target)
    if not ok:
        raise HTTPException(400, "Carta non giocabile")
    _persist(body.game_id, gs, "play", {"hand_index": body.hand_index})
    return serialize_state(gs, body.game_id, viewer_id=getattr(body, 'player_id', 0))


@app.post("/api/eldrazi")
async def api_eldrazi(body: EldraziReq, user: Dict[str, Any] = Depends(require_user)):
    uid = user_id(user)
    gs = _require_game(body.game_id)
    _require_membership(body.game_id, uid)
    if gs.current_player_id != body.player_id:
        raise HTTPException(400, "Non è il tuo turno")
    coords = [c.upper() for c in body.sacrifice_coords]
    ok = gs.summon_eldrazi(body.player_id, body.eldrazi_index, coords)
    if not ok:
        raise HTTPException(400, "Evocazione Mostrissimo fallita")
    _persist(body.game_id, gs, "eldrazi", {"index": body.eldrazi_index})
    return serialize_state(gs, body.game_id, viewer_id=getattr(body, 'player_id', 0))


@app.post("/api/end")
async def api_end(body: EndReq, user: Dict[str, Any] = Depends(require_user)):
    uid = user_id(user)
    gs = _require_game(body.game_id)
    _require_membership(body.game_id, uid)
    if gs.phase == Phase.GAME_OVER:
        return serialize_state(gs, body.game_id, viewer_id=getattr(body, 'player_id', 0))
    if gs.current_player_id != body.player_id:
        raise HTTPException(400, "Non è il tuo turno")
    try:
        gs.end_turn()
        if gs.phase != Phase.GAME_OVER and gs.players[gs.current_player_id].is_ai:
            ai = BasicAI(gs, player_id=gs.current_player_id)
            ai.take_turn()
        _persist(body.game_id, gs, "end_turn")
        return serialize_state(gs, body.game_id, viewer_id=getattr(body, 'player_id', 0))
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Errore fine turno: {type(e).__name__}: {e}")


@app.post("/api/fragment")
async def api_fragment(body: FragmentReq, user: Dict[str, Any] = Depends(require_user)):
    """Piazza (o sposta) il Frammento/Corona su una tua creatura."""
    uid = user_id(user)
    gs = _require_game(body.game_id)
    _require_membership(body.game_id, uid)
    if gs.phase == Phase.GAME_OVER:
        raise HTTPException(400, "Partita finita")
    if gs.current_player_id != body.player_id:
        raise HTTPException(400, "Non è il tuo turno")
    p = gs.players[body.player_id]
    cost = p.next_fragment_cost()
    if cost is None:
        raise HTTPException(400, "Nessun Frammento rimanente")
    if not p.can_afford(cost):
        raise HTTPException(400, f"Mana insufficiente (serve {cost})")
    try:
        r, c = coord_to_pos(body.coord.upper())
    except Exception:
        raise HTTPException(400, "Coordinata non valida")
    unit = gs.board.get_unit_at(r, c)
    if not unit or unit.owner_id != body.player_id:
        raise HTTPException(400, "Nessuna tua creatura su quella casella")
    if not unit.is_alive:
        raise HTTPException(400, "Unità non valida")
    ok = p.place_fragment(unit)
    if not ok:
        raise HTTPException(400, "Impossibile piazzare il Frammento")
    gs.log_msg(f"{p.name} piazza la Corona su {unit.card.name} ({unit.coord}) pagando {cost} mana")
    _persist(body.game_id, gs, "fragment", {"coord": body.coord, "cost": cost})
    return serialize_state(gs, body.game_id, viewer_id=getattr(body, 'player_id', 0))


@app.post("/api/draft")
async def api_draft(body: DraftReq, user: Dict[str, Any] = Depends(require_user)):
    uid = user_id(user)
    gs = _require_game(body.game_id)
    _require_membership(body.game_id, uid)
    if gs.phase != Phase.DRAFT:
        raise HTTPException(400, "Non sei in fase draft")
    idx = body.pack_index if body.pack_index is not None else body.card_index
    if idx is None:
        raise HTTPException(400, "Serve pack_index")
    ok = gs.draft_pick(body.player_id, idx)
    if not ok:
        raise HTTPException(400, "Scelta busta non valida")
    _persist(body.game_id, gs, "draft", {"pack_index": idx})
    return serialize_state(gs, body.game_id, viewer_id=getattr(body, 'player_id', 0))


static_dir = ROOT / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
