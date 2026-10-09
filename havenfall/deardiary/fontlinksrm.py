
from pathlib import Path
import re

folder = Path(__file__).parent

pattern = re.compile(
    r'<link\b(?=[^>]*(?:fonts\.googleapis\.com|fonts\.gstatic\.com))[^>]*>\s*',
    re.IGNORECASE
)

for file in folder.rglob("*.html"):
    content = file.read_text(encoding="utf-8")
    updated, count = pattern.subn("", content)

    if count:
        file.write_text(updated, encoding="utf-8")
        print(f"Updated: {file} — removed {count} links")

print("Done!")