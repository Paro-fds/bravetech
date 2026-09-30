"""Stamp `updated:` on every staged markdown file, in UTC.

Run from .githooks/pre-commit. The point is that `updated:` is a fact git
already owns, so nobody should be asked to remember it: the alternative was a
hand-maintained date, and this repository has already watched three documents
carry a stale test count for two Epics.

Two things it deliberately refuses to do:

* It will not stamp a file that has unstaged changes. Re-adding such a file
  would sweep those changes into the commit behind the author's back, which is
  worse than a stale date. It warns and skips instead.
* It will not invent a `created:`. A file without frontmatter gets a full block
  with both dates equal; a file whose frontmatter lacks `created:` gets it set
  to the same value as `updated:`, which is the best guess available and is
  visibly a guess because the two match.
"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def staged_markdown() -> list[str]:
    # ACMR, not ACM. R is load-bearing: git reports a rename as R, so the first
    # version of this hook silently skipped every renamed file - and the commit
    # that installed the hook renamed eleven documents, all eleven of which it
    # declined to stamp while reporting success on the other sixty-four.
    out = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "--", "*.md")
    return [line for line in out.splitlines() if line.strip()]


def has_unstaged_changes(path: str) -> bool:
    return bool(git("diff", "--name-only", "--", path).strip())


def stamp(path: Path) -> str:
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        block = f"---\ncreated: {NOW}\nupdated: {NOW}\n---\n\n"
        path.write_text(block + text, encoding="utf-8")
        return "frontmatter added"

    end = text.find("\n---", 3)
    if end == -1:
        return "SKIPPED - frontmatter opens and never closes"

    head, rest = text[: end + 1], text[end + 1 :]

    if re.search(r"^updated:", head, re.M):
        new_head = re.sub(r"^updated:.*$", f"updated: {NOW}", head, count=1, flags=re.M)
    else:
        new_head = head.rstrip("\r\n") + f"\nupdated: {NOW}\n"

    if not re.search(r"^created:", new_head, re.M):
        new_head = re.sub(r"^updated:", f"created: {NOW}\nupdated:", new_head, count=1, flags=re.M)

    if new_head == head:
        return "unchanged"
    path.write_text(new_head + rest, encoding="utf-8")
    return "stamped"


def main() -> int:
    files = staged_markdown()
    if not files:
        return 0

    restaged, skipped = [], []
    for name in files:
        path = Path(name)
        if not path.exists():
            continue
        if has_unstaged_changes(name):
            skipped.append(name)
            continue
        result = stamp(path)
        if result in ("stamped", "frontmatter added"):
            restaged.append(name)
        elif result.startswith("SKIPPED"):
            print(f"  {name}: {result}", file=sys.stderr)

    if restaged:
        subprocess.run(["git", "add", "--", *restaged], check=True)
        print(f"updated: stamped {NOW} on {len(restaged)} file(s)")

    for name in skipped:
        print(f"  not stamped, it has unstaged changes: {name}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
