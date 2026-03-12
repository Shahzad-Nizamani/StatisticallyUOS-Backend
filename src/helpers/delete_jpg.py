from pathlib import Path

src = Path('src/static/images/teachers')
deleted = 0

for jpg in src.glob('*.jpg'):
    jpg.unlink()
    print(f'Deleted {jpg.name}')
    deleted += 1

print(f'\nTotal deleted: {deleted} files')