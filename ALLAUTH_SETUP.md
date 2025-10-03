# Django-Allauth Integration Guide

## ✅ Successfully Configured!

Your procurement system now uses **django-allauth** for complete authentication management.

---

## 🔐 Available URLs

### User Authentication
- **Login**: http://localhost:8000/accounts/login/
- **Logout**: http://localhost:8000/accounts/logout/
- **Sign Up (Register)**: http://localhost:8000/accounts/signup/
- **Password Reset**: http://localhost:8000/accounts/password/reset/
- **Password Change**: http://localhost:8000/accounts/password/change/

### Dashboard
- **Dashboard**: http://localhost:8000/dashboard/
- **Admin**: http://localhost:8000/admin/

---

## 🎨 Features Enabled

✅ **Email-based authentication** (no username required)
✅ **User registration** with email validation
✅ **Password reset** via email
✅ **Password change** for logged-in users
✅ **"Remember me"** functionality
✅ **Custom adapter** for Usuario model integration
✅ **Beautiful Bootstrap 5 templates** (matching your design)
✅ **Automatic role assignment** (new users = VENDEDOR)

---

## 📝 How It Works

### Registration Flow
1. User goes to `/accounts/signup/`
2. Enters email and password (twice)
3. Account created with role = VENDEDOR
4. Auto-login (optional) and redirect to dashboard

### Login Flow
1. User goes to `/accounts/login/`
2. Enters email and password
3. Optional "Remember me" checkbox
4. Redirects to dashboard

### Password Reset Flow
1. User clicks "Forgot password?" on login page
2. Enters email at `/accounts/password/reset/`
3. Receives email with reset link
4. Sets new password
5. Redirects to login

---

## ⚙️ Configuration

### Settings (already configured in settings.py)

```python
# Custom adapter for Usuario model
ACCOUNT_ADAPTER = 'users.adapter.CustomAccountAdapter'

# Email as username
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# Password requirements
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True

# Session management
ACCOUNT_SESSION_REMEMBER = True

# Email verification (optional for now)
ACCOUNT_EMAIL_VERIFICATION = 'optional'

# Redirects
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'
```

### Custom Adapter (users/adapter.py)

The `CustomAccountAdapter` handles:
- Setting default role (VENDEDOR) for new users
- Setting status and is_active flags
- Tracking who created the account (if admin)
- Custom redirect after login

---

## 🎯 Templates Created

All templates are in `templates/django/account/`:

- `base.html` - Base template with navbar and styling
- `login.html` - Login page
- `signup.html` - Registration page
- `logout.html` - Logout confirmation
- `password_reset.html` - Request password reset
- `password_reset_done.html` - Reset email sent confirmation

All templates use:
- Bootstrap 5
- Font Awesome icons
- Gradient background
- Responsive design
- Form validation

---

## 🔧 Customization Options

### Change Email Verification

**Make email verification required:**
```python
# In settings.py
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
```

**Disable email verification:**
```python
ACCOUNT_EMAIL_VERIFICATION = 'none'
```

### Change Default Role for New Users

Edit `users/adapter.py`:
```python
def save_user(self, request, user, form, commit=True):
    user.rol = 'COMPRADOR'  # Change to desired default role
    # ...
```

### Disable Registration

If you don't want public registration:
```python
# In settings.py
ACCOUNT_ADAPTER = 'users.adapter.NoSignupAccountAdapter'
```

Then create in `users/adapter.py`:
```python
class NoSignupAccountAdapter(CustomAccountAdapter):
    def is_open_for_signup(self, request):
        return False
```

### Add Social Authentication

allauth supports Google, Facebook, GitHub, etc.:

```python
# In settings.py INSTALLED_APPS
'allauth.socialaccount',
'allauth.socialaccount.providers.google',
'allauth.socialaccount.providers.github',
```

---

## 📧 Email Configuration

For password reset and email verification to work, configure email in `.env`:

```bash
# Console backend (development - prints to console)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Or use SMTP (production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@compras-soft.com
```

---

## 🧪 Testing

### Test Registration
```bash
# Go to http://localhost:8000/accounts/signup/
# Create account with:
# - Email: test@example.com
# - Password: TestPass123!
# - Confirm password

# Should auto-login and redirect to dashboard
```

### Test Login
```bash
# Go to http://localhost:8000/accounts/login/
# Login with credentials above
```

### Test Password Reset
```bash
# Go to http://localhost:8000/accounts/login/
# Click "Forgot password?"
# Enter email
# Check console for reset link (development mode)
```

---

## 🎛️ Admin Management

Admins can still create users via Django admin:
- Go to http://localhost:8000/admin/
- Click "Usuarios" → "Add Usuario"
- Fill in email, password, and role
- User can then login via allauth

---

## 🔄 Migration from Custom Login

The old custom login views have been removed. All authentication now flows through allauth:

**Before:**
- `/login/` → custom view
- `/logout/` → custom view

**After:**
- `/accounts/login/` → allauth
- `/accounts/logout/` → allauth
- `/accounts/signup/` → allauth (NEW!)
- `/accounts/password/reset/` → allauth (NEW!)

---

## 📚 More Features Available

allauth provides many more features you can enable:

- Two-factor authentication (2FA)
- Social authentication (Google, Facebook, etc.)
- Email confirmation required
- Rate limiting for login attempts
- Custom authentication backends
- Token authentication for APIs

Check docs: https://django-allauth.readthedocs.io/

---

## ✨ Summary

Your system now has:
- ✅ Complete authentication via allauth
- ✅ User registration
- ✅ Password reset
- ✅ Email-based login
- ✅ Beautiful templates
- ✅ Custom adapter for Usuario model
- ✅ Ready for production

**Start using it:**
1. `docker-compose up` (or your preferred method)
2. Run migrations if needed
3. Visit http://localhost:8000/accounts/signup/
4. Create your first user!

🎉 **All set!**

