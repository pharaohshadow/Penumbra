# Architettura – Penumbra

**Versione attuale: v1**

Questo file contiene i dettagli tecnici “difficili da recuperare”.  
Deve essere aggiornato ogni volta che cambiano URL, impostazioni o struttura importante.

---

## URL e servizi

| Servizio       | URL / Note                                      | Stato          |
|----------------|--------------------------------------------------|----------------|
| GitHub         | https://github.com/pharaohshadow/Penumbra        | Attivo         |
| Sito live      | (da inserire – Render)                           | Da completare  |
| Supabase       | (da inserire – project URL)                      | Da completare  |
| Render         | (da inserire – dashboard del servizio)           | Da completare  |

---

## Supabase

- **Tabelle principali**:
  - `games` (stato partita + ownership player0_uid / player1_uid)
  - `game_moves` (log delle mosse)

- **Auth**: Supabase Auth (JWT)
- **Storage Buckets**: al momento nessuno rilevante
- **Edge Functions**: nessuna al momento
- **RLS**: presente ma ancora aperta (prototipo)

Schema di riferimento: `backend/supabase/schema.sql`

---

## Render

- Tipo di servizio: Web Service
- File di configurazione: `render.yaml` (presente nel repository)
- Variabili d’ambiente importanti:
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY` (o `SUPABASE_SERVICE_KEY`)
  - `SUPABASE_JWT_SECRET` (consigliato)

---

## Struttura repository (mappa base)
