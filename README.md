# Django Authentication Boilerplate

A production-oriented Django starter with:
- **Web authentication** (`django-allauth`) for signup, login/logout, password reset, and mandatory email verification.
- **API authentication** (`dj-rest-auth` + DRF token auth) for registration and login/logout flows.
- **Social login providers** (Google, Microsoft, Facebook).
- **Custom user model** (`accounts.User`) using email as the primary identifier.

---

## 1) Final project tree (updated)

```text
Django-boilerplate/
├── accounts/
│   ├── adapters.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   └── serializers.py
├── config/
│   ├── asgi.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── api_views.py
│   ├── forms.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── templates/core/
│   ├── urls.py
│   └── views.py
├── profiles/
│   ├── api_urls.py
│   ├── forms.py
│   ├── mixins.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── templates/profiles/
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── account/signup.html
│   ├── base.html
│   └── registration/login.html
├── manage.py
├── requirements.txt
└── README.md
```

---

## 2) Step-by-step setup guide

### A. Installation

1. **Clone and move into the project**
   ```bash
   git clone <your-repo-url>
   cd Django-boilerplate
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate   # Windows PowerShell
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set environment variables** (recommended for production readiness)
   - `DJANGO_SETTINGS_MODULE=config.settings.dev` for local development
   - `SECRET_KEY=<your-secret-key>`
   - `DEBUG=False` in production
   - `ALLOWED_HOSTS=<comma-separated-hosts>`
   - Database credentials and OAuth client credentials as needed

### B. Migrations

1. **Generate migration files (if models changed)**
   ```bash
   python manage.py makemigrations
   ```

2. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

3. **(Optional) Confirm migration state**
   ```bash
   python manage.py showmigrations
   ```

### C. Create superuser

```bash
python manage.py createsuperuser
```

Then log in to admin at:
- `http://localhost:8000/admin/`

### D. Run development server

```bash
python manage.py runserver
```

App runs at:
- `http://localhost:8000/`

---

## 3) API testing guide (Postman + curl)

Base URL:
- `http://localhost:8000`

### A. Register user

**Endpoint**: `POST /api/auth/registration/`

```bash
curl -X POST http://localhost:8000/api/auth/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"user@example.com",
    "password1":"StrongPass123!",
    "password2":"StrongPass123!",
    "full_name":"Jane Doe"
  }'
```

### B. Login user (retrieve token/session payload)

**Endpoint**: `POST /api/auth/login/`

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"user@example.com",
    "password":"StrongPass123!"
  }'
```

Save returned token (if token auth response includes it).

### C. Authenticated request

```bash
curl http://localhost:8000/health/ \
  -H "Authorization: Token <your_token_here>"
```

### D. Logout

**Endpoint**: `POST /api/auth/logout/`

```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Token <your_token_here>"
```

### Postman collection flow

1. Create an environment variable: `base_url = http://localhost:8000`
2. Add requests in order:
   - Register
   - Login
   - Authenticated test endpoint
   - Logout
3. In login test script, save token:
   ```javascript
   const json = pm.response.json();
   if (json.key) pm.environment.set("auth_token", json.key);
   ```
4. Use header in protected requests:
   - `Authorization: Token {{auth_token}}`

---

## 4) Common pitfalls and fixes

1. **`ModuleNotFoundError: No module named 'django'`**
   - Cause: dependencies not installed in active virtualenv.
   - Fix:
     ```bash
     source .venv/bin/activate
     pip install -r requirements.txt
     ```

2. **Social login callback mismatch**
   - Cause: provider redirect URI does not exactly match configured callback.
   - Fix: use exact callbacks:
     - Google: `http://localhost:8000/accounts/google/login/callback/`
     - Microsoft: `http://localhost:8000/accounts/microsoft/login/callback/`
     - Facebook: `http://localhost:8000/accounts/facebook/login/callback/`

3. **Emails not being delivered in development**
   - Cause: console email backend is used by default.
   - Fix: expected behavior in dev; switch to SMTP provider in production settings.

4. **`DisallowedHost` errors**
   - Cause: host not listed in `ALLOWED_HOSTS`.
   - Fix: add domain/IP to `ALLOWED_HOSTS` in the active settings module.

5. **Authentication works in browser but not API client**
   - Cause: mixing session auth and token auth.
   - Fix: ensure API requests include proper `Authorization: Token ...` header.

6. **Static files missing in production**
   - Cause: static collection or web server static routing not configured.
   - Fix:
     ```bash
     python manage.py collectstatic
     ```
     and configure Nginx/Whitenoise/CDN appropriately.

---

## 5) Suggestions for scaling into a SaaS product

1. **Move to PostgreSQL + managed database**
   - Use PostgreSQL in all non-local environments.
   - Enable automated backups and point-in-time restore.

2. **Adopt robust environment segregation**
   - Separate `dev`, `staging`, `prod` settings.
   - Use secrets manager (AWS Secrets Manager, GCP Secret Manager, Vault).

3. **Introduce asynchronous workloads**
   - Add Celery + Redis (or RQ) for email, reports, webhooks, and background jobs.

4. **Harden auth/security**
   - Enforce HTTPS, HSTS, secure cookies, CSRF controls.
   - Add login throttling/rate limiting (e.g., django-axes or DRF throttles).
   - Consider MFA for admin and enterprise tenants.

5. **Implement multi-tenancy early**
   - Decide strategy: row-based tenancy (tenant FK) vs schema-based tenancy.
   - Add tenant-aware permissions and isolation tests.

6. **Observability and SRE baseline**
   - Structured logging, centralized log ingestion.
   - Metrics (request latency, error rate, queue depth), tracing, alerting.
   - Health/readiness endpoints for orchestration.

7. **CI/CD and quality gates**
   - Add automated checks: `black`, `isort`, `flake8/ruff`, tests, security scans.
   - Deploy through staged pipelines with rollback support.

8. **API lifecycle management**
   - Version APIs (`/api/v1/...`), publish OpenAPI schema.
   - Add contract tests to prevent breaking changes.

9. **Billing + entitlement model**
   - Integrate Stripe (or equivalent), implement plan/feature flags.
   - Track subscription state and enforce limits by tenant.

10. **Performance and cost controls**
    - Add Redis caching, queryset optimization, pagination defaults.
    - Profile N+1 queries and tune DB indexes using slow query insights.

---

## Existing authentication configuration summary

### allauth web flows
- Signup: `/accounts/signup/`
- Login: `/accounts/login/`
- Logout: `/accounts/logout/`
- Password reset: `/accounts/password/reset/`
- Email verification is mandatory.

### dj-rest-auth API flows
- Register: `POST /api/auth/registration/`
- Login: `POST /api/auth/login/`
- Logout: `POST /api/auth/logout/`
- Password reset: `POST /api/auth/password/reset/`

### Custom user integration
- `AUTH_USER_MODEL = 'accounts.User'`
- Email as unique login identifier.
- Registration serializer supports `full_name`.
