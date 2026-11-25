---
inclusion: always
---

# Seguridad y datos personales

Estas reglas aplican a todo el código, specs e infraestructura del proyecto.

## Secretos
- Nunca escribir access keys, contraseñas ni tokens en el código o en la plantilla SAM.
- La configuración va en variables de entorno de la Lambda (por ejemplo `TABLE_NAME`).

## IAM de mínimo privilegio
- La Lambda solo puede hacer `dynamodb:PutItem` y `dynamodb:Scan` sobre su propia tabla. Usar las policies de SAM (`DynamoDBCrudPolicy` o una policy explícita acotada), nunca `*`.

## Datos personales
- Validar y sanear todas las entradas en el backend (longitud máxima, formato de correo, lista cerrada de intereses).
- Escapar todo texto antes de insertarlo en el HTML (prevenir XSS). Nunca usar `innerHTML` con datos del usuario.
- No registrar correos ni datos personales en los logs de CloudWatch. Loguear solo IDs o conteos.
- El endpoint público de estadísticas nunca devuelve correos.
- Guardar la fecha y el texto del consentimiento junto con cada registro.

## Contexto regulatorio
- Pensar el diseño como si el cliente fuera un banco o una telco en Perú: datos personales mínimos, consentimiento explícito y trazabilidad (Ley N.º 29733 de Protección de Datos Personales).
