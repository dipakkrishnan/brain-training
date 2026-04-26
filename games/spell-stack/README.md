# Spell Stack

A working-memory brain-training game. A 3x3 grid of runes lights up in a
sequence; each round a directive tells you how to recall it (forward,
reversed, or sorted by color name). Sequence length grows with each
perfect cast and shrinks on a miscast.

## Play locally

The game is a single self-contained HTML file with no dependencies and
no network calls.

One-command run (recommended, opens at http://localhost:8000):

```sh
python3 -m http.server 8000 --directory games/spell-stack
```

Or just open `games/spell-stack/index.html` directly in any modern browser.

## Session

- 8 rounds, 5-minute cap.
- Sequence length starts at 3, max 8, min 3.
- Score is shown live and on the end-of-game panel.

## Directives

- **FORWARD** (1.0x): tap cells in the order they lit up.
- **REVERSE** (1.5x): tap cells in reverse order.
- **ALPHA** (2.0x): tap by color name alphabetically (Blue -> Green -> Red -> Yellow); ties broken by original temporal order.

## Cognitive target

Working memory: maintenance under interference plus deliberate
manipulation (reverse / sort) of the held sequence.
