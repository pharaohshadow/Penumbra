# Penumbra – Consegna v42

## Fix fine draft → 500 / "partita finita"
1. **`TileType.SANCTUARY`** (e altri tipi legacy) non esistono sulla mappa hex → crash in `start_turn` a fine draft.
2. Lookup tile con **q/r invertite** in alcuni punti.
3. **Supabase 400** su `update_game` non deve più far fallire la richiesta (persist “soft”).
4. `/api/draft` con errori più chiari.

Dopo il draft la partita entra in **MAIN** turno 1 con spawn sul Tempio1.

**Nessuna modifica manuale.** Cartella: `penumbra_v42/`
