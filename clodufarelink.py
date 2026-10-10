
import os
import re

TOKEN = "fa899fba183a40578d064fc0069dcfd6"
BEACON = "https://static.cloudflareinsights.com/beacon.min.js"

SCRIPT = f"""<!-- Cloudflare Web Analytics -->
<script defer src="{BEACON}" data-cf-beacon='{{"token": "{TOKEN}"}}'></script>
<!-- End Cloudflare Web Analytics -->"""

for root, dirs, files in os.walk("."):
    for file in files:
        if file.lower().endswith((".html", ".htm")):
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8-sig") as f:
                html = f.read()

            if BEACON in html or TOKEN in html:
                continue

            if re.search(r"</head\s*>", html, re.I):
                html = re.sub(
                    r"</head\s*>",
                    SCRIPT + "\n</head>",
                    html,
                    count=1,
                    flags=re.I
                )
            else:
                continue

            with open(path, "w", encoding="utf-8") as f:
                f.write(html)

            print("Updated:", path)

print("Done!")
