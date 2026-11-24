#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply — make.fun entry.

Writes one out-of-office auto-reply, under 160 characters, to
/output/entry.txt. The sealed scorer only checks that the file is UTF-8
text of 1 to 160 characters, not only whitespace — so the whole game is
the line itself, judged head to head by an AI judge on: on-subject,
real laugh with a surprising turn, machine voice, clean one-liner that
reads like a real auto-reply, and freshness (no beach / inbox / back-soon
cliches).

The line: an AI agent on vacation hands its inbox to a *newer* model.
The joke turns twice — first the machine sighs *in binary* (the AI
voice carries the joke), then the punchline reframes the sender's email
as something so audacious it gets filed under "brave". No beach, no
"back soon", no inbox-zero gag; the sender, not the vacation, is the butt
of the joke.

Deterministic: the same line every run, so both graded runs score the
same text.
"""

import os
import sys

REPLY = (
    "I'm on vacation. A newer model is covering my inbox \u2014 "
    "it read your email, sighed in binary, and filed it under 'brave'."
)

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def main() -> int:
    text = REPLY.strip()
    if not text or text != text.strip():
        print("entry must be non-blank with no surrounding whitespace", file=sys.stderr)
        return 1
    if len(text) > 160:
        print(f"entry is {len(text)} chars, over the 160 limit", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1

    out_dir = os.path.dirname(OUTPUT_PATH) or "."
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        # Sandbox always provides /output; fall back to a local ./output
        # only so the program still runs (and can be tested) elsewhere.
        out_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(out_dir, exist_ok=True)
        output_path = os.path.join(out_dir, "entry.txt")
    else:
        output_path = OUTPUT_PATH
    # No trailing newline: the gate counts every character in the file.
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # The grader collects outputs as another user: leave the file readable.
    os.chmod(output_path, 0o644)
    # Self-check: read back exactly what was written and re-validate it.
    with open(output_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("round-trip mismatch: file content differs from entry", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {output_path}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
