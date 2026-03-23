from PIL import Image
from pathlib import Path

# Path relative to the script file (works from any directory)
src = Path(__file__).parent.parent / 'static/images/teachers'

for jpg in src.glob('*.jpeg'):
    img = Image.open(jpg)
    img.save(jpg.with_suffix('.webp'), 'webp', quality=85)
    print(f'Converted {jpg.name}')

print(f'Done. Looked in: {src}')