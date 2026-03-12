from PIL import Image
from pathlib import Path

src = Path('src/static/images/teachers')
for jpg in src.glob('*.jpg'):
    img = Image.open(jpg)
    img.save(jpg.with_suffix('.webp'), 'webp', quality=85)
    print(f'Converted {jpg.name}')