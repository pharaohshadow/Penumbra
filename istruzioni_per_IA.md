# Istruzioni per IA – Penumbra

Questo file raccoglie le preferenze e le regole operative dell’autore.
Va aggiornato a ogni nuova consegna (v2, v3, …) aggiungendo le istruzioni successive.

---

## Istruzioni ricevute finora

### 1. Contesto iniziale

- Repo: https://github.com/pharaohshadow/Penumbra
- Leggere: README, architettura, roadmap
- Progetto: Tactical Card Game 5×5 (Mage Wars + Scacchi + MOBA + 7th Continent)
- Backend Python (FastAPI) + persistenza opzionale Supabase + UI static

### 2. Procedere senza rompere ciò che esiste

- Preferenza esplicita: **non rompere** codice/funzionalità già presenti.
- Cambiamenti additive e backward-compatible quando possibile.
- Snapshot vecchi devono continuare a funzionare dopo upgrade di serialize/hydrate.

### 3. Formato di consegna dei file

- Consegne in cartelle versionate: `v1`, `v2`, `v3`, …
- Ogni cartella deve contenere almeno:
  - `README.md` aggiornato (punto di ingresso handoff)
  - `architettura.md` aggiornato
  - `ROADMAP.md` aggiornato con dove siamo arrivati
  - `istruzioni_per_IA.md` (questo file, cumulativo)
  - i file di codice modificati, organizzati come nel repo (`backend/api/…` ecc.)

### 4. README come unico handoff tra chat

- Il README della cartella di consegna deve essere **l’unico file** che l’autore deve mandare a una nuova chat per il passaggio di consegne quando la conversazione diventa troppo lunga.
- Il README deve rimandare chiaramente agli altri file della stessa cartella.

### 5. Lingua

- Comunicare in italiano (l’autore scrive in italiano).

---

## Preferenze operative (derivate)

- Avanzare lungo la **roadmap ufficiale** del repo (non inventare feature fuori sequenza senza accordo).
- Documentare sempre cosa è cambiato e cosa resta limitato.
- Versionare API in modo leggero (`/api/health` → `version`).
- Preferire patch minime e leggibili rispetto a refactor ampi.

---

## Aggiornamenti futuri

(Le nuove istruzioni dell’autore vanno aggiunte qui sotto, numerate.)
