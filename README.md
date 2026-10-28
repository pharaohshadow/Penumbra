# Penumbra – Consegna v41

## Fix movimento
- `try_move` usava **q/r invertite** su `get_unit_at`, `get_tile`, `move_unit` → 400/500 su `/api/move`.
- Ora tutto in convenzione hex: **col=q, row=r**.
- Messaggi di errore più chiari da `/api/move`.

Mappa utente e muri su bordo (v39–v40) restano.

**Nessuna modifica manuale.** Cartella: `penumbra_v41/`
