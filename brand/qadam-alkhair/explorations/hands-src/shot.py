import os, re, subprocess, tempfile
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"


def shot(svg_text, w, out):
    vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text).groups())
    h = max(1, round(w * vh / vw))
    html = (f"<html><head><style>html,body{{margin:0;background:transparent}}"
            f"svg{{display:block;width:{w}px;height:{h}px}}</style></head><body>{svg_text}</body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--default-background-color=00000000",
                    f"--window-size={w},{h}", f"--screenshot={out}", "file://" + f.name], capture_output=True)
    os.unlink(f.name)
