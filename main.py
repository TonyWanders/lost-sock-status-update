#!/usr/bin/env python3
"""Funniest Lost Sock Status Update - make.fun bounty entry.

Writes one status update, in the voice of a lost sock, to
/output/entry.txt. Fully deterministic: no randomness, no time,
no network, no input. The line is a fixed string.

Usage: python3 main.py [output-path]
With no argument, the output goes to $OUTPUT_PATH, then to
/output/entry.txt. With an argument, that path is used instead: a
directory argument means <directory>/entry.txt, a file argument is
used as the output file itself.
"""

import os
import sys

LINE = "Day 4 as the dog's favourite toy. He carries me everywhere, shows me off, and I have never felt so seen, or so damp."

MIN_CHARS = 1
MAX_CHARS = 120


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 120 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not MIN_CHARS <= chars <= MAX_CHARS:
        raise ValueError(f"line is {chars} characters, outside 1-120")
    if not text.strip():
        raise ValueError("line is only white space")
    return chars


def resolve_output_path() -> str:
    """Pick the output file path: argv[1], then $OUTPUT_PATH, then default.

    An explicit argument that is a directory (existing, or ending in a
    separator) means <directory>/entry.txt; anything else is the output
    file itself. $OUTPUT_PATH ending in "entry.txt" is used as-is,
    otherwise it names the directory holding entry.txt.
    """
    if len(sys.argv) > 1:
        given = sys.argv[1]
        if given.endswith(os.sep) or os.path.isdir(given):
            return os.path.join(given, "entry.txt")
        return given
    out_dir = os.environ.get("OUTPUT_PATH") or "/output"
    if out_dir.endswith("entry.txt"):
        return out_dir
    return os.path.join(out_dir, "entry.txt")


def write_entry(text: str, path: str) -> int:
    """Write the entry line plus a trailing newline to the output target.

    Creates parent dirs as needed. Returns the character count written.
    """
    parent = os.path.dirname(path) or "."
    os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    return len(text)


def main() -> int:
    try:
        chars = validate(LINE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    written = write_entry(LINE, path)
    print(f"wrote {written} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
