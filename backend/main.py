#!/usr/bin/env python3
"""
Tactical Card Game 5x5 - Prototipo Console
"""

from core.game_state import GameState
from core.constants import Phase
import random


def main():
    print("=" * 60)
    print("  TACTICAL CARD GAME 5x5 - Prototipo")
    print("  Ispirato a Mage Wars + Scacchi + MOBA + 7th Continent")
    print("=" * 60)

    gs = GameState(human_name="Tu", ai_name="AI Overlord")

    # --- DRAFT semplificato automatico per test rapido ---
    gs.start_draft()
    # Auto-pick per entrambi i giocatori (snake)
    while gs.phase == Phase.DRAFT:
        pack = gs.get_current_pack()
        if not pack:
            break
        # P1 sceglie random, P2 sceglie random (in futuro interattivo)
        for pid in (0, 1):
            if gs.phase != Phase.DRAFT:
                break
            pack = gs.get_current_pack()
            if not pack:
                break
            idx = random.randint(0, len(pack) - 1)
            gs.draft_pick(pid, idx)

    # Assegna frammento iniziale gratis (costo 0) a un 1/1 di spawn
    gs.phase = Phase.SETUP
    gs.start_turn()  # turn 1 - umano

    # Dai il primo frammento gratis al primo soldato
    p0 = gs.players[0]
    units = gs.board.get_units_of_player(0)
    if units:
        p0.place_fragment(units[0])
        gs.log_msg(f"Frammento 1 (costo 0) assegnato a {units[0]}")

    gs.print_state()

    print("\nComandi disponibili (prototipo):")
    print("  m <from> <to>              - muovi unità (es. m B5 C4)")
    print("  p <idx> [coord]            - gioca carta dalla mano (es. p 0  oppure  p 2 B5)")
    print("  x <idx> <c1> <c2> ...      - evoca Mostrissimo (sacrifici, uno su Cerchio Rituale)")
    print("  s                          - stato")
    print("  e                          - fine turno")
    print("  q                          - esci")
    print()

    while gs.phase != Phase.GAME_OVER:
        p = gs.players[gs.current_player_id]
        if p.is_ai:
            # IA molto stupida per ora: passa sempre
            print(f"[IA] {p.name} passa il turno.")
            gs.end_turn()
            gs.print_state()
            continue

        try:
            cmd = input(f"[{p.name} Mana {p.mana}/{p.mana_max}] > ").strip().lower()
        except EOFError:
            break

        if not cmd:
            continue
        if cmd == "q":
            break
        if cmd == "s":
            gs.print_state()
            continue
        if cmd == "e":
            gs.end_turn()
            gs.print_state()
            continue
        if cmd.startswith("m "):
            parts = cmd.split()
            if len(parts) != 3:
                print("Uso: m <from> <to>  es. m B5 C4")
                continue
            from_c, to_c = parts[1].upper(), parts[2].upper()
            try:
                fr, fc = __import__("core.constants", fromlist=["coord_to_pos"]).coord_to_pos(from_c)
                tr, tc = __import__("core.constants", fromlist=["coord_to_pos"]).coord_to_pos(to_c)
            except Exception:
                print("Coordinate non valide")
                continue
            unit = gs.board.get_unit_at(fr, fc)
            if not unit or unit.owner_id != 0:
                print("Nessuna tua unità su quella casella")
                continue
            ok = gs.try_move(unit, tr, tc)
            if ok:
                gs.print_state()
            continue

        if cmd.startswith("p "):
            parts = cmd.split()
            if len(parts) < 2:
                print("Uso: p <indice_mano> [coord]  es. p 0   oppure  p 2 B5")
                continue
            try:
                idx = int(parts[1])
            except ValueError:
                print("Indice non valido")
                continue
            target = parts[2].upper() if len(parts) >= 3 else None
            ok = gs.play_card(0, idx, target)
            if ok:
                gs.print_state()
            continue

        if cmd.startswith("x "):
            parts = cmd.split()
            if len(parts) < 3:
                print("Uso: x <indice_mostrissimo> <coord_sacrificio1> <coord2> ...")
                print("Esempio: x 0 A1 B5 C3   (uno dei sacrifici deve essere su Cerchio Rituale)")
                continue
            try:
                idx = int(parts[1])
            except ValueError:
                print("Indice non valido")
                continue
            coords = [c.upper() for c in parts[2:]]
            ok = gs.summon_eldrazi(0, idx, coords)
            if ok:
                gs.print_state()
            continue

        print("Comando non riconosciuto")

    if gs.winner is not None:
        print(f"\n*** VINCITORE: {gs.players[gs.winner].name} ***")
    print("Grazie per aver giocato il prototipo!")


if __name__ == "__main__":
    main()
