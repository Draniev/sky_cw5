from pathlib import Path

from arena.equipment import Equipment

path: Path = Path('data/equipment.json')
try:
    equipment = Equipment.parse_file(path)
except Exception as e:
    print(e)
