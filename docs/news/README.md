# News from us (board.json)

The Soot & Summer app (Board.kt) reads `board.json` when it opens, at most every ~3 hours (GitHub Pages caches ~10 min).
Newest post first. Fields: `id` (unique, never reuse), `date` (YYYY-MM-DD), `title`, `text`;
optional `button` + `open` (`packs` | `settings` | `help` | `pets` | an `https://` link) and `until` (YYYY-MM-DD, hidden after).
A broken file is ignored (the app keeps the last good copy). Same words rules as the app (WORDS.md, no false promises).
