# News from us (board.json)

The Soot & Summer app (Board.kt) reads `board.json` when it opens, at most every ~3 hours (GitHub Pages caches ~10 min).
Newest post first. Fields: `id` (unique, never reuse), `date` (YYYY-MM-DD), `title`, `text`;
optional `button` + `open` (`packs` | `settings` | `help` | `pets` | an `https://` link) and `until` (YYYY-MM-DD, hidden after).
`silent: true` = listed on the News page only (in date order), never the Pets card or the orange NEW dot: for posts added after the fact.
Edited from the News board artifact (https://claude.ai/artifact/C45ccYVziJAgCZintrwv11, `tools/news_push.py`); Claude writes this file from it on "push the news".
A broken file is ignored (the app keeps the last good copy). Same words rules as the app (WORDS.md, no false promises).
