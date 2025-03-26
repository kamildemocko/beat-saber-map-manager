import atexit
import os
import random
from tempfile import TemporaryDirectory, tempdir
import base64
from pathlib import Path
import shutil
from typing import Callable
import uuid

import flet as ft

from beat_sabre_map_manager.data.map_detail import MapDetail


class MapDetailUI:
    def __init__(self) -> None:
        self.content = ft.Container(
            content=ft.Column([]),
            padding=16,
        )
        self.tempdir = TemporaryDirectory()
        atexit.register(self.tempdir.cleanup)

        self._build_default_content()
    
    @staticmethod
    def _get_base64_img(path: str) -> str:
        image_path = Path(path)

        if image_path.exists():
            return base64.b64encode(image_path.read_bytes()).decode("utf-8")
        else:
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/ep2G+IAAAAASUVORK5CYII="
    
    def _open_audio_file(self, path: str) -> None:
        audio_path = Path(path)

        if audio_path.exists():
            temp_audio_path = f"{self.tempdir.name}/{uuid.uuid4()}.ogg"
            shutil.copy(audio_path, temp_audio_path)
            os.startfile(temp_audio_path)


    def build_content(self, detail: MapDetail) -> None:
        col = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Image(
                        src_base64=self._get_base64_img(detail.cover_image_filename), 
                        height=150, 
                        width=150, 
                        fit=ft.ImageFit.FIT_WIDTH, 
                        border_radius=ft.border_radius.all(8)
                    ),
                ]),
                ft.Column([
                    ft.TextField(label="Version", read_only=True, value=detail.version),
                    ft.TextField(label="BPM", read_only=True, value=f"{detail.beats_per_minute:.1f}"),
                    ft.OutlinedButton(text="Open audio file", on_click=lambda _: self._open_audio_file(detail.song_filename))
                ]),
            ]),
            ft.TextField(label="Name", read_only=True, value=detail.song_name),
            ft.Row([
                ft.TextField(label="Song author", read_only=True, value=detail.song_author_name, expand=1),
                ft.TextField(label="Map author", read_only=True, value=detail.level_author_name, expand=1),
            ]),
            ft.Row([
                *[ft.ElevatedButton(text=d.name, disabled=True) 
                for d in detail.difficulties]
            ])
        ])

        self.content.content = col

        if self.content.page:
            self.content.update()
    
    def _build_default_content(self) -> None:
        empty = MapDetail(
            _version=" ",
            _songName=" ",
            _songAuthorName=" ",
            _levelAuthorName=" ",
            _beatsPerMinute=0,
            _songFilename=" ",
            _coverImageFilename=" ",
            _difficultyBeatmapSets=[],
            difficulties=[],
        )

        self.build_content(empty)
