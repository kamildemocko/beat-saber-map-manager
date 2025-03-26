from pathlib import Path
from dataclasses import dataclass

@dataclass
class BSPath:
    name: str
    path: Path
    ...

class Maps:
    def __init__(self):
        self.maps: list[BSPath] = []
    
    def _load_maps(self) -> None:
        ...