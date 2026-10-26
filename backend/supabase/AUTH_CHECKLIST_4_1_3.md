# 4.1.3 – Checklist Auth email/password (Supabase)

**Obiettivo:** poter creare utenti di test con email fittizie (`fra@test.local`) senza SMTP reale.  
**Nessun codice app in questo step.** Solo configurazione dashboard + note.

Segna le caselle mentre lavori sul progetto Supabase collegato a Penumbra.

---

## A. Provider Email

- [ ] Dashboard → **Authentication** → **Providers**
- [ ] **Email** abilitato (Enable Email provider)
- [ ] “Confirm email” in **dev**: **disabilitato** (o “Allow unconfirmed” se presente)  
  → così `*@test.local` non richiede casella mail vera
- [ ] Password min length accettabile (default ok, es. ≥ 6)

**Nota produzione (dopo Fase 4):** riattivare conferma email e SMTP reali; le email `test.local` restano solo per dev.

---

## B. URL / redirect (anche se la UI login arriva in 4.4)

- [ ] **Authentication** → **URL Configuration**
- [ ] Site URL: per ora URL Render dell’API **oppure** futuro GitHub Pages (es. `https://<user>.github.io/Penumbra/`)
- [ ] Redirect URLs: aggiungere almeno
  - `http://localhost:3000/**` (se testerai in locale)
  - URL Pages quando esisterà
  - URL static servito da Render se usi quello

In 4.1 non serve ancora una UI login completa: gli utenti si creano dalla dashboard (4.1.4).

---

## C. Email fittizie `*@test.local`

| Cosa | Dettaglio |
|------|-----------|
| Funzionano? | Sì **se** create da **Dashboard → Authentication → Users → Add user** (o Admin API), non via signup pubblico che manda mail |
| Ricevono posta? | No — `test.local` non è un dominio mail reale |
| Confirm | Con confirm **off** in dev, l’utente è subito usabile |
| Password | Scegline una forte e **non** committarla nel repo |

Esempi previsti:

- `fra@test.local` — giocatore umano (P0)
- opzionale `p2@test.local` — solo se vuoi simulare PvP più avanti

---

## D. Chiavi da conoscere (non committare i secret)

| Env | Uso |
|-----|-----|
| `SUPABASE_URL` | già in Render (es. `https://xxxx.supabase.co`) |
| `SUPABASE_ANON_KEY` | client / prototipo attuale |
| `SUPABASE_SERVICE_KEY` (service_role) | **solo server** in 4.2+; non nel frontend |

- [ ] Hai copiato URL e anon key in Render env (già fatto se restore funzionava)
- [ ] Service role key tenuta da parte per 4.2 (Settings → API) — **non** in repo git

---

## E. Cosa non fare in 4.1.3

- Non chiudere ancora le policy RLS anon (→ 4.1.5)
- Non modificare FastAPI / JWT (→ 4.2)
- Non implementare form di login (→ 4.4)
- Non pubblicare password o service_role su GitHub

---

## F. Verifica rapida “Auth ok”

1. [ ] Provider Email ON, confirm disabilitato in dev  
2. [ ] (Opzionale subito, obbligatorio in 4.1.4) creato almeno un user da dashboard  
3. [ ] Login di prova da **Authentication → Users** (utente presente, non banned)  
4. [ ] Partite/API esistenti ancora ok (nessun cambio schema Auth obbligatorio oltre al provider)

---

## G. Output da annotare in privato (non nel repo)

```
SUPABASE_URL=...
Test user email=fra@test.local
Test user uid=<incolla da Authentication → Users>
Password=<solo password manager>
```

L’**uid** servirà in 4.1.4 / 4.1.6 / 4.2 per `player0_uid`.

---

## Done 4.1.3

Quando A + C (policy confirm) + D (chiavi note) sono a posto, 4.1.3 è completo.  
Creazione effettiva utenti = **4.1.4**.
