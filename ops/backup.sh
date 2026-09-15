#!/usr/bin/env bash
# نسخة احتياطية من كل ملفات حالة منصة واصل.
# الاستخدام:  bash ops/backup.sh
#             WASEL_BACKUP_DIR=/var/backups/wasel bash ops/backup.sh
#
# ⚠️ الناتج يحتوي بيانات دخول الراوترات — تعامل معه كملف أسرار (راجع 06-backup-restore.md §و).

set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -f "$APP_DIR/ops/inventory.local.env" ] && . "$APP_DIR/ops/inventory.local.env"

WASEL_APP_DIR="${WASEL_APP_DIR:-$APP_DIR}"
WASEL_BACKUP_DIR="${WASEL_BACKUP_DIR:-$APP_DIR/backups}"
WASEL_BACKUP_KEEP="${WASEL_BACKUP_KEEP:-14}"

STAMP="$(date '+%Y%m%d-%H%M%S')"
OUT="$WASEL_BACKUP_DIR/wasel-backup-$STAMP.tar.gz"

# ملفات الحالة التي يكتبها التطبيق وقت التشغيل (راجع docs/ops/01-architecture.md §3)
TARGETS=(
  include/config.php
  include/lang.php
  include/theme.php
  img
)
for t in "$WASEL_APP_DIR"/voucher/template*.php "$WASEL_APP_DIR"/voucher/default*.php; do
  [ -e "$t" ] && TARGETS+=( "voucher/$(basename "$t")" )
done

mkdir -p "$WASEL_BACKUP_DIR"
chmod 700 "$WASEL_BACKUP_DIR" 2>/dev/null || true

present=(); missing=()
for t in "${TARGETS[@]}"; do
  if [ -e "$WASEL_APP_DIR/$t" ]; then present+=( "$t" ); else missing+=( "$t" ); fi
done

if [ "${#present[@]}" -eq 0 ]; then
  echo "خطأ: ما في أي ملف حالة للنسخ في $WASEL_APP_DIR" >&2
  exit 1
fi

META="$(mktemp)"
trap 'rm -f "$META"' EXIT
{
  echo "backup_time: $(date '+%Y-%m-%d %H:%M:%S %z')"
  echo "app_dir: $WASEL_APP_DIR"
  echo "host: $(hostname 2>/dev/null || echo unknown)"
  echo "app_version: $(cat "$WASEL_APP_DIR/verson.txt" 2>/dev/null || echo unknown)"
  echo "git_commit: $(git -C "$WASEL_APP_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
  echo "git_branch: $(git -C "$WASEL_APP_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
  echo "php_version: $(php -r 'echo PHP_VERSION;' 2>/dev/null || echo unknown)"
  echo "routers:"
  php -r '
    error_reporting(0); $_SERVER["REQUEST_URI"]="cli";
    include $argv[1]."/include/config.php";
    if (!isset($data) || !is_array($data)) exit;
    foreach ($data as $k => $v) {
      if ($k === "mikhmon" || !is_array($v)) continue;
      $raw = isset($v[1]) ? explode("!", $v[1]) : array();
      echo "  - name: " . $k . "  addr: " . (isset($raw[1]) ? $raw[1] : "?") . "\n";
    }' "$WASEL_APP_DIR" 2>/dev/null || true
  echo "files:"
  printf '  - %s\n' "${present[@]}"
  [ "${#missing[@]}" -gt 0 ] && printf '  # مفقود: %s\n' "${missing[@]}"
} > "$META"

cp "$META" "$WASEL_APP_DIR/.wasel-backup-meta.yml"
tar -czf "$OUT" -C "$WASEL_APP_DIR" ".wasel-backup-meta.yml" "${present[@]}"
rm -f "$WASEL_APP_DIR/.wasel-backup-meta.yml"
chmod 600 "$OUT"

if command -v sha256sum >/dev/null 2>&1; then
  ( cd "$WASEL_BACKUP_DIR" && sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256" )
fi

size=$(du -h "$OUT" | cut -f1)
echo "✅ النسخة جاهزة: $OUT  ($size)"
[ "${#missing[@]}" -gt 0 ] && echo "ℹ️  ملفات غير موجودة (طبيعي لو ما اتغيّرت): ${missing[*]}"

# تنظيف النسخ القديمة
old=$(ls -1t "$WASEL_BACKUP_DIR"/wasel-backup-*.tar.gz 2>/dev/null | tail -n +"$((WASEL_BACKUP_KEEP+1))" || true)
if [ -n "$old" ]; then
  echo "$old" | while read -r f; do rm -f "$f" "$f.sha256"; echo "🗑️  حُذفت نسخة قديمة: $(basename "$f")"; done
fi

cat <<'EOF'

⚠️ تذكير: هذه نسخة السيرفر فقط.
   تقارير المبيعات والمستخدمين مخزّنة داخل الراوتر — خذ نسخة منه أيضًا:
     /system backup save name=wasel-weekly
     /export file=wasel-config
   وانقل النسخ خارج السيرفر. (docs/ops/06-backup-restore.md)
EOF
