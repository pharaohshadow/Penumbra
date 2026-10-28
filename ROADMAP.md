# Roadmap – Penumbra

**Versione attuale: v1.9**

## Stato attuale
v1.9 – Mappa: tessere unite, ostacoli come montagne, bordo esterno montagnoso (non confondibile col fog).

---

## 1. Sistema di consegne e documentazione (completato)
**Stato: CHIUSO**

---

## 2. Migrazione completa alla mappa esagonale (in corso)

### 2.1 Core della mappa
- [x] 2.1.1 Sistema coordinate + compatibilità completa con map_board v39
- [x] 2.1.1b Aggiunto `parse_hex_key` (v1.5)
- [x] 2.1.1c Aggiunto `hex_to_pixel` (v1.6)
- [x] 2.1.2 Muri aggiornati dall’utente (v1.7)
- [x] 2.1.2b Stile grafico mappa come editor (v1.8)
- [x] 2.1.2c Montagne al posto dei muri rossi + bordo esterno montagna (v1.9)
- [ ] 2.1.3 – 2.1.5 (Tile, Board, Unit)

### 2.2 Logica di gioco
Da verificare dopo il deploy di v1.9.

---

## Rischi e note
- L’utente non è tecnico → ogni passaggio deve essere semplice e guidato.
