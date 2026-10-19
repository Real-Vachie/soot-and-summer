# The site's FAQ, made from the app's Help text (summer-phone help/faq.md, the one source for both).
# Writes it into docs/index.html between the FAQ:START / FAQ:END marks. Run after the Help text changes.
import html, re
from pathlib import Path

SRC = Path.home()/'Projects/summer-phone/help/faq.md'
PAGE = Path(__file__).resolve().parent.parent/'docs/index.html'
SKIP_SECTIONS = {'Contact'}   # the app's "Email us" card; the site has its own contact line
APP_ONLY = re.compile(r'^(if|button|clip):|^open$')

def inline(t):
    t = html.escape(t, quote=False)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)

def card(q, lines):
    out, items = [], []
    for l in lines + ['']:
        if l.startswith('- '): items.append(f'<li>{inline(l[2:])}</li>'); continue
        if items: out.append('<ul>' + ''.join(items) + '</ul>'); items = []
        if l: out.append(f'<p>{inline(l)}</p>')
    return f'<details><summary>{inline(q)}</summary><div>{"".join(out)}</div></details>'

text = re.sub(r'<!--.*?-->', '', SRC.read_text(), flags=re.S)
blocks, section, q, lines, off = [], None, None, [], False
def flush():
    if q and not off and section not in SKIP_SECTIONS: blocks.append(card(q, lines))
for l in text.splitlines():
    l = l.strip()
    if l.startswith('## '):
        flush(); q = None; section = l[3:]
        if section not in SKIP_SECTIONS: blocks.append(f'<h3>{inline(section)}</h3>')
    elif l.startswith('### '):
        flush(); q, lines, off = l[4:], [], False
    elif q is not None:
        if l == 'off': off = True
        elif not APP_ONLY.match(l): lines.append(l)
flush()

page = PAGE.read_text()
start = page.index('<!-- FAQ:START'); start = page.index('-->', start) + 3
end = page.index('<!-- FAQ:END')
PAGE.write_text(page[:start] + '\n' + '\n'.join(blocks) + '\n' + page[end:])
print(f'{sum(b.startswith("<details") for b in blocks)} questions')
