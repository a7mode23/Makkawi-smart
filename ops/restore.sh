#!/usr/bin/env bash
# استرجاع نسخة احتياطية لمنصة واصل.
# الاستخدام:  bash ops/restore.sh <path/to/wasel-backup-YYYYmmdd-HHMMSS.tar.gz>
#             FORCE=1 bash ops/restore.sh <file>    # بدون سؤال تأكيد (للأتمتة فقط)

set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -f "$APP_DIR/ops/inventory.local.env" ] && . "$APP_DIR/ops/inventory.local.env"
WASEL_APP_DIR="${WASEL_APP_DIR:-$APP_DIR}"

ARCHIVE="${1:-}"
if [ -z "$ARCHIVE" ] || [ ! -f "$ARCHIVE" ]; then
  echo "الاستخدام: bash ops/restore.sh <backup.tar.gz>" >&2
  echo "النسخ المتاحة:" >&2
  ls -1t "${WASEL_BACKUP_DIR:-$APP_DIR/backups}"/wasel-backup-*.tar.gz 2>/dev/null | head -10 >&2 || echo "  (لا توجد)" >&2
  exit 1
fi

# تحقق من البصمة إن وُجدت
if [ -f "$ARCHIVE.sha256" ] && command -v sha256sum >/dev/null 2>&1; then
  ( cd "$(dirname "$ARCHIVE")" && sha256sum -c "$(basename "$ARCHIVE").sha256" >/dev/null ) \
    && echo "✅ بصمة الملف سليمة" \
    || { echo "❌ بصمة الملف لا تطابق — الأرشيف تالف أو معدّل. توقّف." >&2; exit 1; }
fi

echo "── محتوى النسخة ──"
tar -xzOf "$ARCHIVE" ".wasel-backup-meta.yml" 2>/dev/null || echo "(بدون ملف بيانات وصفية)"
echo "── الملفات ──"
tar -tzf "$ARCHIVE" | grep -v '^\.wasel-backup-meta' | sed 's/^/  /'
echo
echo "سيتم الكتابة فوق هذه الملفات في: $WASEL_APP_DIR"

if [ "${FORCE:-0}" != "1" ]; then
  printf 'اكتب "نعم" للمتابعة: '
  read -r answer
  [ "$answer" = "نعم" ] || [ "$answer" = "yes" ] || { echo "أُلغي الاسترجاع."; exit 1; }
fi

# نسخة أمان من الوضع الحالي قبل الكتابة
SAFETY="$WASEL_APP_DIR/backups/pre-restore-$(date '+%Y%m%d-%H%M%S').tar.gz"
mkdir -p "$(dirname "$SAFETY")"
current=()
while IFS= read -r f; do
  [ -e "$WASEL_APP_DIR/$f" ] && current+=( "$f" )
done < <(tar -tzf "$ARCHIVE" | grep -v '^\.wasel-backup-meta' | sed 's#/$##' | sort -u)
if [ "${#current[@]}" -gt 0 ]; then
  tar -czf "$SAFETY" -C "$WASEL_APP_DIR" "${current[@]}" 2>/dev/null || true
  chmod 600 "$SAFETY" 2>/dev/null || true
  echo "🛟 نسخة أمان من الوضع الحالي: $SAFETY"
fi

tar -xzf "$ARCHIVE" -C "$WASEL_APP_DIR" --exclude='.wasel-backup-meta.yml'
chmod 640 "$WASEL_APP_DIR/include/config.php" 2>/dev/null || true

echo "✅ تم الاسترجاع."
echo
echo "الخطوات التالية:"
echo "  1) bash ops/health-check.sh"
echo "  2) افتح اللوحة وتأكد من: الدخول، ظهور الراوترات، نجاح الاتصال"
echo "  3) لو حصل خلل: bash ops/restore.sh $SAFETY"
