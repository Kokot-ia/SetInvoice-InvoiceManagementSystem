# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please report it responsibly:

1. **DO NOT** open a public issue
2. Email the maintainer directly with details
3. Allow reasonable time for a fix before public disclosure

## Security Best Practices

### For Development

#### 1. Environment Variables

**NEVER commit sensitive data to version control:**

- ✅ Use `.env` file for all secrets
- ✅ Keep `.env` in `.gitignore`
- ✅ Use `.env.example` as a template (without real values)
- ❌ Never hardcode passwords, API keys, or secrets in code

**Example `.env` structure:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST_PASSWORD=your-email-password
```

#### 2. Secret Key Management

Generate a strong Django secret key:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

- Minimum 50 characters
- Use random, unpredictable values
- Rotate regularly (especially after suspected compromise)
- Never reuse across environments

#### 3. Password Security

**For Admin/User Accounts:**
- Minimum 8 characters (enforced by Django validators)
- Mix of uppercase, lowercase, numbers, and symbols
- Avoid common passwords (Django checks against common password list)
- Use password managers for strong, unique passwords

**Password Hashing:**
- System uses Argon2 (if installed) or PBKDF2
- Passwords are never stored in plain text
- Password reset uses secure token-based system

#### 4. Database Security

**Development:**
- SQLite is fine for development
- Keep `db.sqlite3` in `.gitignore`
- Never commit database files with real user data

**Production:**
- Use PostgreSQL or MySQL
- Enable SSL/TLS for database connections
- Use strong database passwords
- Restrict database access to application server only
- Regular backups with encryption

### For Production Deployment

#### 1. Django Settings

Update `config/settings.py` or `.env`:

```env
DEBUG=False
SECRET_KEY=<new-production-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

#### 2. HTTPS/SSL

- **REQUIRED** for production
- Obtain SSL certificate (Let's Encrypt is free)
- Configure web server (Nginx/Apache) for HTTPS
- Enable HSTS (HTTP Strict Transport Security)

The following settings are automatically enabled when `DEBUG=False`:

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

#### 3. Security Headers

Already configured in `config/settings.py`:

- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-Content-Type-Options: nosniff` - Prevents MIME sniffing
- `X-XSS-Protection: 1; mode=block` - XSS protection
- `Referrer-Policy: same-origin` - Controls referrer information

#### 4. CSRF Protection

- Enabled by default on all forms
- Use `{% csrf_token %}` in all POST forms
- AJAX requests must include CSRF token

#### 5. Session Security

Current configuration:

```python
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
```

For production, sessions are secure (HTTPS only).

#### 6. Email Security

**Gmail Configuration:**
- Enable 2-Factor Authentication
- Use App Passwords (not your main password)
- Never commit email credentials

**SendGrid/Other SMTP:**
- Use API keys instead of passwords where possible
- Rotate API keys regularly
- Monitor for unauthorized usage

#### 7. File Upload Security

If implementing file uploads:

- Validate file types and extensions
- Limit file sizes
- Scan for malware
- Store uploads outside web root
- Use unique, random filenames

#### 8. Rate Limiting

The system includes basic rate limiting middleware:

- Login attempts are limited
- Account lockout after failed attempts
- Protects against brute force attacks

#### 9. SQL Injection Prevention

- **Always** use Django ORM (never raw SQL)
- If raw SQL is necessary, use parameterized queries
- Never concatenate user input into SQL

**Good:**
```python
User.objects.filter(email=user_email)
```

**Bad:**
```python
cursor.execute(f"SELECT * FROM users WHERE email='{user_email}'")
```

#### 10. XSS Prevention

- Django auto-escapes template variables
- Use `|safe` filter only for trusted content
- Sanitize user input before display

### Access Control

#### Role-Based Permissions

- Admin: Full access
- Manager: Business operations
- User: Limited access
- Viewer: Read-only

**Enforce permissions in views:**
```python
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import role_required

@login_required
@role_required(['Admin', 'Manager'])
def sensitive_view(request):
    # Only Admin and Manager can access
    pass
```

### Secure Coding Practices

#### 1. Input Validation

- Validate all user input
- Use Django forms for automatic validation
- Sanitize data before processing

#### 2. Error Handling

- Never expose stack traces to users (set `DEBUG=False`)
- Log errors securely
- Use custom error pages (400, 403, 404, 500)

#### 3. Logging

- Log security events (failed logins, permission denials)
- Protect log files (don't commit to version control)
- Rotate logs regularly

#### 4. Dependencies

- Keep Django and packages updated
- Run `pip list --outdated` regularly
- Monitor security advisories
- Use `pip-audit` to check for vulnerabilities:

```bash
pip install pip-audit
pip-audit
```

### Deployment Checklist

Before deploying to production:

- [ ] `DEBUG=False` in production
- [ ] Strong, unique `SECRET_KEY`
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] HTTPS/SSL enabled
- [ ] Database using PostgreSQL with strong password
- [ ] Email configured with secure credentials
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Media files stored securely
- [ ] Backups configured and tested
- [ ] Monitoring and logging enabled
- [ ] Security headers verified
- [ ] Dependencies updated
- [ ] `.env` file secured (not in version control)
- [ ] Admin scripts with hardcoded passwords removed
- [ ] Rate limiting configured
- [ ] Error pages customized (no debug info)

### Regular Maintenance

#### Weekly
- Review access logs for suspicious activity
- Check for failed login attempts

#### Monthly
- Update dependencies
- Review user accounts and permissions
- Test backup restoration

#### Quarterly
- Security audit
- Rotate secrets and API keys
- Review and update security policies

### Common Vulnerabilities to Avoid

#### 1. Hardcoded Credentials

❌ **Bad:**
```python
admin_password = 'admin123'
EMAIL_HOST_PASSWORD = 'mypassword'
```

✅ **Good:**
```python
admin_password = os.getenv('ADMIN_PASSWORD')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

#### 2. Debug Mode in Production

❌ **Bad:**
```python
DEBUG = True  # In production
```

✅ **Good:**
```python
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

#### 3. Weak Passwords

❌ **Bad:**
- admin/admin
- password123
- 12345678

✅ **Good:**
- Use password generators
- Minimum 12 characters for admin accounts
- Mix of character types

#### 4. Exposed Secret Keys

❌ **Bad:**
- Committing `.env` to GitHub
- Hardcoding `SECRET_KEY` in settings.py
- Sharing secrets in chat/email

✅ **Good:**
- Use environment variables
- Use secret management tools
- Rotate keys regularly

### Security Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Releases](https://www.djangoproject.com/weblog/)
- [Python Security Advisories](https://python.org/dev/security/)

### Incident Response

If a security breach occurs:

1. **Immediate Actions:**
   - Take affected systems offline if necessary
   - Change all passwords and secrets
   - Review access logs

2. **Investigation:**
   - Determine scope of breach
   - Identify vulnerability
   - Document timeline

3. **Remediation:**
   - Fix vulnerability
   - Update security measures
   - Notify affected users (if applicable)

4. **Post-Incident:**
   - Update security policies
   - Implement additional safeguards
   - Train team on lessons learned

---

## Contact

For security concerns, please contact the project maintainer.

**Remember: Security is everyone's responsibility!** 🔒
