from pathlib import Path
import winreg
import re

from loguru import logger


class BSPath:
    def __init__(self):
        self.path: Path | None = None
    
    def find_game_path(self) -> tuple[Path, str]:
        """
        method that returns existing folder where the game should be installed
        checks both Steam and Oculus paths

        Returns:
            tuple[Path, str]: path to the game folder, errro if ocurred
        """
        if self.path is not None:
            return self.path, ""

        logger.info("Finding game path..")

        found_paths_steam = self._find_game_path_steam()
        found_paths_oculus = self._find_game_path_oculus()
        found_paths: list[Path] = found_paths_steam + found_paths_oculus

        match len(found_paths):
            case 0: 
                return Path(), "game folder not found"
            case x if x > 1:
                return Path(), "multiple game folders were found"
            case _:
                self.path = (found_paths[0]
                             .joinpath("Beat Saber_Data")
                             .joinpath("CustomLevels"))
                return self.path, ""
    
    def _find_game_path_steam(self) -> list[Path]:
        """finds game paths for Steam installation

        Returns:
            list[Path]: list of paths to lib
        """
        found_paths = []

        steam_root_path, err = self._get_steam_path()
        if err != "":
            return []
        
        steam_steamapps_paths = self._get_steamapps_path(steam_root_path)

        for path in steam_steamapps_paths:
            search_folder = path.joinpath(r"steamapps\common\Beat Saber")

            if search_folder.exists():
                found_paths.append(search_folder)
        
        return found_paths

    def _find_game_path_oculus(self) -> list[Path]:
        """finds game paths for Oculus installation

        Returns:
            list[Path]: list of paths to lib
        """
        found_paths = []

        oculus_libraries, err = self._get_oculus_libraries()
        if err != "":
            return []

        for path in oculus_libraries:
            search_folder = path.joinpath(r"Software/Beat Saber")

            if search_folder.exists():
                found_paths.append(search_folder)
        
        return found_paths

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

    @staticmethod
    def _get_oculus_libraries() -> tuple[list[Path], str]:
        """tries to get the oculus libraries paths

        Returns:
            tuple[list[Path], str]: list of paths to libraries, error if occured
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                r"Software\Oculus VR, LLC\Oculus\Libraries", 
                access=winreg.KEY_READ
            )

            lib_ids: list[str] = []
            for i in range(0, 100):
                try:
                    lib_ids.append(winreg.EnumKey(key, i))
                except OSError:
                    break
            
            libraries: list[str] = []
            for lib in lib_ids:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, 
                    fr"Software\Oculus VR, LLC\Oculus\Libraries\{lib}", 
                    access=winreg.KEY_READ
                )
                lib_path = winreg.QueryValueEx(key, "OriginalPath")
                libraries.append(lib_path[0])

            return [Path(li) for li in libraries], ""

        except FileNotFoundError:
            return [], "no Oculus library path found"
