from result import Result, Ok, Err
from pathlib import Path
import winreg


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
        """tries to get the steam install path from the registry

        Returns:
            Result[Path, str]: Ok(Path) if successful, Err(str) if not
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, 
                r"SOFTWARE\WOW6432Node\Valve\Steam", 
                access=winreg.KEY_READ
            )

            install_path = winreg.QueryValueEx(key, r"InstallPath")

            return Ok(Path(install_path[0]))

        except FileNotFoundError:
            return Err("Steam install path not found")

    @staticmethod
    def _get_steamapps_path() -> Result[Path, str]:
        ...
