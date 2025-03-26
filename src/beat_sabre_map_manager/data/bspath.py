from result import Result, Ok, Err
from pathlib import Path


class BSPath:
    def __init__(self):
        self.root: Path
        self.path: Path
    
    def find_game_path(self) -> Result[Path, str]:
        if self.path is None:
            ...
        
        return Ok(self.path)
        
        

    @staticmethod
    def _get_steam_path() -> Result[Path, str]:
        ...

    @staticmethod
    def _get_steamapps_path() -> Result[Path, str]:
        ...
