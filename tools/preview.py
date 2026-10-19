# Private preview copy for a claude.ai artifact: the page without its own <html>/<head> wrapper, brand.css inlined.
import re, sys
from pathlib import Path
D = Path(__file__).resolve().parent.parent/'docs'; out = Path(sys.argv[1])
s = (D/'index.html').read_text()
s = re.sub(r'<!doctype html>|</?html[^>]*>|</?head>|</?body>|<meta charset[^>]*>|<meta name="viewport"[^>]*>', '', s)
s = s.replace('<link rel="stylesheet" href="brand.css">', '<style>' + (D/'brand.css').read_text() + '</style>')
out.write_text(s.strip() + '\n')
