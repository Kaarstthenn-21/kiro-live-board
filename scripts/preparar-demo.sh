#!/usr/bin/env bash
# Prepara el repo de la demo con dos ramas:
#   main                  -> estado inicial (solo .kiro, kit, docs, scripts). Aquí construyes en vivo.
#   respaldo/app-completa -> app terminada en la raíz (plan B y versión del teaser).
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -d .git ]; then
  echo "Ya existe un repo git aquí. Bórralo (rm -rf .git) si quieres regenerarlo."
  exit 1
fi

cat > .gitignore <<'EOF'
.aws-sam/
node_modules/
leads.json
.DS_Store
EOF

git init -q -b main
git add .kiro kit docs scripts .gitignore README.md
git commit -qm "Estado inicial de la demo: steering, MCP, hooks y guion"

git checkout -qb respaldo/app-completa
cp -R respaldo/. .
cp kit/steering-empresa/*.md .kiro/steering/
git add -A -- . ':!respaldo'
git commit -qm "Respaldo: app Kiro Live Board terminada"

git checkout -q main
# La carpeta respaldo/ queda fuera de main a propósito: no debe verla Kiro durante la demo.
mkdir -p ../kiro-live-board-respaldo-src && mv respaldo ../kiro-live-board-respaldo-src/ 2>/dev/null || true

echo "Listo:"
git branch
echo "Construye en vivo en 'main'. Plan B: git checkout respaldo/app-completa"
