# Roadmap – Penumbra

**Versione attuale: v1.7**

## Stato attuale
v1.7 – Aggiornati i muri della mappa esagonale secondo il JSON dell’utente (editor HTML).

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
- [ ] 2.1.3 – 2.1.5 (Tile, Board, Unit) – in gran parte già presenti nel map_board fornito

### 2.2 Logica di gioco
Da verificare dopo che il deploy di v1.7 mostra i muri corretti.

---

## Rischi e note
- L’utente non è tecnico → ogni passaggio deve essere semplice e guidato.
- URL Render e Supabase devono restare scritti in architettura.md.
