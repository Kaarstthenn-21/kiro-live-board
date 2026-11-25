---
inclusion: always
---

# Stack técnico y convenciones

## Arquitectura (serverless en AWS)
- **API**: Amazon API Gateway HTTP API.
- **Cómputo**: una sola función AWS Lambda en Node.js 24 (ESM, archivos `.mjs`).
- **Datos**: una sola tabla Amazon DynamoDB, modo on-demand (PAY_PER_REQUEST).
- **Frontend**: HTML + CSS + JavaScript vanilla servido por la misma Lambda. Sin frameworks ni build.
- **Infraestructura como código**: AWS SAM (`template.yaml`). Región por defecto `us-east-1`.

## Convenciones de código
- Usar AWS SDK v3 (incluido en el runtime de Lambda, no se agrega a `package.json`).
- Sin dependencias npm externas salvo que sea imprescindible.
- Nombres de variables y funciones en inglés; textos de UI en español.
- Funciones pequeñas y puras para la lógica de validación, para poder testearlas.
- Respuestas HTTP en JSON con códigos correctos: 201 creado, 400 validación, 409 duplicado, 500 error.

## Pruebas
- Tests unitarios con `node --test` (runner nativo, sin Jest).
- Las pruebas de UI se hacen con el MCP de Playwright.

## Qué NO hacer
- No crear más de una Lambda ni más de una tabla.
- No usar contenedores, EC2 ni servidores.
- No agregar Cognito ni autenticación: la app es pública por diseño.
