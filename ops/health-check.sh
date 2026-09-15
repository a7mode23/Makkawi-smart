#!/usr/bin/env bash
# فحص صحة منصة واصل — يُشغَّل على السيرفر أو محليًا.
# الاستخدام:  bash ops/health-check.sh
# الخروج: 0 = كل شيء سليم، 1 = يوجد تحذير، 2 = يوجد فشل حرج.

set -uo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -f "$APP_DIR/ops/inventory.local.env" ] && . "$APP_DIR/ops/inventory.local.env"

WASEL_APP_DIR="${WASEL_APP_DIR:-$APP_DIR}"
WASEL_BACKUP_DIR="${WASEL_BACKUP_DIR:-$APP_DIR/backups}"
WASEL_BACKUP_MAX_AGE_HOURS="${WASEL_BACKUP_MAX_AGE_HOURS:-26}"
WASEL_DISK_WARN_PCT="${WASEL_DISK_WARN_PCT:-80}"
WASEL_ROUTER_TIMEOUT="${WASEL_ROUTER_TIMEOUT:-5}"
WASEL_URL="${WASEL_URL:-}"
WASEL_DOMAIN="${WASEL_DOMAIN:-}"
WASEL_SERVICES="${WASEL_SERVICES:-}"

pass=0; warn=0; fail=0; skip=0
if [ -t 1 ]; then G=$'\e[32m'; Y=$'\e[33m'; R=$'\e[31m'; B=$'\e[2m'; N=$'\e[0m'; else G=; Y=; R=; B=; N=; fi

ok()   { printf '  %sOK%s    %s\n'   "$G" "$N" "$1"; pass=$((pass+1)); }
wrn()  { printf '  %sWARN%s  %s\n'   "$Y" "$N" "$1"; warn=$((warn+1)); }
err()  { printf '  %sFAIL%s  %s\n'   "$R" "$N" "$1"; fail=$((fail+1)); }
skp()  { printf '  %sSKIP%s  %s\n'   "$B" "$N" "$1"; skip=$((skip+1)); }
sec()  { printf '\n%s\n' "== $1"; }

printf '%s\n' "فحص صحة منصة واصل — $(date '+%Y-%m-%d %H:%M:%S')"
printf '%s\n' "المسار: $WASEL_APP_DIR"

# ── 1) سلامة ملفات التطبيق ─────────────────────────────────────────
sec "ملفات التطبيق"
missing=0
for f in index.php admin.php include/config.php include/readcfg.php lib/routeros_api.class.php; do
  [ -f "$WASEL_APP_DIR/$f" ] || { err "ملف أساسي مفقود: $f"; missing=1; }
done
[ "$missing" -eq 0 ] && ok "كل الملفات الأساسية موجودة"

if command -v php >/dev/null 2>&1; then
  bad=$(cd "$WASEL_APP_DIR" && find . -name '*.php' -not -path './.git/*' -print0 \
        | xargs -0 -n1 php -l 2>&1 | grep -v 'No syntax errors' | head -5)
  if [ -z "$bad" ]; then ok "لا توجد أخطاء صياغة PHP"; else err "أخطاء صياغة PHP: $bad"; fi
  ok "إصدار PHP: $(php -r 'echo PHP_VERSION;')"
else
  skp "php غير متاح — تخطي فحص الصياغة"
fi

