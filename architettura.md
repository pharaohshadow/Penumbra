# Architettura – v1.10

## Stato attuale

### Fix Fog of War (bug visioni “doppie”)
In `game_state.py` la funzione `is_visible_to` controllava la distanza **due volte** con le coordinate invertite.
Effetto: oltre alla tua zona (basso a sinistra, Tempio 1) si “accendeva” anche un’area in alto a destra vicino al Tempio 2.

**Fix v28.4:** le fonti di visione sono solo `(q, r)` del tuo tempio + delle tue creature. Nessun doppio check invertito.

### Grafica mappa (stato intermedio)
- Esagoni flat-top, colori scuri
- Ostacoli ancora disegnati come linee (creste) → da sostituire con montagne irregolari (vedi roadmap §3)
- Bordo esterno stile montagna, distinto dal fog

### File toccati in questa consegna
- `backend/core/game_state.py` (solo Fog of War)

### Supabase
- URL: `https://favrmxwyaxklfiruyvqz.supabase.co`

### Render
- URL live: https://penumbra-8psb.onrender.com
