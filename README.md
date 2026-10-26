# Tactical Card Game 5×5 – Backend (v2)

Motore di gioco Python puro fedele al GDD ufficiale.

## Cosa c’è in v2 (rispetto a v1)

- Database **180 carte** completo (5 colori 0-5 + 15 Boss + 15 Mostrissimi)
- Evocazione Mostri/Boss solo in zona Tempio
- Piazzamento Trappole nascoste + attivazione all’ingresso
- Maledizioni con effetti base (cura, danno, scudo, debuff ATK, mana)
- Esplorazione tessere Evento (Portali, Palude, Santuario, Fenditura, Muro Illusione, Fossa Spine, Runa Furto, …)
- Main Quest (Dominio del Territorio + Superiorità Numerica) verificate a inizio turno
- **Mostrissimi Eldrazzici**: pool comune di 3, evocazione a 0 mana con N sacrifici (uno obbligatorio su Cerchio Rituale)
- Effetti a inizio turno (Santuario +1 HP, Fenditura 1 danno, Growth, Regenerate)
- CLI aggiornata con comando `x` per i Mostrissimi

## Come testare

```bash
cd backend
python3 main.py
```

### Comandi CLI

| Comando | Descrizione |
|---------|-------------|
| `m B5 C4` | Muovi unità da B5 a C4 (solo diagonale, costa 1 mana) |
| `p 0` | Gioca la carta indice 0 della mano (Mostro → zona Tempio automatica) |
| `p 2 B5` | Gioca carta 2 su casella B5 (Trappole / Maledizioni con target) |
| `x 0 A1 B5` | Evoca Mostrissimo indice 0 sacrificando le creature su A1 e B5 (una deve essere su Cerchio Rituale) |
| `s` | Stampa stato completo (mappa, mana, mano, Mostrissimi) |
| `e` | Fine turno |
| `q` | Esci |

## Stack previsto

| Layer | Tecnologia |
|-------|------------|
| Logica | Python 3.12 (questa cartella) |
| API | FastAPI (prossimo) |
| Frontend | Next.js |
| DB / Auth / Realtime | Supabase |
| Hosting | Render |
| Repo | GitHub (`/backend` + `/docs`) |

## Prossimi passi (v3+)

1. IA base con priorità (difesa Corona, Altare, Main Quest)
2. FastAPI + WebSocket
3. Schema Supabase
4. Frontend griglia interattiva
5. Deploy Render

Leggi anche **`architettura.md`** per la mappa completa del codice.
