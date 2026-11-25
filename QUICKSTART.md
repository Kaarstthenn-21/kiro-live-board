# 🚀 Inicio Rápido - Kiro Live Board v2.0

## Deployment en 3 Pasos

### 1️⃣ Desplegar Backend + Infraestructura

```bash
sam build && sam deploy
```

**Tiempo estimado**: 5-10 minutos (creación de CloudFront toma tiempo)

**Recursos creados**:
- Lambda function (Python 3.12)
- DynamoDB table
- API Gateway HTTP API
- S3 Bucket (frontend)
- CloudFront Distribution
- CloudWatch Logs

### 2️⃣ Desplegar Frontend

```bash
./deploy-frontend.sh
```

**Esto hace**:
- Obtiene URLs del stack
- Actualiza API URLs en HTML files
- Sube archivos a S3
- Invalida cache de CloudFront

**Tiempo estimado**: 1-2 minutos

### 3️⃣ Obtener URLs del Evento

```bash
aws cloudformation describe-stacks \
    --stack-name kiro-live-board \
    --query 'Stacks[0].Outputs[?OutputKey==`QrCodeUrl` || OutputKey==`DashboardUrl`].{Key:OutputKey,Value:OutputValue}' \
    --output table
```

**Output esperado**:
```
-----------------------------------------------------------------
|                      DescribeStacks                           |
+---------------+-----------------------------------------------+
|      Key      |                    Value                      |
+---------------+-----------------------------------------------+
|  QrCodeUrl    |  https://d123abc.cloudfront.net/qr.html      |
|  DashboardUrl |  https://d123abc.cloudfront.net/board.html   |
+---------------+-----------------------------------------------+
```

---

## 📺 Uso en Evento

### Para el Organizador:

**Proyectar en pantalla grande**:
```
https://d123abc.cloudfront.net/qr.html
```
- Presiona F11 para pantalla completa
- Deja esta vista proyectada durante todo el evento

**Monitorear en laptop/segunda pantalla**:
```
https://d123abc.cloudfront.net/board.html
```
- Se actualiza automáticamente cada 3 segundos
- Muestra total de registrados, gráficas, últimos 12

### Para los Asistentes:

1. Escanean el QR code con la cámara de su móvil
2. Se abre `registration.html` automáticamente
3. Completan el formulario
4. Son redirigidos a `board.html` para ver estadísticas

---

## ⚡ Comandos Útiles

### Ver logs de Lambda en tiempo real:
```bash
sam logs -n RegistrationFunction --tail
```

### Ver datos en DynamoDB:
```bash
aws dynamodb scan --table-name KiroLiveBoardAttendees --max-items 10
```

### Invalidar cache de CloudFront manualmente:
```bash
DIST_ID=$(aws cloudfront list-distributions --query "DistributionList.Items[?Comment=='CloudFront distribution for kiro-live-board Kiro Live Board'].Id" --output text)
aws cloudfront create-invalidation --distribution-id $DIST_ID --paths "/*"
```

### Actualizar solo frontend (sin rebuild backend):
```bash
./deploy-frontend.sh
```

---

## 🧪 Testing Local (Desarrollo)

### Backend local:
```bash
sam local start-api
```

Luego abre: http://localhost:3000/board

### Frontend local:
```bash
cd frontend
python3 -m http.server 8000
```

Luego abre: http://localhost:8000/qr.html

**Nota**: Actualiza las URLs de API en los HTML files para apuntar a `http://localhost:3000`

---

## 🗑️ Limpiar Todo

```bash
# Eliminar archivos del bucket S3
BUCKET=$(aws cloudformation describe-stacks --stack-name kiro-live-board --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucketName`].OutputValue' --output text)
aws s3 rm s3://$BUCKET --recursive

# Eliminar stack completo
sam delete --stack-name kiro-live-board
```

---

## 🆘 Troubleshooting

### "Stack with name kiro-live-board does not exist"
El stack aún no ha sido desplegado. Ejecuta `sam deploy --guided` primero.

### "AccessDenied" al subir a S3
Verifica que tu usuario de AWS tenga permisos de S3 y CloudFront.

### QR code no aparece en qr.html
Revisa la consola del navegador. La biblioteca QRCode.js debe cargarse desde CDN.

### Los registros no aparecen en el dashboard
1. Verifica que la API esté respondiendo: `curl <API_URL>/board`
2. Revisa logs de Lambda: `sam logs -n RegistrationFunction --tail`
3. Verifica que DynamoDB tenga datos

### CloudFront tarda mucho en crear
Es normal. La primera creación de una distribution puede tomar 15-20 minutos.

---

## 📞 Soporte

- Revisa `CHANGES.md` para ver todos los cambios de v2.0
- Revisa `README.md` para documentación completa
- Logs de Lambda: CloudWatch Logs
- Logs de API Gateway: CloudWatch Logs

---

**Versión**: 2.0  
**Stack Name**: `kiro-live-board`  
**Región**: us-east-1 (o la que configuraste)
