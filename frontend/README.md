# Kiro Live Board - Frontend

Este directorio contiene los archivos HTML estáticos para el sistema de registro de eventos Kiro Live Board.

## Archivos

- `board.html` - Panel de visualización en tiempo real que muestra las estadísticas de asistentes (producción)
- `board-demo.html` - Versión demo con datos simulados (para pruebas sin backend)
- `board-test.html` - Página de pruebas con checklist de implementación
- `README.md` - Esta documentación
- `TASK5_VERIFICATION.md` - Documento de verificación detallado
- `IMPLEMENTATION_COMPLETE.md` - Resumen de implementación completa

## Vista Previa Rápida

**¿Quieres ver cómo se ve el panel antes de desplegar el backend?**

Simplemente abre `board-demo.html` en tu navegador. Este archivo incluye:
- Datos mock que simulan registros reales
- Actualización automática cada 3 segundos con nuevos "asistentes"
- Visualización completa de todas las características

```bash
# Opción 1: Abrir directamente
open frontend/board-demo.html

# Opción 2: Con servidor HTTP
cd frontend
python3 -m http.server 8000
# Abre http://localhost:8000/board-demo.html
```

## Configuración para Producción

### Paso 1: Desplegar el Backend

Primero, despliega la infraestructura AWS usando SAM:

```bash
sam build
sam deploy --guided
```

Después del despliegue, SAM mostrará la URL de tu API Gateway, por ejemplo:
```
Outputs:
  ApiUrl: https://abc123xyz.execute-api.us-east-1.amazonaws.com
```

### Paso 2: Configurar la URL de la API

Abre `board.html` en tu editor de texto y reemplaza `YOUR_API_GATEWAY_URL_HERE` con la URL de tu API Gateway:

```javascript
// Busca esta línea en board.html:
const API_BASE_URL = 'YOUR_API_GATEWAY_URL_HERE';

// Reemplázala con tu URL (sin barra final):
const API_BASE_URL = 'https://abc123xyz.execute-api.us-east-1.amazonaws.com';
```

### Paso 3: Servir los Archivos

Puedes servir estos archivos de varias maneras:

#### Opción A: Servidor HTTP Simple (Desarrollo)

```bash
# Python 3
python3 -m http.server 8000

# Node.js (requiere instalación global de http-server)
npx http-server -p 8000
```

Luego abre `http://localhost:8000/board.html` en tu navegador.

#### Opción B: S3 Static Website Hosting (Producción)

1. Crea un bucket S3:
```bash
aws s3 mb s3://kiro-live-board-frontend
```

2. Configura el bucket para hosting web estático:
```bash
aws s3 website s3://kiro-live-board-frontend --index-document board.html
```

3. Sube los archivos:
```bash
aws s3 sync . s3://kiro-live-board-frontend --exclude "README.md"
```

4. Configura la política de bucket para acceso público (ajusta según tus necesidades de seguridad).

#### Opción C: Abrir Directamente en el Navegador

Simplemente abre `board.html` en tu navegador. Sin embargo, esto puede causar problemas de CORS dependiendo de tu configuración de API Gateway.

## Uso del Panel de Visualización (board.html)

El panel se actualiza automáticamente cada 3 segundos y muestra:

- **Total de Asistentes**: Número total de registros en el sistema
- **Distribución por Interés**: Gráfico de barras horizontales mostrando la cantidad de asistentes por categoría de interés
- **Últimos Registros**: Los 12 asistentes más recientes (solo nombre y empresa, sin emails)

### Características de Privacidad

- ✅ Solo se muestra el primer nombre del asistente (no el nombre completo)
- ✅ Los correos electrónicos corporativos NUNCA se muestran en el panel
- ✅ Solo se muestra la empresa junto al primer nombre

### Estado Vacío

Si no hay registros, el panel mostrará:
- Contador en 0
- Mensaje "No hay datos de intereses aún" en el área de gráficos
- Mensaje "No hay registros aún" en la sección de asistentes recientes

## Proyección en Eventos

Para proyectar el panel durante un evento en vivo:

1. Abre `board.html` en un navegador en modo pantalla completa (F11 o Cmd+Shift+F en Mac)
2. Conecta el computador al proyector
3. El panel se actualizará automáticamente cada 3 segundos
4. El timestamp de última actualización aparece al final de la página

## Solución de Problemas

### El panel muestra "Error conectando con el servidor"

- Verifica que la URL de la API Gateway esté configurada correctamente
- Asegúrate de que el backend esté desplegado y funcionando
- Verifica que CORS esté habilitado en la API Gateway (el template SAM ya lo configura)

### Los datos no se actualizan

- Verifica la consola del navegador (F12) para ver errores
- Asegúrate de que el endpoint `/board` del Lambda esté funcionando correctamente
- Verifica que haya conexión a internet

### El gráfico no se muestra

- Verifica que Chart.js se esté cargando correctamente desde el CDN
- Revisa la consola del navegador para errores de JavaScript

## Tecnologías Utilizadas

- **HTML5/CSS3**: Estructura y estilos
- **JavaScript (Vanilla)**: Lógica de actualización y renderizado
- **Chart.js 4.4.1**: Gráficos de barras para distribución de intereses
- **Fetch API**: Llamadas HTTP al backend

## Personalización

### Cambiar el Intervalo de Actualización

Modifica la constante `REFRESH_INTERVAL` en `board.html`:

```javascript
const REFRESH_INTERVAL = 3000; // 3 segundos (valor en milisegundos)
```

### Cambiar Colores y Estilos

Los estilos CSS están embebidos en la sección `<style>` de cada archivo HTML. Puedes modificarlos directamente.

### Cambiar el Número de Asistentes Recientes

Por defecto se muestran 12 asistentes recientes (según los requisitos). Si deseas cambiar este número, modifica la línea en la función `renderRecentAttendees`:

```javascript
const attendeesToShow = recentAttendees.slice(0, 12); // Cambiar 12 por el número deseado
```

**Nota**: El Lambda también limita los resultados a 12 en el backend, así que necesitarías modificar ambos lugares.

## Validación de Requisitos

Este archivo valida los siguientes requisitos del documento de requisitos:

- ✅ **3.1**: Panel accesible vía URL
- ✅ **3.2**: Muestra el total de asistentes registrados
- ✅ **3.3**: Muestra gráficos de barras agrupados por interés
- ✅ **3.4**: Muestra los 12 registros más recientes con solo nombre y empresa
- ✅ **3.5**: Actualización automática cada 3 segundos
- ✅ **3.6**: NUNCA muestra correos electrónicos corporativos
- ✅ **3.7**: Maneja el estado vacío (cero asistentes)

## Seguridad

- El código incluye escape de HTML para prevenir XSS
- Se valida que los emails nunca aparezcan en los datos mostrados
- Los datos se obtienen solo del backend autorizado (misma configuración CORS)
