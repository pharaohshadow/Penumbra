# Penumbra – Consegna v12 (step 4.2.1)

Contratto auth API. **Scelta A** (no legacy open).  
**Sito in costruzione:** nessun giocatore reale da preservare.

## Contenuto

| File | Ruolo |
|------|--------|
| `README.md` | Handoff |
| `backend/api/AUTH_CONTRACT_4_2_1.md` | Tabella endpoint 401/403 |
| `ROADMAP.md` | 4.2.1 fatto |
| `architettura.md` | |
| `istruzioni_per_IA.md` | **Preferenze permanenti** (A + in costruzione) |

## Decisioni bloccate

1. Legacy uid null → **sempre 403** (scelta A)  
2. Progetto **in costruzione** → non serve compatibilità partite/utenti reali  
3. `GET /api/health` e static restano pubblici; tutto il resto gioco richiede JWT  

## Prossimo

**4.2.2** – modulo verifica JWT Supabase (`require_user`).

## Repo

https://github.com/pharaohshadow/Penumbra
