# Roadmap – Penumbra

**Versione attuale: v1.6**

## Stato attuale
v1.6 – Aggiunta `hex_to_pixel` in `constants.py`.  
Questo risolve il secondo ImportError che faceva fallire il deploy su Render dopo il fix di `parse_hex_key`.

---

## 1. Sistema di consegne e documentazione (completato)
**Stato: CHIUSO**

---

## 2. Migrazione completa alla mappa esagonale (in corso)

### 2.1 Core della mappa
- [x] 2.1.1 Sistema coordinate + compatibilità completa con map_board v39
- [x] 2.1.1b Aggiunto `parse_hex_key` (v1.5)
- [x] 2.1.1c Aggiunto `hex_to_pixel` (v1.6)
- [ ] 2.1.2 Verifica caricamento map.json
- [ ] 2.1.3 – 2.1.5 (Tile, Board, Unit) – in gran parte già presenti nel map_board fornito

### 2.2 Logica di gioco
Da verificare dopo che il deploy di v1.6 parte correttamente.

---

## Rischi e note
- L’utente non è tecnico → ogni passaggio deve essere semplice e guidato.
- URL Render e Supabase devono restare scritti in architettura.md.
- Possibili altri ImportError se altri file richiedono funzioni non ancora presenti in constants.py.
