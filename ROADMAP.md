# Roadmap Penumbra

## Fase 5 — Partita base

| Step | Stato |
|------|--------|
| 5.1 Movimento re | fatto |
| 5.2 Home | fatto |
| 5.3 Giallo | fatto |
| 5.4 Regole | in corso (v25+v27) |
| Draft buste | fatto (v26) |
| Corona come carta + no PvP in UI | fatto (v27) |
| **Mappa 7×7 + muri edge + templi angolo** | **fatto (v28)** |
| Hotfix tempio hardcode + messaggio errore /api/end | **fatto (v28.1)** |
| Rimuovere neutrali + Fog of war raggio 2 | **fatto (v28.3)** |

## Fase A — Stabilizzazione errori

| Step | Stato |
|------|--------|
| A.1 Correggere 400 su /api/draft e /api/move | in verifica |
| A.2 Correggere 500 su /api/end | hotfix v28.1 (messaggio chiaro + tempio) |
| A.3 Auth obbligatorio (già attivo) | fatto |
| A.4 Smoke test dopo partita utente | in attesa |

## Fase B — Nuova mappa (v28) ✅

| Step | Stato |
|------|--------|
| B.1 Griglia 7×7 | fatto |
| B.2 Zona giocabile interna 5×5 | fatto |
| B.3 Cornice FRAME non giocabile | fatto |
| B.4 Templi angoli (P1 basso-sx, P2 alto-dx) | fatto |
| B.5 Spawn solo sul Tempio | fatto |
| B.6 Altare al centro zona MAPPA (3,3) | fatto |
| B.7 Muri edge da xlsx | fatto |
| B.8 Coordinate A–G / 0–6 | fatto |
| B.9 UI 7×7 | fatto |

## Prossimo
- Utente ridistribuisce v28.1 e rifà una partita.
- Se c’è ancora errore, il messaggio ora dice esattamente quale eccezione è.
