# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.5.x   | :white_check_mark: |
| 1.4.x   | :white_check_mark: |
| < 1.4   | :x:                |

## Reporting a Vulnerability

We take the security of our software seriously. If you have discovered a security vulnerability in this project, please report it responsibly by following these guidelines:

### How to Report

1. **Do not open a public issue** for security vulnerabilities
2. Send an email to: **contato@estoicapi.com** (if this email is not available, create a GitHub issue with minimal details and we'll provide a secure contact method)
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if you have one)

### What to Expect

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide an estimated timeline for a fix within 72 hours
- We will notify you when the vulnerability has been fixed
- We will credit you in our security advisory (unless you prefer to remain anonymous)

### Security Best Practices

When using this API:

1. **Rate Limiting**: The API includes built-in rate limiting to prevent abuse
2. **CORS Configuration**: Configure CORS settings appropriately for your production environment
3. **HTTPS**: Always use HTTPS in production environments
4. **Input Validation**: All inputs are validated using Pydantic models
5. **Security Headers**: The API includes security headers (CSP, X-Frame-Options, etc.)

### Responsible Disclosure

We follow responsible disclosure practices:

- Security fixes will be released as soon as possible
- We will coordinate with you on the disclosure timeline
- We will publicly acknowledge your contribution (if desired)

## Security Considerations

### Production Deployment

- Set `APP_ENV=production` in production environments
- Configure `ALLOWED_ORIGINS` to restrict CORS to trusted domains
- Use environment variables for sensitive configuration
- Deploy behind a reverse proxy (nginx, Cloudflare, etc.)
- Enable logging and monitoring
- Keep dependencies updated

### Known Security Features

- **Rate Limiting**: Built-in protection against brute force and DoS attacks
- **CORS Protection**: Configurable cross-origin resource sharing
- **Security Headers**: Content Security Policy, X-Frame-Options, X-Content-Type-Options
- **Input Validation**: Strict type checking with Pydantic
- **No User Data Storage**: The API doesn't store personal user data

Thank you for helping keep our project safe!