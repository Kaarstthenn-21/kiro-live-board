#!/usr/bin/env bash
# Revisión rápida de secretos y fugas de datos personales.
# La usa el hook .kiro/hooks/seguridad-al-guardar.json (no consume créditos).
set -u

TARGETS=$(ls -d src template.yaml 2>/dev/null)
if [ -z "$TARGETS" ]; then
  echo "check-secrets: no hay código todavía, nada que revisar."
  exit 0
fi

FOUND=0
check() {
  local label="$1" pattern="$2"
  local hits
  hits=$(grep -RInE --exclude='*.test.mjs' "$pattern" $TARGETS 2>/dev/null)
  if [ -n "$hits" ]; then
    echo "⚠️  $label"
    echo "$hits" | sed 's/^/    /'
    FOUND=1
  fi
}

check "Posible AWS Access Key en el código" 'AKIA[0-9A-Z]{16}'
check "Posible secreto o contraseña en texto plano" '(secret|password|passwd|api[_-]?key|token)[[:space:]]*[:=][[:space:]]*["'\''][^"'\'']{6,}'
check "Posible log de datos personales (correo) en CloudWatch" 'console\.(log|info|error|warn)\(.*email'
check "Uso de innerHTML (riesgo de XSS)" '\.innerHTML[[:space:]]*='
check "Permiso IAM comodín" 'Action:[[:space:]]*["'\'']?\*'

if [ "$FOUND" -eq 0 ]; then
  echo "✅ check-secrets: sin secretos ni fugas de datos personales detectadas."
  exit 0
fi
echo "❌ check-secrets: revisa los hallazgos antes de hacer commit (regla de security.md)."
exit 1
