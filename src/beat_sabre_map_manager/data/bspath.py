from pathlib import Path
import winreg
import re


class BSPath:
    def __init__(self):
        self.path: Path | None = None
    
    def find_game_path(self) -> tuple[Path, str]:
        if self.path is not None:
            return self.path, ""

        found_paths = []

        steam_root_path, err = self._get_steam_path()
        if err != "":
            return Path(), "steam path not found"
        
        steam_steamapps_paths = self._get_steamapps_path(steam_root_path)

        for path in steam_steamapps_paths:
            search_folder = path.joinpath(r"steamapps\common\Beat Saber")

            if search_folder.exists():
                found_paths.append(search_folder)
        
        match len(found_paths):
            case 0: 
                return Path(), "game folder not found"
            case x if x > 1:
                return Path(), "multiple game folders were found"
            case _:
                self.path = (Path(found_paths[0])
                             .joinpath("Beat Saber_Data")
                             .joinpath("CustomLevels"))
                return self.path, ""
        
        

    @staticmethod
    def _get_steam_path() -> tuple[Path, str]:
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

            return Path(install_path[0]), ""

        except FileNotFoundError:
            return Path(), "Steam install path not found"

    @staticmethod
    def _get_steamapps_path(steam_root_path: Path) -> list[Path]:
        """tries to get the steamapps path - or more from config file in steam folder

        Args:
            steam_root_path (Path): path to the steam root folder

        Returns:
            list[Path]: list of paths to steamapps folders
        """
        steam_conf_file = steam_root_path.joinpath(r"steamapps\libraryfolders.vdf")
        file_content = steam_conf_file.read_text()

        pattern = re.compile(r'"path"\s+"(.*)"')
        matches = pattern.findall(file_content)
        matches_paths = [Path(m) for m in matches]

        return [m for m in matches_paths if m.exists()]
