---
name: api-security
description: >
  Audita y refuerza la seguridad de APIs REST y GraphQL.
  Usa cuando el usuario desarrolle endpoints, configure auth,
  o revise código backend por vulnerabilidades comunes.
allowed-tools:
  - Read
  - Grep
  - Edit
  - Write
  - Bash
---

# API Security

## Cuándo usar

- Revisión de código de endpoints nuevos o modificados.
- Configuración de autenticación/autorización.
- Respuesta a reportes de seguridad o auditorías.

## Reglas

### Autenticación

- NUNCA implementes tu propio crypto. Usa librerías probadas (bcrypt, argon2, JWT con librerías estándar).
- Tokens JWT: usar `HS256` solo si el secreto es ≥256 bits y rotado. Preferir `RS256` para microservicios.
- Expiración de tokens de acceso: ≤15 minutos. Refresh tokens: ≤7 días con rotación.

### Autorización

- Principio de mínimo privilegio: cada endpoint debe verificar el rol/permiso mínimo necesario.
- NUNCA confíes en el `user_id` del body/query; sácalo del token verificado.
- Implementa rate limiting por usuario + IP.

### Input validation

- Toda entrada externa es hostil hasta demostrado lo contrario.
- Usa schemas (Zod, Pydantic, Joi) para validar y sanitizar antes de tocar lógica de negocio.
- SQL injection: usar ORM/parametrización. NUNCA concatenar strings en queries.

### Headers de seguridad

- `Content-Security-Policy` para APIs que sirven HTML.
- `Strict-Transport-Security` (HSTS) en producción.
- `X-Content-Type-Options: nosniff`.

## Anti-patrones

1. **Secrets hardcodeados**
   - Solución: Variables de entorno + gestor de secrets (HashiCorp Vault, AWS Secrets Manager).

2. **Error messages informativos para atacantes**
   - Solución: Logs detallados internos, mensajes genéricos al cliente ("Credenciales inválidas").

3. **CORS abierto (`*`) en producción**
   - Solución: Lista blanca de orígenes explícita.

## Plantilla — Checklist de endpoint

```markdown
## Seguridad de `POST /api/v1/resource`

- [ ] Autenticación requerida
- [ ] Autorización verificada (¿el usuario puede crear en este scope?)
- [ ] Rate limiting aplicado
- [ ] Input validado con schema
- [ ] Output no expone datos sensibles
- [ ] Logs de auditoría generados
- [ ] Tests de seguridad incluidos
```

## Checklist global

- [ ] ¿Todos los endpoints tienen autenticación?
- [ ] ¿Los secrets están fuera del código?
- [ ] ¿Hay rate limiting configurado?
- [ ] ¿Los logs no contienen PII ni passwords?
