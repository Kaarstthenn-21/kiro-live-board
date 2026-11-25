# Guion: Kiro fast track (45 min de demo)

Objetivo: que el público vea en vivo cómo una idea pasa a una app en AWS con specs, reglas de empresa y pruebas automáticas, y que **se registre** en esa app. Esa lista es tu pipeline de leads.

Presupuesto: **~20–35 créditos en Auto**, con margen sobre 50.

| Min | Bloque | Qué haces | Qué dices (idea clave) | Créditos |
|---|---|---|---|---|
| 0–2 | Teaser | Proyectas el `/board` de la versión de respaldo ya desplegada, con el QR. Pides que se registren. | "Esta app la vamos a construir de cero en los próximos 40 minutos." | 0 |
| 2–5 | Recorrido rápido del IDE | Muestras chat, panel Kiro (Specs, Steering, Hooks, MCP) y la terminal. Solo señalas, no profundizas. | "Es VS Code por fuera; lo distinto está en este panel." | 0 |
| 5–9 | Steering rompehielos | Prompt 1 sin y con `#estilo-argentino`. Pregúntale al público qué estilo quiere. | "El steering es el contexto permanente: cómo quieres que Kiro trabaje." | ~1 |
| 9–11 | Memoria | Prompt 2: "recuerda…" → sesión nueva → lo recuerda. | "Steering es lo que la empresa le enseña a Kiro; memoria es lo que Kiro aprende de ti." | ~1 |
| 11–13 | Steering de empresa | `cp kit/steering-empresa/*.md .kiro/steering/` y lees 2 o 3 reglas de `security.md`. | "Así se gobierna la IA en un banco o una telco: reglas versionadas en el repo." | 0 |
| 13–21 | Spec | Prompt 4. Recorres requirements (formato EARS), design y tasks. Agregas el requisito del público. | "Antes de escribir código, Kiro escribe lo que un arquitecto revisaría." | ~5 |
| 21–31 | Ejecución | **Start task** en las tareas 1–5. Mientras corren, explicas el design.md. Muestras que respetó el steering: Node 24, una Lambda e IAM acotado. | "No le dije qué stack usar en el prompt: lo tomó del steering." | ~10 |
| 31–33 | Hook | Guardas un archivo y se dispara `seguridad-al-guardar` (command, 0 créditos). Opcional: muestras `tests-al-guardar` (agent) apagado. | "Gobernanza automática: cada vez que guardas, se revisan secretos y datos personales." | 0 |
| 33–36 | Deploy | `sam build && sam deploy` en la terminal. | "De la spec a AWS en 30 minutos." | 0 |
| 36–41 | Playwright MCP | Prompt 7: Kiro abre el navegador, llena el form y verifica el board. | "Con MCP, Kiro usa herramientas reales: navegador, documentación, Jira…" | ~4 |
| 41–45 | Cierre | Proyectas el `/board` nuevo y el público se registra en vivo. CTA. | "Esto mismo lo hacemos con tu equipo en un PoC de 2 semanas." | 0 |

## Planes B

- **Una tarea falla o tarda más de 3 min:** "les muestro la versión terminada" → `git checkout respaldo/app-completa`.
- **El deploy falla:** proyectas la versión de respaldo que desplegaste antes (es la del teaser).
- **Sin internet:** pasas al video de respaldo grabado en el ensayo.
- **Se acaban los créditos:** sigues desde la rama de respaldo; el deploy y el hook no gastan créditos.

## Cierre / CTA

- QR del board = lista de interesados con consentimiento.
- Oferta concreta: "PoC de Kiro de 2 semanas" o "workshop de adopción para tu equipo".
- Repo público con los steerings y hooks de la demo.
