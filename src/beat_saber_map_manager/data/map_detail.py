import atexit
import base64
import os
import uuid
from tempfile import TemporaryDirectory
import shutil
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError


tempdir = TemporaryDirectory()
atexit.register(tempdir.cleanup)


class _DifficultyBeatmap(BaseModel):
    difficulty: str = Field(alias="_difficulty")
    difficulty_rank: int = Field(alias="_difficultyRank")


class _MapDifficultySet(BaseModel):
    difficulty_beatmaps: list[_DifficultyBeatmap] = Field(alias="_difficultyBeatmaps")


class Difficulty(BaseModel):
    name: str
    rank: int

    def __hash__(self) -> int:
        return hash((self.name, self.rank))


class MapDetail(BaseModel):
    """Class representing a Beat Saber map detail."""
    version: str = Field(alias="_version")
    song_name: str = Field(alias="_songName")
    song_author_name: str = Field(alias="_songAuthorName")
    level_author_name: str = Field(alias="_levelAuthorName")
    beats_per_minute: float = Field(alias="_beatsPerMinute")
    song_filename: str = Field(alias="_songFilename")
    cover_image_filename: str = Field(alias="_coverImageFilename")
    difficulty_sets: list[_MapDifficultySet] = Field(alias="_difficultyBeatmapSets")
    difficulties: list[Difficulty] = []
    
    @staticmethod
    def sort_difficulty(difficulties: list[Difficulty]) -> list[Difficulty]:
        """
        Sort the difficulties in the correct order. The order is:
        easy, normal, hard, expert, expertplus. The order is case insensitive.

        Args:
            difficulties (list[Difficulty]): List of difficulties to sort.

        Returns:
            list[Difficulty]: Sorted list of difficulties.
        """
        correct = ["easy", "normal", "hard", "expert", "expertplus"]
        output: list[Difficulty] = []

        for pol in correct:
            for d in difficulties:
                if pol != d.name.lower():
                    continue
                
                output.append(d)
        
        return output
            
    def model_post_init(self, _context: Any) -> None:
        for dset in self.difficulty_sets:
            self.difficulties.extend(
                (Difficulty(name=d.difficulty, rank=d.difficulty_rank)
                for d in dset.difficulty_beatmaps)
            )
        
        self.difficulties = list(set(self.difficulties))
        self.difficulties = self.sort_difficulty(self.difficulties)

        del self.difficulty_sets
    
    @classmethod
    def get_empty_map_detail(cls) -> "MapDetail":
        return MapDetail(
            _version="",
            _songName="",
            _songAuthorName="",
            _levelAuthorName="",
            _beatsPerMinute=0.0,
            _songFilename="",
            _coverImageFilename="",
            _difficultyBeatmapSets=[]
        )

def get_map_detail(map_path: Path) -> tuple[MapDetail, str]:
    """
    Get the map detail from the map path. The map path is the path to the
    map folder. The map folder contains the info.dat file. The info.dat
    file contains the map detail. The map detail is parsed and returned
    as a MapDetail object. If the map detail is not valid, an empty
    MapDetail object is returned and an error message is returned.

    Args:
        map_path (Path): Path to the map folder.

    Returns:
        tuple[MapDetail, str]: Tuple containing the MapDetail object 
        and an error message.
    """
    info_file_path = map_path.joinpath("info.dat")
    if not info_file_path.exists:
        return MapDetail.get_empty_map_detail(), ""

    try:
        with info_file_path.open("r", encoding="utf-8") as file:
            parsed = MapDetail.model_validate_json(file.read())
            parsed.song_filename = map_path.joinpath(parsed.song_filename).as_posix()
            parsed.cover_image_filename = map_path.joinpath(parsed.cover_image_filename).as_posix()
            parsed.song_name = parsed.song_name.strip().title()
            parsed.song_author_name = parsed.song_author_name.strip().title()

            return parsed, ""

    except ValidationError:
        return MapDetail.get_empty_map_detail(), "unsupported map"
    


def get_base64_img(path: str) -> str:
    """
    Get the base64 encoded image from the path. The path is the path to
    the image file. The image file is read and encoded to base64. The
    base64 encoded image is returned as a string. If the image file does
    not exist, a default image is returned. The default image is a 1x1
    transparent PNG image.

    Args:
        path (str): Path to the image file.

    Returns:
        str: Base64 encoded image string.
    """
    image_path = Path(path)

    if image_path.exists():
        return base64.b64encode(image_path.read_bytes()).decode("utf-8")
    else:
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/ep2G+IAAAAASUVORK5CYII="

def open_audio_file(path: str) -> None:
    """
    Open the audio file in the default audio player. The audio file is
    copied to a temporary directory and opened. The temporary directory
    is deleted when the program exits. 

    Args:
        path (str): Path to the audio file.
    """
    audio_path = Path(path)

    if audio_path.exists():
        temp_audio_path = f"{tempdir.name}/{uuid.uuid4()}.ogg"
        shutil.copy(audio_path, temp_audio_path)
        os.startfile(temp_audio_path)