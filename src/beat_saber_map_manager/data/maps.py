from pathlib import Path
from dataclasses import dataclass
import re

from loguru import logger

from beat_saber_map_manager.data.map_detail import get_map_detail, MapDetail

@dataclass
class BSMap:
    """Class representing a Beat Saber map."""
    filename: str
    name: str
    path: Path
    detail: MapDetail
    title: str
    uid: str

class Maps:
    def __init__(self, game_path: Path):
        self.game_path = game_path
        self.maps: list[BSMap] = []
    
    @staticmethod
    def _get_name_if_valid(name: str) -> str | None:
        """
        Get the name of the map if it is valid. A valid name is one that
        starts with 1-6 alphanumeric characters followed by a space and
        a set of parentheses. The contents of the parentheses are returned.
        If the name is not valid, None is returned.

        Args:
            name (str): The name of the map.

        Returns:
            str | None: Output or none if invalid.
        """
        match = re.search(r"^\w{1,6}\s{1}\((.*)\)$", name)
        return None if match is None else match.group(1)
    
    def reload_maps(self) -> None:
        self.maps = []
        self.load_maps()
    
    def load_maps(self) -> None:
        """
        Load all maps from the game path. The maps are loaded from the
        Beat Saber game directory. The maps are loaded into a list of
        BSMap objects. The maps are sorted by name.
        """
        logger.info("Loading maps..")

        for mapdir in self.game_path.glob("*"):
            if not mapdir.is_dir():
                continue

            name = self._get_name_if_valid(mapdir.name)
            if name is None:
                continue

            detail, err = get_map_detail(mapdir)
            if err != "":
                continue

            title = f"{detail.song_author_name} - {detail.song_name}"

            self.maps.append(
                BSMap(
                    filename=mapdir.name, 
                    name=name,
                    path=mapdir,
                    detail=detail,
                    title=title,
                    uid=mapdir.name.split(" ")[0],
                )
            )
    
    def sort_maps_interpret_asc(self, reverse: bool = False) -> None:
        """
        Sort the maps by the song author name. The maps are sorted in
        ascending order by default.
        """
        self.maps = sorted(self.maps, key=lambda x: x.detail.song_author_name, reverse=reverse)

    def sort_maps_song_asc(self, reverse: bool = False) -> None:
        """
        Sort the maps by the song title name. The maps are sorted in
        ascending order by default.
        """
        self.maps = sorted(self.maps, key=lambda x: x.detail.song_name, reverse=reverse)
