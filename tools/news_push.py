#!/usr/bin/env python3
"""Write docs/news/board.json from the News board artifact's posts.

Claude runs this on "push the news":
  1. ArtifactData list  url=https://claude.ai/artifact/C45ccYVziJAgCZintrwv11  collection=posts  out_dir=<dir>
  2. python3 tools/news_push.py <dir>/posts            (add --dry to only print)
  3. commit + push the site; set the board's sync/state pushedAt = now; delete the posts marked deleted.

Newest date first (newer createdAt first on the same day). Drops removed posts and empty fields.
Fields the app reads: id, date, title, text, button, open, until, silent (Board.kt).
"""
import json, re, sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "docs/news/board.json"
PAGES = {"packs", "settings", "help", "pets"}
MAX_POSTS = 20  # the app reads only the first 20


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    if len(args) != 1:
        sys.exit("usage: news_push.py <folder of exported post .json files> [--dry]")
    rows = []
    for f in sorted(Path(args[0]).glob("*.json")):
        d = json.loads(f.read_text())
        d = d.get("data", d)
        d["id"] = f.stem
        rows.append(d)
    gone = [r["id"] for r in rows if r.get("deleted")]
    rows = [r for r in rows if not r.get("deleted")]
    rows.sort(key=lambda r: (r.get("date", ""), r.get("createdAt", 0)), reverse=True)

    posts, problems = [], []
    for r in rows:
        p = {"id": r["id"], "date": r.get("date", ""), "title": (r.get("title") or "").strip(), "text": (r.get("text") or "").strip()}
        if not p["title"]:
            problems.append(f"{r['id']}: no title")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", p["date"]):
            problems.append(f"{r['id']}: bad date {p['date']!r}")
        op, bt = (r.get("open") or "").strip(), (r.get("button") or "").strip()
        if op and bt:
            if op in PAGES or op.startswith("https://"):
                p["button"], p["open"] = bt, op
            else:
                problems.append(f"{r['id']}: button opens {op!r} (not a page or https link)")
        if r.get("until"):
            p["until"] = r["until"]
        if r.get("silent"):
            p["silent"] = True
        posts.append(p)
    if len(posts) > MAX_POSTS:
        problems.append(f"{len(posts)} posts: the app shows only the newest {MAX_POSTS}")
    if problems:
        print("PROBLEMS:\n  " + "\n  ".join(problems))
        if any("no title" in x or "bad date" in x for x in problems):
            sys.exit(1)

    body = json.dumps({"v": 1, "posts": posts}, ensure_ascii=False, indent=2) + "\n"
    if len(body.encode()) >= 64_000:
        sys.exit("board.json would be 64 KB or more: the app ignores it")
    loud = next((p for p in posts if not p.get("silent")), None)
    print(f"{len(posts)} posts ({sum(1 for p in posts if p.get('silent'))} silent); Pets card: {loud['title'] if loud else 'none'}")
    if gone:
        print("removed: " + ", ".join(gone))
    if dry:
        print(body)
        return
    old = OUT.read_text() if OUT.exists() else ""
    if old == body:
        print("board.json unchanged")
    else:
        OUT.write_text(body)
        print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
