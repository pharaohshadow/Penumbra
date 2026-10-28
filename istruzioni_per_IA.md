# Istruzioni per IA – Penumbra

## Consegne
- Cartella `penumbra_vXX` ascendente.
- **Mai** lasciare file `__init__.py` con contenuto di errore HTTP (es. "404: Not Found").
- Auth = Supabase client-side; backend verifica JWT.
- Deploy Render: `uvicorn api.main:app` con cwd/PYTHONPATH su `backend/`.
