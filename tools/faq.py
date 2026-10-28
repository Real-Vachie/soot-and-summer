# The site's FAQ, made from the app's Help text (summer-phone help/faq.md, the one source for both).
# Writes it into docs/index.html between the FAQ:START / FAQ:END marks. Run after the Help text changes.
# Like the app's Help (HELP_SEARCH): search box, Most asked (`top`), a tile per section with an `icon:` (the app's
# res/drawable/help_<icon>.xml as SVG; icon + title, `words:` tags, "N questions ›"), each topic as one card of rows,
# Still stuck? + Email us. The page's script runs search and tiles; without it the tiles are links and every question shows.
# --check: only say whether the page is stale (exit 1), for linked-check.
import html, re, sys
from pathlib import Path

SRC = Path.home()/'Projects/summer-phone/help/faq.md'
PAGE = Path(__file__).resolve().parent.parent/'docs/index.html'
ICONS = Path.home()/'Projects/summer-phone/app/src/main/res/drawable'
PAW = '<circle cx="8" cy="7" r="2"/><circle cx="16" cy="7" r="2"/><circle cx="5" cy="12" r="1.8"/><circle cx="19" cy="12" r="1.8"/><path d="M8 18c0-3 2-5 4-5s4 2 4 5c0 1.5-2 2-4 2s-4-.5-4-2z"/>'   # play = the app's paw
SKIP_SECTIONS = {'Contact'}   # the app's "Email us" card; the site has its own contact line
APP_ONLY = re.compile(r'^(if|button|clip|live|words|icon):|^(open|top)$')   # words/icon/top: the app's search + topic tiles

def inline(t):
    t = html.escape(t, quote=False)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)

def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

def icon(name):
    body = PAW if name == 'play' else f'<path d="{re.search(r"pathData=\"([^\"]+)", (ICONS/f"help_{name}.xml").read_text())[1]}"/>'
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{body}</svg>'

def card(q, lines, words):
    out, items = [], []
    for l in lines + ['']:
        if l.startswith('- '): items.append(f'<li>{inline(l[2:])}</li>'); continue
        if items: out.append('<ul>' + ''.join(items) + '</ul>'); items = []
        if l: out.append(f'<p>{inline(l)}</p>')
    w = f' data-w="{html.escape(", ".join(words))}"' if words else ''
    return f'<details id="q-{slug(q)}"{w}><summary>{inline(q)}</summary><div>{"".join(out)}</div></details>'

text = re.sub(r'<!--.*?-->', '', SRC.read_text(), flags=re.S)
sections, section, q, lines, words, off, top = [], None, None, [], [], False, False
def flush():
    if q and not off and section['title'] not in SKIP_SECTIONS:
        section['cards'].append(card(q, lines, words))
        if top: tops.append(q)
tops = []
for l in text.splitlines():
    l = l.strip()
    if l.startswith('## '):
        flush(); q = None; section = {'title': l[3:], 'icon': None, 'tags': [], 'cards': []}; sections.append(section)
    elif l.startswith('### '):
        flush(); q, lines, words, off, top = l[4:], [], [], False, False
    elif q is None and section:
        if l.startswith('icon:'): section['icon'] = l[5:].strip()
        elif l.startswith('words:'): section['tags'] = [w.strip() for w in l[6:].split('·')]
    elif q is not None:
        if l == 'off': off = True
        elif l == 'top': top = True
        elif l.startswith('words:'): words = [w.strip() for w in l[6:].split(',')]
        elif not APP_ONLY.match(l): lines.append(l)
flush()
sections = [s for s in sections if s['title'] not in SKIP_SECTIONS and s['cards']]

def tile(s):
    n = len(s['cards'])
    tags = ''.join(f'<span>{inline(w)}</span>' for w in s['tags'])
    return (f'<a class="tile" href="#t-{slug(s["title"])}"><span class="th"><span class="ic">{icon(s["icon"])}</span><b>{inline(s["title"])}</b></span>'
            f'<span class="kw">{tags}</span><i>{"1 question" if n == 1 else f"{n} questions"} ›</i></a>')

blocks = [
    '<label class="hs" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4,11a7,7 0 1,0 14,0a7,7 0 1,0 -14,0z M20,20l-4,-4"/></svg>'
    '<input type="search" placeholder="Search help" aria-label="Search help" autocomplete="off"><button type="button" class="hx" hidden aria-label="Clear search">×</button></label>',
    '<div class="hhome">',
    '<div class="lbl">Most asked</div><div class="chips">' + ''.join(f'<a class="chip" href="#q-{slug(t)}">{inline(t)}</a>' for t in tops) + '</div>',
    '<div class="lbl">Topics</div><div class="tiles">' + ''.join(tile(s) for s in sections if s['icon']) + '</div>',
    '</div>',
    '<button type="button" class="hback" hidden>‹ Help</button><div class="hfound lbl" hidden></div><div class="hres qs" hidden></div>',
]
for s in sections:
    blocks.append(f'<div class="topic" id="t-{slug(s["title"])}"><h3>{inline(s["title"])}</h3><div class="qs">')
    blocks += s['cards']
    blocks.append('</div></div>')
blocks.append('<div class="stuck"><div><b>Still stuck?</b>Write to us and we\'ll help.</div><a class="btn" href="mailto:vachiek@gmail.com">✉ Email us</a></div>')

page = PAGE.read_text()
start = page.index('<!-- FAQ:START'); start = page.index('-->', start) + 3
end = page.index('<!-- FAQ:END')
new = page[:start] + '\n' + '\n'.join(blocks) + '\n' + page[end:]
if '--check' in sys.argv:   # linked-check (MasterPlan claude/linked.toml): exit 1 when the page is stale, write nothing
    sys.exit(0 if new == page else 'docs/index.html FAQ is stale: run tools/faq.py')
PAGE.write_text(new)
print(f'{sum(b.startswith("<details") for b in blocks)} questions, {len(tops)} most asked, {sum(1 for s in sections if s["icon"])} tiles')
