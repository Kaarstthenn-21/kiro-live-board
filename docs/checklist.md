# Checklist de preparación

## Una semana antes
- [ ] Ensayar el guion completo **en otra cuenta** (no en la de 50 créditos) y anotar los créditos reales de cada bloque.
- [ ] Grabar el ensayo completo en video (plan B sin internet).
- [ ] Desplegar la versión de respaldo: `git checkout respaldo/app-completa && sam build && sam deploy --stack-name kiro-live-board-respaldo`. Esa es la del teaser.
- [ ] Probar el QR del board con 3 celulares distintos (con datos móviles, no solo wifi).

## El día anterior
- [ ] `aws sts get-caller-identity` funciona con el perfil que usarás.
- [ ] Confirmar que el deploy de respaldo terminó: eso ya crea el bucket gestionado de SAM en la cuenta y región, así el deploy en vivo es más rápido.
- [ ] Activar Memory en Kiro (viene apagada) y probarla una vez.
- [ ] Abrir el panel MCP y confirmar que `playwright` y `aws-docs` están en verde (la primera vez descargan paquetes).
- [ ] Desactivar el auto-update de Kiro y anotar la versión con la que ensayaste.
- [ ] Borrar las memorias de prueba para que la demo de memoria arranque limpia.

## Una hora antes
- [ ] `git checkout main && git clean -fd` para dejar el proyecto en estado inicial.
- [ ] Login hecho en Kiro, modelo en **Auto**, créditos disponibles revisados.
- [ ] Fuente del editor en 18–20 y tema claro si el proyector es malo.
- [ ] Notificaciones del Mac en "No molestar".
- [ ] Pestañas abiertas: board de respaldo, consola de AWS (CloudFormation) y slides.

## Después de la charla
- [ ] Exportar los leads: `aws dynamodb scan --table-name <TableName> --output json > leads.json`.
- [ ] Pasárselos a comercial (solo los que dieron consentimiento; todos lo dieron por diseño).
- [ ] `sam delete` de los stacks si ya no los necesitas.
