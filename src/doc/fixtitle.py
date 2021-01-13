from pathlib import Path
import os

def fix_no_title(path: str, title: str):
    content = ''
    with open(path) as fin:
        content = fin.read()

    with open(path, 'w+') as fout:
        fout.write(content.replace('&lt;no title&gt;', title))

fix_no_title('./_build/html/guide.html', 'Guide')

for root, _, files in os.walk('./_build/html/guide'):
    for path in (it for it in files if it.endswith('.html')):
        fix_no_title(Path(root) / path, 'Guide')