# ── 2) الأمان الأساسي ──────────────────────────────────────────────
sec "الأمان"
CFG="$WASEL_APP_DIR/include/config.php"
if [ -f "$CFG" ]; then
  if grep -q 'aWNlbA==' "$CFG"; then
    err "كلمة مرور الأدمن لسه الافتراضية (mikhmon/1234) — غيّرها فورًا (docs/ops/07-security.md §1)"
  else
    ok "كلمة مرور الأدمن مش الافتراضية"
  fi
  perm=$(stat -c '%a' "$CFG" 2>/dev/null || stat -f '%Lp' "$CFG" 2>/dev/null)
  case "$perm" in
    600|640|644) ok "صلاحيات config.php = $perm" ;;
    *) wrn "صلاحيات config.php = $perm (الموصى به 640)" ;;
  esac
  if git -C "$WASEL_APP_DIR" rev-parse --git-dir >/dev/null 2>&1; then
    if git -C "$WASEL_APP_DIR" ls-files -v include/config.php 2>/dev/null | grep -q '^S'; then
      ok "config.php مستثنى من تتبّع git (skip-worktree)"
    elif git -C "$WASEL_APP_DIR" diff --quiet -- include/config.php 2>/dev/null; then
      skp "config.php متتبَّع في git بدون تعديلات محلية"
    else
      wrn "config.php متتبَّع في git وفيه تعديلات محلية — خطر تسريب أسرار (07-security.md §2)"
    fi
  fi
else
  err "include/config.php غير موجود"
fi

# ── 3) استجابة اللوحة ──────────────────────────────────────────────
sec "اللوحة"
if [ -n "$WASEL_URL" ] && command -v curl >/dev/null 2>&1; then
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 15 -L "$WASEL_URL" 2>/dev/null)
  case "$code" in
    200|302) ok "اللوحة ترد ($code) على $WASEL_URL" ;;
    000)     err "اللوحة لا ترد إطلاقًا على $WASEL_URL" ;;
    5*)      err "اللوحة ترجع خطأ خادم ($code) — راجع docs/ops/03-incidents.md §1" ;;
    *)       wrn "اللوحة ترجع $code على $WASEL_URL" ;;
  esac
else
  skp "WASEL_URL غير مضبوط — تخطي فحص اللوحة"
fi

