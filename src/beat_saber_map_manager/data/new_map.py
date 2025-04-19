from pathlib import Path
import zipfile


def add_new_map(game_path: Path, path: str) -> tuple[bool, str]:
    """
    Adds a new map to the game path. The map must be in a zip file.

    Args:
        game_path (Path): Path to the game folder.
        path (str): Path to the zip file.

    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating 
        success or failiure and error message
    """
    ppath = Path(path)
    if not zipfile.is_zipfile(ppath):
        return False, f"Map {ppath.stem} is not a valid map!"

    copy_to_folder = game_path.joinpath(ppath.stem)
    if copy_to_folder.exists():
        return False, f"Map {ppath.stem} is already installed!"
        
    copy_to_folder.mkdir()
    with zipfile.ZipFile(path, "r") as file:
        file.extractall(copy_to_folder)
    
    return True, f"Map {ppath.stem} successfully installed!"
        