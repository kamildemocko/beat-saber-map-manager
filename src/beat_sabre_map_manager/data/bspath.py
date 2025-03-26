from pathlib import Path
import winreg
import re


class BSPathError(Exception):
    ...


class BSPath:
    def __init__(self):
        self.root: Path
        self.path: Path
    
    def find_game_path(self) -> Path:
        if self.path is None:
            ...
        
        return self.path
        
        

    @staticmethod
    def _get_steam_path() -> Path:
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

            return Path(install_path[0])

        except FileNotFoundError as fnfe:
            raise BSPathError("Steam install path not found") from fnfe

    @staticmethod
    def _get_steamapps_path(steam_root_path: Path) -> list[Path]:
        """tries to get the steamapps path - or more from config file in steam folder

        Args:
            steam_root_path (Path): path to the steam root folder

        Returns:
            list[Path]: list of paths to steamapps folders
        """
        steam_conf_file = steam_root_path.join(r"steamapps\libraryfolders.vdf")
        file_content = steam_conf_file.read_text()

        pattern = re.compile(r'"path"\s+"(.*)"')
        matches = pattern.findall(file_content)
        matches_paths = [Path(m) for m in matches]

        return [m for m in matches_paths if m.exists()]
