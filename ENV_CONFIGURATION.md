# Environment Configuration Guide

## ✅ Your `.env` File Has Been Created!

A fresh `.env` file with a secure SECRET_KEY has been created for you.

---

## 📋 Current Configuration (Development)

Your `.env` file is configured for **Docker development**:

```bash
# Django
SECRET_KEY=e9m$ktrif7cy2m(vz6^*_aptqm#5aen*0bogl^68*#$^rxr$t0
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Docker service names)
DB_NAME=procurement_db
DB_USER=procurement_user
DB_PASSWORD=procurement_password
DB_HOST=db        # Docker service name
DB_PORT=5432

# Redis (Docker service name)
REDIS_HOST=redis  # Docker service name
REDIS_PORT=6379
REDIS_DB=0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email (console for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Security (development)
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False
```

---

## 🐳 For Docker (Current Setup)

**✅ You're all set!** The above configuration works with:

```bash
docker-compose up
```

Emails will print to the console where docker-compose is running.

---

## 💻 For Local Development (Without Docker)

If running **without Docker**, change these values:

```bash
# Change service names to localhost
DB_HOST=localhost           # was: db
REDIS_HOST=localhost        # was: redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

**Requirements:**
- PostgreSQL running locally on port 5432
- Redis running locally on port 6379
- Create the database manually:
  ```sql
  CREATE DATABASE procurement_db;
  CREATE USER procurement_user WITH PASSWORD 'procurement_password';
  GRANT ALL PRIVILEGES ON DATABASE procurement_db TO procurement_user;
  ```

---

## 📧 Email Configuration

### Option 1: Console Backend (Current - Development)
```bash
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
✅ **Good for:** Development, testing  
✅ **Behavior:** Emails print to console  
✅ **No setup needed**

### Option 2: Gmail SMTP (Production)
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@compras-soft.com
SERVER_EMAIL=server@compras-soft.com
```

**Gmail Setup:**
1. Go to Google Account settings
2. Enable 2-factor authentication
3. Generate an "App Password"
4. Use that password in `EMAIL_HOST_PASSWORD`

### Option 3: SendGrid (Production)
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@compras-soft.com
```

### Option 4: AWS SES (Production)
```bash
EMAIL_BACKEND=django_ses.SESBackend
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_SES_REGION_NAME=us-east-1
AWS_SES_REGION_ENDPOINT=email.us-east-1.amazonaws.com
DEFAULT_FROM_EMAIL=noreply@compras-soft.com
```

---

## 🔐 Security Settings

### Development (Current)
```bash
DEBUG=True
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False
```

### Production (Recommended)
```bash
DEBUG=False
SECRET_KEY=generate-a-new-long-random-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Security Headers
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY
```

---

## 🗄️ Database Configuration

### PostgreSQL (Current)
```bash
DB_NAME=procurement_db
DB_USER=procurement_user
DB_PASSWORD=procurement_password
DB_HOST=db
DB_PORT=5432
```

### Custom PostgreSQL
```bash
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=strong_password_here
DB_HOST=your_db_host
DB_PORT=5432
```

### Connection String (Alternative)
```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
```

---

## 🎯 Different Environments

### Create Multiple .env Files

**.env.development**
```bash
DEBUG=True
DB_HOST=db
REDIS_HOST=redis
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**.env.production**
```bash
DEBUG=False
DB_HOST=production-db-host.com
REDIS_HOST=production-redis-host.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
# ... full email config
```

**Use with:**
```bash
# Development
cp .env.development .env
docker-compose up

# Production
cp .env.production .env
docker-compose -f docker-compose.prod.yml up
```

---

## 🔧 Advanced Settings

### Celery Configuration
```bash
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CELERY_TASK_ALWAYS_EAGER=False  # True for synchronous (testing)
```

### Redis Configuration
```bash
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your-redis-password  # if using password
```

### Django Settings
```bash
LANGUAGE_CODE=es-ar         # Spanish (Argentina)
TIME_ZONE=America/Argentina/Buenos_Aires
USE_I18N=True
USE_TZ=True
```

---

## ⚠️ Important Notes

### 🔑 SECRET_KEY
- **Never commit** your `.env` file to git
- Use a **different SECRET_KEY** for production
- Generate new key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### 🔒 Passwords
- Use **strong passwords** in production
- Change default passwords (`procurement_password`)
- Store securely (use password manager)

### 📧 Email Verification
If you want **mandatory email verification** for new users:
```bash
# Add to .env or settings.py
ACCOUNT_EMAIL_VERIFICATION=mandatory  # optional, mandatory, or none
```

### 🌐 Allowed Hosts
In production, **update ALLOWED_HOSTS**:
```bash
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com
```

---

## ✅ Checklist Before Going to Production

- [ ] Set `DEBUG=False`
- [ ] Generate new `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Use strong database password
- [ ] Configure real email backend (SMTP/SendGrid/SES)
- [ ] Enable security settings (HTTPS, HSTS, etc.)
- [ ] Set up SSL certificate
- [ ] Use environment-specific .env files
- [ ] Never commit .env to version control
- [ ] Set up database backups
- [ ] Configure monitoring/logging

---

## 🧪 Testing Your Configuration

### Test Database Connection
```bash
docker-compose exec web python manage.py dbshell
```

### Test Redis Connection
```bash
docker-compose exec redis redis-cli ping
# Should return: PONG
```

### Test Email
```bash
docker-compose exec web python manage.py shell
```
```python
from django.core.mail import send_mail
send_mail(
    'Test Subject',
    'Test message.',
    'from@example.com',
    ['to@example.com'],
)
# Check console output for the email
```

### Test Celery
```bash
docker-compose exec web python manage.py shell
```
```python
from procurement_system.celery import debug_task
debug_task.delay()
# Check celery worker logs
```

---

## 📚 Additional Resources

- [Django Settings Best Practices](https://docs.djangoproject.com/en/5.1/topics/settings/)
- [12-Factor App](https://12factor.net/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)

---

## 🆘 Troubleshooting

### "Database connection failed"
- Check `DB_HOST`, `DB_PORT`, `DB_NAME`
- Ensure PostgreSQL is running
- For Docker: use service name `db`
- For local: use `localhost`

### "Redis connection refused"
- Check `REDIS_HOST` and `REDIS_PORT`
- Ensure Redis is running
- For Docker: use service name `redis`
- For local: use `localhost`

### "Invalid HTTP_HOST header"
- Update `ALLOWED_HOSTS` in .env
- Include all domains you'll use

### "Emails not sending"
- Check `EMAIL_BACKEND` setting
- For Gmail: use app-specific password
- Check console output (console backend)

---

**Your `.env` file is ready to use! Start the system with:**

```bash
docker-compose up
```

🎉 **All configured!**

