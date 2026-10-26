"""Ricostruisce GameState da state_json serializzato (API snapshot)."""

from __future__ import annotations
from typing import Any, Dict, Optional

from core.game_state import GameState
from core.unit import Unit
from core.card import Card, get_card_db
from core.constants import Phase, CardType, Color, coord_to_pos, TileType


def hydrate(snapshot: Dict[str, Any]) -> Optional[GameState]:
    if not snapshot or "board" not in snapshot:
        return None
    db = get_card_db()
    gs = GameState(human_name="Giocatore 1", ai_name="Giocatore 2")
    # Pulisci spawn automatici del costruttore-path: ricreiamo da zero
    gs.board.units.clear()
    for p in gs.players:
        p.hand.clear()
        p.crown_unit = None
        p.fragments_remaining = 3
        p.has_lost = False

    gs.turn = int(snapshot.get("turn") or 1)
    phase_name = snapshot.get("phase") or "MAIN"
    try:
        gs.phase = Phase[phase_name] if phase_name in Phase.__members__ else Phase.MAIN
    except Exception:
        gs.phase = Phase.MAIN
    gs.current_player_id = int(snapshot.get("current_player") or 0)
    gs.winner = snapshot.get("winner")
    gs.main_quest = snapshot.get("main_quest")
    gs.log = list(snapshot.get("log") or [])

    # Players
    for pdata in snapshot.get("players") or []:
        pid = int(pdata.get("id", 0))
        if pid not in (0, 1):
            continue
        p = gs.players[pid]
        p.name = pdata.get("name") or p.name
        p.mana = int(pdata.get("mana") or 0)
        p.mana_max = int(pdata.get("mana_max") or 1)
        p.fragments_remaining = int(pdata.get("fragments") if pdata.get("fragments") is not None else 3)
        p.is_ai = bool(pdata.get("is_ai"))
        p.has_lost = bool(pdata.get("lost"))
        hand = []
        for h in pdata.get("hand") or []:
            cid = h.get("id")
            card = db.get(cid) if cid is not None else None
            if card is None:
                # carta sintetica
                try:
                    ctype = CardType(h.get("type") or "Mostro")
                except Exception:
                    ctype = CardType.MONSTER
                card = Card(
                    id=cid or 0,
                    name=h.get("name") or "?",
                    cost=int(h.get("cost") or 0),
                    card_type=ctype,
                    color=Color.GRAY,
                    atk=int(h.get("atk") or 0),
                    hp=int(h.get("hp") or 0),
                    text=h.get("text") or "",
                )
            hand.append(card)
        p.hand = hand

    # --- Tile ricchi (step 3.3 / v20) ---
    # Il costruttore di Board applica il layout fisso. Qui sovrascriviamo
    # solo i campi che possono cambiare durante la partita (explored,
    # tile_type dopo eventi, permanent_effect, trap, wall_hp, owner_id).
    # Snapshot vecchi senza i nuovi campi restano compatibili.
    _value_to_tiletype = {t.value: t for t in TileType}
    for row in snapshot.get("board") or []:
        for cell in row:
            coord = cell.get("coord")
            if not coord:
                continue
            try:
                r, c = coord_to_pos(coord)
            except Exception:
                continue
            tile = gs.board.get_tile(r, c)
            if not tile:
                continue
            # tipo tile (se presente e valido)
            tname = cell.get("tile")
            if tname and tname in _value_to_tiletype:
                tile.tile_type = _value_to_tiletype[tname]
            if "explored" in cell:
                tile.explored = bool(cell.get("explored"))
            # campi ricchi (opzionali: assenti su snapshot pre-v20)
            if "permanent_effect" in cell:
                tile.permanent_effect = cell.get("permanent_effect")
            if "trap_card_id" in cell:
                tile.trap_card_id = cell.get("trap_card_id")
            if "wall_hp" in cell and cell.get("wall_hp") is not None:
                try:
                    tile.wall_hp = int(cell.get("wall_hp") or 0)
                except (TypeError, ValueError):
                    tile.wall_hp = 0
            if "owner_id" in cell:
                tile.owner_id = cell.get("owner_id")

    # Units on board
    for row in snapshot.get("board") or []:
        for cell in row:
            u = cell.get("unit")
            if not u:
                continue
            coord = u.get("coord") or cell.get("coord")
            try:
                r, c = coord_to_pos(coord)
            except Exception:
                continue
            owner = int(u.get("owner", -1))
            name = u.get("name") or "?"
            atk = int(u.get("atk") or 0)
            hp = int(u.get("hp") or 1)
            # trova carta per nome
            card = None
            for cobj in db.cards.values():
                if cobj.name == name:
                    card = cobj
                    break
            if card is None:
                card = Card(
                    id=90000 + r * 10 + c,
                    name=name,
                    cost=0,
                    card_type=CardType.NEUTRAL if owner < 0 else CardType.MONSTER,
                    color=Color.GRAY,
                    atk=atk,
                    hp=hp,
                )
            unit = Unit(card, owner, r, c, hp, atk)
            unit.has_fragment = bool(u.get("crown"))
            gs.board.place_unit(unit)
            if unit.has_fragment and owner in (0, 1):
                gs.players[owner].crown_unit = unit

    # Eldrazi pool (best effort by name)
    pool = []
    for e in snapshot.get("eldrazi") or []:
        name = e.get("name")
        found = None
        for cobj in db.eldrazi:
            if cobj.name == name:
                found = cobj
                break
        if found:
            pool.append(found)
    if pool:
        gs.eldrazi_pool = pool

    # p1 ai flag handled by caller via _modes
    return gs
