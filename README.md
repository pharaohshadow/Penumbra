# Penumbra – Consegna v35

## Fix deploy Render
- `backend/api/__init__.py` era corrotto (`404: Not Found` come contenuto) → **SyntaxError** all’avvio.
- File ripristinato a package vuoto valido.

## Contenuto
Include v34 (login Supabase) + v33 (mappa hex) + fix package.

**Nessuna modifica manuale.** Cartella: `penumbra_v35/`

Assicurati di pushare su GitHub **tutto** il contenuto di `backend/`, in particolare:
- `backend/api/__init__.py` (solo docstring/package, **non** testo 404)
- `backend/static/index.html`
- `backend/core/*`
