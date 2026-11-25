# Prompts exactos para la demo

Cópialos tal cual. Están pensados para gastar pocos créditos y dar resultados predecibles.
Modelo: **Auto** en todos.

---

## 1. Rompehielos de steering (≈1 crédito)

Sin steering:
```
Explícame en una frase qué es Amazon DynamoDB.
```

Con steering (escribe `#` y elige `estilo-argentino`):
```
#estilo-argentino Explícame en una frase qué es Amazon DynamoDB.
```

## 2. Memoria (≈1 crédito)

```
Recuerda esto para mis próximos proyectos: siempre uso node --test para pruebas, nunca Jest.
```
Abre una sesión nueva (`+` en el chat) y pregunta:
```
¿Con qué herramienta escribo las pruebas en este proyecto?
```
Señala en pantalla el aviso de memoria accedida en el chat.

## 3. Steering de empresa (0 créditos)

En la terminal integrada de Kiro:
```bash
cp kit/steering-empresa/*.md .kiro/steering/
```
Abre `security.md` en pantalla y lee 2 o 3 reglas en voz alta.

## 4. Spec (≈4–7 créditos)

Abre el panel de Kiro → **Spec** → pega:
```
Construye "Kiro Live Board": una app web serverless para que los asistentes de una charla se registren escaneando un QR desde el celular, y un tablero en vivo para el proyector.

- Formulario móvil: nombre, correo corporativo, empresa, rol, interés principal y checkbox de consentimiento obligatorio.
- Tablero en /board que se actualiza cada 3 segundos: total de registrados, barras por interés y los últimos 12 en llegar (solo primer nombre y empresa, nunca correos).
- Una Lambda, una tabla DynamoDB y API Gateway HTTP API, desplegado con SAM.

Mantén el plan en máximo 5 tareas, sin subtareas.
```

**Requisito del público** (pídele a alguien del público uno y, si no sale nada, usa este):
```
Agrega un requisito: si un correo ya está registrado, no se duplica y se le muestra un mensaje amable.
```

## 5. Ejecutar tareas (≈8–15 créditos)

Usa siempre el botón **Start task** dentro de `tasks.md`, no el chat.

## 6. Deploy (0 créditos si lo corres tú en la terminal)

En la terminal integrada:
```bash
sam build && sam deploy
```
Copia `FormUrl` y `BoardUrl` de los Outputs.

## 7. Playwright MCP (≈3–5 créditos)

Reemplaza `<FormUrl>` por la URL del Output:
```
Usa Playwright para abrir <FormUrl>, llenar el formulario con datos de prueba (nombre "Ana Demo", correo ana@demo.pe, empresa "Demo SAC", interés "Desarrollo con IA", consentimiento marcado) y enviarlo. Luego abre <FormUrl>board y confirma que aparece "Ana". Toma una captura al final.
```
Después abre `BoardUrl` en pantalla completa: el público escanea el QR y se registra.
