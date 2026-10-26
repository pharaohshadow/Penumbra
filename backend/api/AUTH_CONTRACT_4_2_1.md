# 4.2.1 – Contratto auth endpoint (API protetta)

**Contesto progetto (non dimenticare):**  
il sito è **in costruzione**. Non ci sono partite in corso né utenti reali che giocano.  
Quindi: **niente compatibilità legacy** da preservare in produzione.

**Policy ownership (scelta A, confermata):**  
se una partita non ha membership valida per l’uid del JWT → **403**.  
Partite con `player0_uid` / `player1_uid` entrambi null → **403** (non si “aprono” al possessore del solo `game_id`).

---

## Header

```http
Authorization: Bearer <supabase_access_token>
```

- Assente / malformato → **401**
- JWT valido ma uid non membro del `game_id` → **403**
- Membership: `uid == player0_uid` **oppure** `uid == player1_uid`  
  (partita base vs IA: solo `player0_uid` valorizzato)

---

## Tabella endpoint

| Endpoint | Metodo | Auth | Membership | Note |
|----------|--------|------|------------|------|
| `/` | GET | No | — | Serve static `index.html` |
| `/static/*` | GET | No | — | Asset |
| `/api/health` | GET | No | — | Monitor / cron keep-alive |
| `/api/new` | POST | **JWT** | — (diventi P0) | Setta `player0_uid=sub`, `vs_ai` da body |
| `/api/join` | POST | **JWT** | slot P1 libero | 400 se `vs_ai`; setta `player1_uid` |
| `/api/state` | GET | **JWT** | **Sì** | Niente auto-new anonimo se manca game_id senza auth |
| `/api/move` | POST | **JWT** | **Sì** | + turno / regole gioco |
| `/api/play` | POST | **JWT** | **Sì** | |
| `/api/eldrazi` | POST | **JWT** | **Sì** | |
| `/api/end` | POST | **JWT** | **Sì** | |
| `/api/fragment` | POST | **JWT** | **Sì** | |
| `/api/draft` | POST | **JWT** | **Sì** | |

### Comportamento speciale `/api/state`

Oggi senza `game_id` crea una partita nuova.  
Con auth (4.2):

- senza JWT → **401** (niente partita anonima)
- con JWT e senza `game_id` → equivalente a create “mia” partita base **oppure** 400 “game_id richiesto”  
  **Proposta implementazione 4.2.5:** senza `game_id` → 400; create solo via `POST /api/new` (più chiaro).

### Legacy

- **Nessun** flag `ALLOW_LEGACY_OPEN`
- Partite vecchie in DB con uid null: non giocabili via API finché non si assegnano uid a mano o si ricreano

---

## Codici errore (contratto)

| Codice | Quando |
|--------|--------|
| 401 | Token assente, scaduto, firma invalida |
| 403 | Token ok ma non sei P0/P1 di quella partita |
| 404 | Partita inesistente (né RAM né Supabase) |
| 400 | Regole gioco / join non valido / body |

---

## Env rilevanti (preview 4.2.2+)

| Var | Uso |
|-----|-----|
| `SUPABASE_URL` | già |
| `SUPABASE_SERVICE_KEY` | persistenza (bypass RLS) |
| `SUPABASE_JWT_SECRET` | verify access token (scelta preferita in 4.2.2) |

---

## Done 4.2.1

- [x] Tabella endpoint
- [x] Scelta A documentata
- [x] Contesto “in costruzione” documentato
- [x] Niente legacy open
