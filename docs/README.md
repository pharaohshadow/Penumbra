# Docs – Penumbra (GitHub Pages)

Questa cartella è la **source** di GitHub Pages.

## Contenuto minimo

- `index.md` – homepage
- `_config.yml` – configurazione Jekyll (tema primer)
- `assets/css/style.scss` – stylesheet richiesto dal tema

## Come è configurato il workflow

Il workflow `jekyll-build-pages` usa come source la cartella `docs/`.  
Se questa cartella manca, il build fallisce con:

```
No such file or directory @ dir_chdir0 - /github/workspace/docs
```

## Aggiornamenti futuri

Qui andranno:
- Regole del gioco (sintesi del GDD)
- Guide di setup
- Changelog delle versioni backend
