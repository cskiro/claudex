---
paths:
  - "**/auth/**/*"
  - "**/security/**/*"
  - "**/middleware/**/*"
  - "**/*.env*"
  - "**/secrets/**/*"
  - "**/config/**/*"
  - "**/*password*"
  - "**/*credential*"
  - "**/crypto/**/*"
  - "**/session/**/*"
  - "**/token/**/*"
---

<!-- Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync -->

# Security Standards (Detailed)

Loads for: Auth, security, middleware, config, and credential-related files.

---

## Authentication & Authorization

- MFA for all admin accounts
- OAuth 2.0/OIDC (not custom auth)
- Short-lived tokens (15-60 minutes)
- bcrypt/argon2 for password hashing
- Rate limiting on login endpoints

---

## Input Validation (OWASP Top 10)

| Vulnerability | Prevention |
|---------------|------------|
| SQL Injection | Parameterized queries |
| XSS | Sanitize HTML, CSP headers |
| Command Injection | No shell exec with user input |
| Path Traversal | Validate paths, use absolute |
| CSRF | Anti-CSRF tokens |
| Insecure Deserialization | Validate/sanitize before deserialize |

---

## Data Protection

- Encryption at rest (AES-256)
- TLS 1.2+ for all traffic
- Redact PII from logs
- GDPR deletion support
- Minimize data collection

---

## Secrets Management

- NEVER hardcode secrets in code
- Use environment variables or secret managers
- Rotate secrets regularly
- Different secrets per environment
- Audit secret access

**Bad**:
```python
API_KEY = "sk-1234567890abcdef"  # NEVER DO THIS
```

**Good**:
```python
import os
API_KEY = os.environ["API_KEY"]
```

---

## Secure Coding Patterns

### Password Handling
```python
from argon2 import PasswordHasher

ph = PasswordHasher()
hash = ph.hash(password)
ph.verify(hash, password)  # Raises on mismatch
```

### SQL Queries
```python
# GOOD - Parameterized
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# BAD - String interpolation
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### File Paths
```python
import os

# GOOD - Validate path
base_dir = "/app/uploads"
requested = os.path.abspath(os.path.join(base_dir, user_input))
if not requested.startswith(base_dir):
    raise ValueError("Path traversal detected")
```

---

## Security Headers

Required HTTP headers:
```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

---

## Pre-Production Checklist

- [ ] No hardcoded secrets
- [ ] TLS 1.2+ enforced
- [ ] MFA for admin accounts
- [ ] Input validation on all entry points
- [ ] Dependency vulnerabilities resolved
- [ ] SAST scan passed
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Logging excludes sensitive data
