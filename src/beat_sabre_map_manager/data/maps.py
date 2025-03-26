from pathlib import Path
from dataclasses import dataclass
import re

from beat_sabre_map_manager.data.bspath import BSPath

@dataclass
class BSMap:
    filename: str
    name: str
    path: Path

class Maps:
    def __init__(self):
        self.maps: list[BSMap] = []
    
    def _get_name_if_valid(self, name: str) -> str | None:
        match = re.search(r"^\w{4}\s{1}\((.*)\)$", name)
        return None if match is None else match.group(1)
    
    def load_maps(self) -> None:
        game_path = BSPath().find_game_path()
        for mapdir in game_path.glob("*"):
            if not mapdir.is_dir():
                continue

            name = self._get_name_if_valid(mapdir.name)
            if name is None:
                continue
                
            print(mapdir)

            self.maps.append(
                BSMap(
                    filename=mapdir.name, 
                    name=name,
                    path=mapdir,
                )
            )