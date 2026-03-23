from pathlib import Path

src = Path(__file__).parent.parent / 'static/images/teachers'
deleted = 0

for jpg in src.glob('*.jpeg'):
    jpg.unlink()
    print(f'Deleted {jpg.name}')
    deleted += 1

print(f'\nTotal deleted: {deleted} files')