# ── 4) الراوترات ───────────────────────────────────────────────────
sec "الراوترات (MikroTik API)"
if command -v php >/dev/null 2>&1 && [ -f "$CFG" ]; then
  routers=$(cd "$WASEL_APP_DIR" && php -r '
    error_reporting(0); $_SERVER["REQUEST_URI"]="cli";
    include "include/config.php";
    if (!isset($data) || !is_array($data)) exit;
    foreach ($data as $k => $v) {
      if ($k === "mikhmon" || !is_array($v)) continue;
      $raw = isset($v[1]) ? explode("!", $v[1]) : array();
      $addr = isset($raw[1]) ? trim($raw[1]) : "";
      if ($addr === "") continue;
      $p = explode(":", $addr);
      $host = $p[0]; $port = isset($p[1]) && $p[1] !== "" ? $p[1] : "8728";
      echo $k . "|" . $host . "|" . $port . "\n";
    }' 2>/dev/null)
  if [ -z "$routers" ]; then
    wrn "ما في أي راوتر مضاف في config.php"
  else
    while IFS='|' read -r name host port; do
      [ -z "$host" ] && continue
      if timeout "$WASEL_ROUTER_TIMEOUT" bash -c "exec 3<>/dev/tcp/$host/$port" 2>/dev/null; then
        ok "الراوتر '$name' ($host:$port) — منفذ API مفتوح"
      else
        err "الراوتر '$name' ($host:$port) — لا يمكن الوصول لمنفذ API (03-incidents.md §2)"
      fi
    done <<< "$routers"
  fi
else
  skp "تعذّر قراءة الراوترات من config.php"
fi

# ── 5) شهادة SSL ───────────────────────────────────────────────────
sec "شهادة SSL"
if [ -n "$WASEL_DOMAIN" ] && command -v openssl >/dev/null 2>&1; then
  end=$(echo | timeout 15 openssl s_client -servername "$WASEL_DOMAIN" -connect "$WASEL_DOMAIN:443" 2>/dev/null \
        | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  if [ -n "$end" ]; then
    end_ts=$(date -d "$end" +%s 2>/dev/null || date -j -f '%b %d %T %Y %Z' "$end" +%s 2>/dev/null)
    if [ -n "${end_ts:-}" ]; then
      days=$(( (end_ts - $(date +%s)) / 86400 ))
      if   [ "$days" -lt 0 ];  then err "الشهادة منتهية منذ $(( -days )) يوم"
      elif [ "$days" -lt 14 ]; then err "الشهادة تنتهي خلال $days يوم — جدّد فورًا (05-renewals.md)"
      elif [ "$days" -lt 30 ]; then wrn "الشهادة تنتهي خلال $days يوم"
      else ok "الشهادة صالحة $days يوم"; fi
    else wrn "تعذّر تحليل تاريخ انتهاء الشهادة: $end"; fi
  else
    err "تعذّر جلب شهادة $WASEL_DOMAIN"
  fi
else
  skp "WASEL_DOMAIN غير مضبوط — تخطي فحص SSL"
fi

# ── 6) موارد السيرفر ───────────────────────────────────────────────
sec "موارد السيرفر"
if command -v df >/dev/null 2>&1; then
  use=$(df -P "$WASEL_APP_DIR" | awk 'NR==2 {gsub("%","",$5); print $5}')
  if [ -n "$use" ]; then
    if   [ "$use" -ge 90 ]; then err "القرص ممتلئ $use%"
    elif [ "$use" -ge "$WASEL_DISK_WARN_PCT" ]; then wrn "استهلاك القرص $use%"
    else ok "استهلاك القرص $use%"; fi
  fi
fi
if [ -r /proc/meminfo ]; then
  total=$(awk '/MemTotal/{print $2}' /proc/meminfo)
  avail=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
  if [ -n "$total" ] && [ -n "$avail" ] && [ "$total" -gt 0 ]; then
    pct=$(( avail * 100 / total ))
    if [ "$pct" -lt 10 ]; then wrn "الذاكرة المتاحة $pct% فقط"; else ok "الذاكرة المتاحة $pct%"; fi
  fi
fi
if command -v uptime >/dev/null 2>&1; then ok "التشغيل: $(uptime | sed 's/^ *//')"; fi

# ── 7) خدمات النظام ────────────────────────────────────────────────
sec "خدمات النظام"
if [ -n "$WASEL_SERVICES" ] && command -v systemctl >/dev/null 2>&1; then
  for s in $WASEL_SERVICES; do
    if systemctl is-active --quiet "$s" 2>/dev/null; then ok "الخدمة $s تعمل"; else err "الخدمة $s متوقفة"; fi
  done
else
  skp "WASEL_SERVICES غير مضبوط أو systemctl غير متاح"
fi

# ── 8) النسخ الاحتياطي ─────────────────────────────────────────────
sec "النسخ الاحتياطي"
if [ -d "$WASEL_BACKUP_DIR" ]; then
  latest=$(ls -1t "$WASEL_BACKUP_DIR"/wasel-backup-*.tar.gz 2>/dev/null | head -1)
  if [ -n "$latest" ]; then
    mtime=$(stat -c %Y "$latest" 2>/dev/null || stat -f %m "$latest" 2>/dev/null)
    age_h=$(( ( $(date +%s) - mtime ) / 3600 ))
    if [ "$age_h" -le "$WASEL_BACKUP_MAX_AGE_HOURS" ]; then
      ok "آخر نسخة عمرها ${age_h}س — $(basename "$latest")"
    else
      err "آخر نسخة عمرها ${age_h}س (الحد ${WASEL_BACKUP_MAX_AGE_HOURS}س) — شغّل ops/backup.sh"
    fi
  else
    err "لا توجد أي نسخة احتياطية في $WASEL_BACKUP_DIR"
  fi
else
  wrn "مجلد النسخ غير موجود: $WASEL_BACKUP_DIR"
fi

# ── الخلاصة ────────────────────────────────────────────────────────
printf '\n%s\n' "── الخلاصة: ${G}${pass} سليم${N} / ${Y}${warn} تحذير${N} / ${R}${fail} فشل${N} / ${skip} متخطّى"
if [ "$fail" -gt 0 ]; then
  printf '%s\n' "→ يوجد فشل. راجع docs/ops/03-incidents.md"
  exit 2
elif [ "$warn" -gt 0 ]; then
  exit 1
fi
exit 0
