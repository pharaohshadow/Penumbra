# Patch prioritaria key (consigliata con 4.1.5)

In `backend/api/supabase_store.py` sostituisci:

```python
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "") or os.environ.get("SUPABASE_SERVICE_KEY", "")
```

con:

```python
# Preferisci service_role (bypass RLS). Mai esporre questa key al browser.
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "") or os.environ.get("SUPABASE_ANON_KEY", "")
```

Nessun altro cambio richiesto per 4.1.5.
