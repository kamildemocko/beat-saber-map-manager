from pathlib import Path
import zipfile

from beat_sabre_map_manager.data.bspath import BSPath


def add_new_map(path: str) -> str:
    ppath = Path(path)
    if not zipfile.is_zipfile(ppath):
        return f"map {ppath.stem} is not a valid map!"

    root = BSPath().find_game_path()

    copy_to_folder = root.joinpath(ppath.stem)
    if copy_to_folder.exists():
        return f"map {ppath.stem} is already installed!"
        
    copy_to_folder.mkdir()
    with zipfile.ZipFile(path, "r") as file:
        file.extractall(copy_to_folder)
    
    return ""
        