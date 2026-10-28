# Istruzioni per IA – Penumbra

## Consegne e versioni (obbligatorio)
- **Ogni consegna va in una cartella nuova** con numero ascendente: `penumbra_v28`, `penumbra_v29`, `penumbra_v30`, …
- Non sovrascrivere la cartella della versione precedente: copia e modifica nella nuova.
- Utente non tecnico; **niente modifiche manuali** richieste all’utente.
- Ad ogni consegna aggiornare: `README.md`, `ROADMAP.md`, `architettura.md`, `istruzioni_per_IA.md`.

## Regole di gioco da rispettare
- UI partita: niente PvP/Unisciti finché non si lavora su quella modalità.
- Corona = carta in mano costo 0/3/6, non bottone dedicato.
- Draft = buste; movimento = re; Giallo = proxy.
- Mappa: griglia 7×7, templi angoli (P0=`A6`, P1=`G0`), cornice non giocabile, muri edge, spawn solo Tempio, Altare `D3`.
- **Fog of war**: visione raggio 2 (Chebyshev) da creature e Tempio del giocatore; magie a bersaglio non colpiscono unità nascoste.
- **Neutrali Altare (v29)**: a fine turno di ogni giocatore spawn sull’Altare con stats crescenti 1/1…6/6 (Signore), poi reset; comportamento vagabondaggio / inseguimento; Signore = BBEG (regole da definire).
- Auth obbligatorio (Supabase JWT).
