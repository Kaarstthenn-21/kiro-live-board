# Kiro Live Board · kit de la charla Kiro fast track

App que se construye en vivo durante la charla: los asistentes escanean un QR, se registran y aparecen en un tablero en el proyector. Al final te quedas con la lista de interesados.

## Qué hay aquí

```
.kiro/
  steering/estilo-argentino.md   # rompehielos (inclusión manual: #estilo-argentino)
  settings/mcp.json              # Playwright + AWS Documentation
  hooks/seguridad-al-guardar.json  # command: revisa secretos/PII, 0 créditos
  hooks/tests-al-guardar.json      # agent: actualiza tests (apagado, gasta créditos)
kit/steering-empresa/            # product, tech, security: se copian EN VIVO a .kiro/steering/
docs/guion-charla.md             # minuto a minuto + créditos + planes B
docs/prompts.md                  # prompts exactos para copiar
docs/checklist.md                # preparación antes/durante/después
scripts/check-secrets.sh         # lo ejecuta el hook de seguridad
scripts/preparar-demo.sh         # crea ramas main (inicio) y respaldo/app-completa
respaldo/                        # app terminada y probada (SAM + Lambda Node 24 + DynamoDB);
                                 # preparar-demo.sh la pasa a la rama respaldo/app-completa
```

## Primeros pasos

```bash
cd kiro-live-board
bash scripts/preparar-demo.sh     # crea el repo con las 2 ramas
kiro .                            # o abre la carpeta desde Kiro
```

Probar la app de respaldo:
```bash
git checkout respaldo/app-completa
npm test                          # 6 tests con node --test
sam build && sam deploy --stack-name kiro-live-board-respaldo
git checkout main
```

Requisitos: AWS CLI + SAM CLI configurados, Node 20+ local, `uv` (para el MCP de AWS Docs).

Lee primero `docs/guion-charla.md`.
