from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class _DifficultyBeatmap(BaseModel):
    difficulty: str = Field(alias="_difficulty")
    difficulty_rank: int = Field(alias="_difficultyRank")


class _MapDifficultySet(BaseModel):
    difficulty_beatmaps: list[_DifficultyBeatmap] = Field(alias="_difficultyBeatmaps")


class Difficulty(BaseModel):
    name: str
    rank: int


class MapDetail(BaseModel):
    version: str = Field(alias="_version")
    song_name: str = Field(alias="_songName")
    song_author_name: str = Field(alias="_songAuthorName")
    level_author_name: str = Field(alias="_levelAuthorName")
    beats_per_minute: float = Field(alias="_beatsPerMinute")
    song_filename: str = Field(alias="_songFilename")
    cover_image_filename: str = Field(alias="_coverImageFilename")
    difficulty_sets: list[_MapDifficultySet] = Field(alias="_difficultyBeatmapSets")
    difficulties: list[Difficulty] = []
    
    def model_post_init(self, _context: Any) -> None:
        for dset in self.difficulty_sets:
            self.difficulties.extend(
                [Difficulty(name=d.difficulty, rank=d.difficulty_rank)
                for d in dset.difficulty_beatmaps]
            )

        del self.difficulty_sets
            

def get_map_detail(map_path: Path) -> MapDetail:
    info_file_path = map_path.joinpath("info.dat")
    with info_file_path.open("r", encoding="utf-8") as file:
        parsed = MapDetail.model_validate_json(file.read())
        parsed.song_filename = map_path.joinpath(parsed.song_filename).as_posix()
        parsed.cover_image_filename = map_path.joinpath(parsed.cover_image_filename).as_posix()

        return parsed
    