#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path


def normalize_inline_math(text: str) -> str:
    out: list[str] = []
    buf: list[str] = []
    in_math = False
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]
        prev = text[i - 1] if i > 0 else ""
        nxt = text[i + 1] if i + 1 < n else ""

        is_single_dollar = ch == "$" and prev != "\\" and prev != "$" and nxt != "$"

        if is_single_dollar:
            if in_math:
                out.append(f"${''.join(buf).strip()}$")
                buf.clear()
                in_math = False
            else:
                in_math = True
            i += 1
            continue

        if in_math:
            buf.append(ch)
        else:
            out.append(ch)
        i += 1

    if in_math:
        out.append("$" + "".join(buf))

    return "".join(out)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: normalize_inline_math.py <input.md>", file=sys.stderr)
        return 2

    source = Path(sys.argv[1]).read_text()
    sys.stdout.write(normalize_inline_math(source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
