# Django Authentication Boilerplate

## Implemented authentication scope

- Web auth via `django-allauth`: signup, login, logout, mandatory email verification, password reset.
- API auth via `dj-rest-auth`: registration, login/logout, token auth.
- Social login providers: Google, Microsoft, Facebook.
- Custom user model (`accounts.User`) connected to both web and API flows.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Configuration details

### 1) allauth web flows
- URLs: `/accounts/signup/`, `/accounts/login/`, `/accounts/logout/`, `/accounts/password/reset/`
- Email verification is mandatory (`ACCOUNT_EMAIL_VERIFICATION = "mandatory"`).
- Email backend defaults to console backend for development.

### 2) dj-rest-auth API flows
- Registration: `POST /api/auth/registration/`
- Login: `POST /api/auth/login/`
- Logout: `POST /api/auth/logout/`
- Password reset: `POST /api/auth/password/reset/`
- Token auth enabled through DRF `TokenAuthentication` and `authtoken.Token`.

### 3) Social login setup
Create social apps in Django admin (`/admin/socialaccount/socialapp/`) OR configure via env/db fixture.

Provider callback URLs:
- Google: `http://localhost:8000/accounts/google/login/callback/`
- Microsoft: `http://localhost:8000/accounts/microsoft/login/callback/`
- Facebook: `http://localhost:8000/accounts/facebook/login/callback/`

Use these values in provider consoles:
- Client ID
- Client Secret
- Authorized redirect URL (exact match with callback above)

Then attach each `SocialApp` to `Site` with domain `localhost:8000`.

### 4) Custom user integration
- `AUTH_USER_MODEL = 'accounts.User'`
- Email is the unique identifier (`USERNAME_FIELD = 'email'`).
- allauth configured for email-only auth (no username).
- API register serializer (`CustomRegisterSerializer`) stores `full_name`.

## API examples

### Register
```bash
curl -X POST http://localhost:8000/api/auth/registration/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password1":"StrongPass123!","password2":"StrongPass123!","full_name":"Jane Doe"}'
```

### Login (token)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"StrongPass123!"}'
```

### Authenticated request
```bash
curl http://localhost:8000/health/ -H "Authorization: Token <token>"
```

## Flow explanation

1. User signs up (web/API).
2. allauth creates inactive-ish email state and sends email confirmation.
3. User confirms email via link.
4. User logs in via web session or API token endpoint.
5. Social login users are authenticated via OAuth callback and linked/created as local users.
6. Logout invalidates session (web) or token session context (API endpoint semantics).
