from __future__ import annotations

import re
from pathlib import Path

def fix_file(path: Path) -> bool:
    s = path.read_text(encoding="utf-8")

    # Fix double-escaped ampersands in href/src attributes:
    # ...?a=1&amp;amp;b=2  ->  ...?a=1&amp;b=2
    new = re.sub(r'((?:href|src)="[^"]*?)&amp;amp;([^"]*")', r"\1&amp;\2", s)

    # Some builds can create even worse chains; collapse repeatedly
    # until stable (e.g., &amp;amp;amp; -> &amp;)
    while True:
        newer = re.sub(r'((?:href|src)="[^"]*?)&amp;amp;([^"]*")', r"\1&amp;\2", new)
        if newer == new:
            break
        new = newer

    if new != s:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main(build_dir: str = "_build/html") -> None:
    root = Path(build_dir)
    if not root.exists():
        raise SystemExit(f"Build dir not found: {root.resolve()}")

    changed = 0
    total = 0
    for html_file in root.rglob("*.html"):
        total += 1
        if fix_file(html_file):
            changed += 1

    print(f"Post-processed HTML: {changed}/{total} files updated in {root.resolve()}")

if __name__ == "__main__":
    main()
