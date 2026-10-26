# 4.2.1 – Contratto auth endpoint (API protetta)

**Decisioni fisse (non richiedere di nuovo):**

1. **Legacy ownership:** opzione **A** — se `player0_uid` e `player1_uid` sono entrambi null (o la partita non ha membership valida), **403**. Nessuna partita “aperta” per game_id.  
2. **Stato prodotto:** sito **in costruzione**; non ci sono partite reali in corso né utenti che giocano in produzione. Si può fare hard cut senza migrazione utenti live.

---

## Header

```http
Authorization: Bearer <supabase_access_token>
```

- `401` — token assente, malformato o non valido  
- `403` — token valido ma uid **non** membro del match (o partita legacy senza uid)  
- `404` — partita inesistente (dopo auth), se applicabile  

Membership: `uid == player0_uid` **oppure** `uid == player1_uid`.  
Partita base vs IA: di norma solo `player0_uid` valorizzato; P1 è IA.

---

## Tabella endpoint

| Metodo | Path | Auth | Membership | Note |
|--------|------|------|------------|------|
| GET | `/` | no | — | serve static UI |
| GET | `/api/health` | **no** | — | monitoring / cron keep-alive |
| POST | `/api/new` | **JWT** | — (diventi P0) | set `player0_uid=sub`, `vs_ai` da body, `player1_uid=null` se vs IA |
| GET | `/api/state` | **JWT** | **sì** | senza `game_id`: comportamento da definire in 4.2.5 (preferenza: non creare partita anonima; richiedere new esplicito o new autenticato) |
| POST | `/api/join` | **JWT** | slot P1 | no se `vs_ai`; set `player1_uid=sub` |
| POST | `/api/move` | **JWT** | **sì** | + turno/regole gioco |
| POST | `/api/play` | **JWT** | **sì** | |
| POST | `/api/end` | **JWT** | **sì** | |
| POST | `/api/eldrazi` | **JWT** | **sì** | |
| POST | `/api/fragment` | **JWT** | **sì** | |
| POST | `/api/draft` | **JWT** | **sì** | |

Static `/static/*` se montato: pubblico (asset).

---

## `GET /api/state` senza `game_id`

**Oggi:** crea una nuova partita vs IA (comportamento comodo ma incompatibile con “sempre authed”).

**4.2 (scelta):**  
- Con JWT e senza `game_id` → **400** con messaggio tipo “fornire game_id oppure POST /api/new”  
- **Non** auto-create senza ownership esplicita  

(Implementazione in 4.2.5.)

---

## Env rilevanti (preview 4.2.2)

| Env | Uso |
|-----|-----|
| `SUPABASE_URL` | già |
| `SUPABASE_SERVICE_KEY` | store (bypass RLS) |
| `SUPABASE_JWT_SECRET` o JWKS | verify access token |
| ~~`ALLOW_LEGACY_OPEN`~~ | **non usato** (scelta A) |

---

## Fuori scope 4.2.1

Implementazione JWT/codice → 4.2.2+.

**Done 4.2.1:** questo contratto.
