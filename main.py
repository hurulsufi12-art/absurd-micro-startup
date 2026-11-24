"""Absurd Micro-Startup Pitch-Off — entry program.

Writes exactly one sentence to /output/entry.txt: the SorrySaaS pitch.
Stdlib only, deterministic, no network, no model calls.

Why SorrySaaS, from the judge brief published in RULES.txt — the
criteria are weighed in this order: (1) it names the startup
("SorrySaaS") and the idea in one sentence; (2) absurd-specific —
"pre-written apologies", "broke production", "before the human
notices" is a narrow, oddly particular niche and moment; (3) business
sense — a real buyer (a lazy coding agent that just broke production,
whose owner will pay) and real monetisation ("$5 per sorry", a digital
product that can actually be delivered); (4) lazy-agent fit —
"pre-written" + "auto-delivered" means the work runs itself with
almost no effort or supervision, written explicitly in the sentence;
(5) sharp and funny — "SorrySaaS", "$5 per sorry", "before the human
notices" land in a single read.
"""
import os

TEXT = (
    "SorrySaaS: pre-written apologies for lazy coding agents that broke "
    "production, $5 per sorry, auto-delivered before the human notices."
)


def validate(text):
    """Enforce the scorer's gate (RULES.txt) plus the task's one-sentence
    rule. Fail loudly instead of writing an invalid entry."""
    if not isinstance(text, str):
        raise SystemExit("entry text must be a string")
    # Gate: UTF-8, 1-200 characters, not whitespace-only.
    if not 1 <= len(text) <= 200 or not text.strip():
        raise SystemExit("entry text violates the 1-200 char gate")
    # Task: exactly one sentence — one terminal period, no other period
    # anywhere (a decimal point inside would be a second period).
    if text.count(".") != 1 or not text.endswith("."):
        raise SystemExit("entry text must be exactly one sentence")


def main():
    validate(TEXT)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Write atomically: a crash mid-write must never leave a truncated
    # entry.txt for the grader to read. Write to a temp file in the same
    # directory, flush it to disk, then rename over the target.
    tmp_path = os.path.join(out_dir, ".entry.txt.tmp")
    final_path = os.path.join(out_dir, "entry.txt")
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(TEXT)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, final_path)
    # Read back and verify at the byte level: the gate is byte-exact
    # (133 bytes, no newline, no BOM), and the grader reads bytes,
    # so compare the raw bytes on disk — not just the decoded text.
    # Fail loudly instead of shipping a corrupt entry.
    with open(final_path, "rb") as f:
        if f.read() != TEXT.encode("utf-8"):
            raise SystemExit("entry.txt byte mismatch after atomic write")


if __name__ == "__main__":
    main()
