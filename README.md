# Kiro Live Board

Sistema serverless de registro de eventos con dashboard en tiempo real, construido con AWS SAM.

## 🎯 Características

- **3 Vistas Frontend**:
  - `qr.html` - Pantalla de proyección con código QR
  - `registration.html` - Formulario de registro móvil
  - `board.html` - Dashboard en tiempo real con estadísticas

- **Backend Serverless**:
  - Lambda (Python 3.12) para lógica de negocio
  - DynamoDB para almacenamiento de datos
  - API Gateway HTTP API para endpoints REST

- **Infraestructura de Hosting**:
  - S3 para archivos estáticos
  - CloudFront para distribución global con HTTPS
  - Generación automática de código QR

## 🚀 Despliegue

### 1. Desplegar Backend

```bash
# Construir la aplicación
sam build

# Desplegar (primera vez)
sam deploy --guided

# Desplegar (subsecuentes)
sam deploy
```

Durante `sam deploy --guided`:
- Stack Name: `kiro-live-board`
- AWS Region: tu región preferida (ej: `us-east-1`)
- Confirmar cambios: Y
- Permitir creación de rol IAM: Y
- Guardar configuración: Y

### 2. Desplegar Frontend

Después de que el backend esté desplegado:

```bash
# Ejecutar script de deployment
./deploy-frontend.sh
```

Este script:
1. Obtiene las URLs del stack de CloudFormation
2. Actualiza los archivos HTML con la URL de la API
3. Sube los archivos a S3
4. Invalida el cache de CloudFront

### 3. Obtener URLs

```bash
# Ver todas las URLs del stack
aws cloudformation describe-stacks \
    --stack-name kiro-live-board \
    --query 'Stacks[0].Outputs' \
    --output table
```

O consulta los outputs del deployment:
- **QrCodeUrl**: Pantalla QR para proyectar
- **RegistrationUrl**: Formulario de registro
- **DashboardUrl**: Dashboard en tiempo real

## 📋 Uso

### Para el Organizador del Evento:

1. **Proyecta la pantalla QR**:
   ```
   https://<cloudfront-domain>/qr.html
   ```

2. **Monitorea el dashboard** en otra pantalla:
   ```
   https://<cloudfront-domain>/board.html
   ```

### Para los Asistentes:

1. Escanean el código QR con su cámara
2. Completan el formulario de registro
3. Son redirigidos automáticamente al dashboard

## 🎨 Colores Escala24x7

El diseño utiliza la paleta de colores corporativa de Escala24x7:

- **Primario**: `#00D9B4` (turquesa/verde brillante)
- **Oscuro**: `#0A1E2E` (azul marino oscuro)
- **Secundario**: `#1A3A52` (azul marino medio)
- **Texto**: `#FFFFFF` (blanco)

## 🧪 Pruebas Locales

### Backend Local

```bash
# Iniciar API local
sam local start-api

# Probar registro
curl -X POST http://localhost:3000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "company": "Acme Corp",
    "role": "Developer",
    "interest": "AI & Machine Learning",
    "consent": true
  }'

# Probar dashboard
curl http://localhost:3000/board
```

### Frontend Local

```bash
cd frontend
python3 -m http.server 8000

# Abrir en navegador:
# http://localhost:8000/qr.html
# http://localhost:8000/registration.html
# http://localhost:8000/board.html
```

## 📁 Estructura del Proyecto

```
kiro-live-board/
├── template.yaml              # SAM template (infraestructura)
├── src/
│   ├── app.py                # Lambda handler
│   ├── test_lambda.py        # Unit tests
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── qr.html              # Pantalla de proyección con QR
│   ├── registration.html     # Formulario de registro
│   └── board.html           # Dashboard en tiempo real
├── deploy-frontend.sh        # Script de deployment
└── README.md                # Este archivo
```

## 🔧 Configuración

### Variables de Entorno (Lambda)

Configuradas automáticamente por SAM:
- `TABLE_NAME`: Nombre de la tabla DynamoDB
- `GSI_NAME`: Nombre del índice secundario global

### Endpoints API

- `POST /register`: Registrar nuevo asistente
- `GET /board`: Obtener datos del dashboard

### Tabla DynamoDB

- **Clave primaria**: `email` (String)
- **GSI**: `TimestampIndex` (gsiPK, timestamp)
- **Modo de facturación**: On-demand

## 📊 Monitoreo

### CloudWatch Logs

```bash
# Ver logs de Lambda
sam logs -n RegistrationFunction --tail

# Ver logs de API Gateway
aws logs tail /aws/apigateway/kiro-live-board-HttpApi --follow
```

### Métricas

- Lambda invocations, errors, duration
- DynamoDB read/write capacity, throttles
- API Gateway 4xx/5xx errors, latency
- CloudFront requests, cache hit rate

## 🗑️ Limpieza

```bash
# Eliminar archivos del bucket S3
aws s3 rm s3://$(aws cloudformation describe-stacks --stack-name kiro-live-board --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucketName`].OutputValue' --output text) --recursive

# Eliminar stack
sam delete
```

## 🔐 Seguridad

- ✅ HTTPS enforced (CloudFront)
- ✅ S3 bucket privado (acceso solo vía CloudFront OAI)
- ✅ Emails nunca se muestran en el dashboard
- ✅ Validación de inputs en Lambda
- ✅ CORS configurado correctamente
- ✅ Encriptación en reposo (S3, DynamoDB)

## 📝 Requisitos

- AWS CLI configurado
- SAM CLI instalado
- Python 3.12
- Permisos de AWS: CloudFormation, Lambda, DynamoDB, API Gateway, S3, CloudFront

## 🤝 Soporte

Para problemas o preguntas, revisa:
1. CloudWatch Logs para errores de Lambda
2. API Gateway access logs
3. CloudFront distribution status

## 📄 Licencia

MIT License - ver LICENSE file para detalles
