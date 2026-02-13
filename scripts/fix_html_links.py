from __future__ import annotations

import re
import sys
from pathlib import Path


_PATTERN = re.compile(r'((?:href|src)="[^"]*?)&amp;amp;([^"]*")')


def fix_file(path: Path) -> bool:
    s = path.read_text(encoding="utf-8")

    new = s
    # Collapse repeatedly until stable: &amp;amp; -> &amp; (and deeper chains)
    while True:
        newer = _PATTERN.sub(r"\1&amp;\2", new)
        if newer == new:
            break
        new = newer

    if new != s:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def iter_build_roots(arg: str | None) -> list[Path]:
    if arg:
        return [Path(arg)]

    candidates = [
        Path("_build/dirhtml"),
        Path("_build/singlehtml"),
        Path("_build/html"),
    ]
    # Use all candidates that exist
    roots = [p for p in candidates if p.exists()]
    return roots


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    roots = iter_build_roots(arg)

    if not roots:
        raise SystemExit(
            "Build dir not found. Tried: _build/dirhtml, _build/singlehtml, _build/html "
            "(or pass a path: python scripts/fix_html_links.py _build/dirhtml)"
        )

    for root in roots:
        changed = 0
        total = 0
        for html_file in root.rglob("*.html"):
            total += 1
            if fix_file(html_file):
                changed += 1

        print(f"Post-processed HTML: {changed}/{total} files updated in {root.resolve()}")


if __name__ == "__main__":
    main()
