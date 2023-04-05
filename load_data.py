from pathlib import Path

from equipment import Equipment

path: Path = Path('data/equipment.json')
try:
    equipment = Equipment.parse_file(path)
except Exception as e:
    print(e)
