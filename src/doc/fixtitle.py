from pathlib import Path
import os
import glob
import shutil
import pathlib

def fix_no_title(path: str, title: str):
    content = ''
    with open(path) as fin:
        content = fin.read()

    with open(path, 'w+') as fout:
        content = content.replace('&lt;no title&gt;', title)
        content = content.replace('guide/images', '../images')
        fout.write(content)

fix_no_title('./_build/html/guide.html', 'Guide')

cwd = os.getcwd()
os.chdir('../..')
os.makedirs('./docs/images', exist_ok=True)
image_dir = pathlib.Path('./docs/images')

for path in glob.glob('*/images/*.svg'):
    if path.startswith('docs/images'):
        continue
    shutil.copy(path, image_dir / os.path.split(path)[-1])

os.chdir(cwd)

for root, _, files in os.walk('./_build/html/guide'):
    for path in (it for it in files if it.endswith('.html')):
        fix_no_title(Path(root) / path, 'Guide')

