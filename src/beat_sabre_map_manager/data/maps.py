from result import Result, Ok, Err
from pathlib import Path
from dataclasses import dataclass

from result import Result

@dataclass
class BSPath:
    name: str
    path: Path
    ...

class Maps:
    def __init__(self):
        self.maps: list[BSPath] = []
    
    def _load_maps(self) -> Result[None, str]:
        ...