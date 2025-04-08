import os
import urllib.parse
from typing import Callable
import shutil

import flet as ft

from beat_sabre_map_manager.data.map_detail import MapDetail, get_base64_img, open_audio_file
from beat_sabre_map_manager.data.maps import BSMap
from beat_sabre_map_manager.ui.status import StatusUI
from beat_sabre_map_manager.error_handling import with_snackbar_err_popup


class MapDetailUI:
    def __init__(
        self, 
        status_handle: StatusUI, 
        map_reload_callback: Callable
    ) -> None:
        self.content = ft.Container(
            content=ft.Column([]),
            padding=16,
        )
        self.status_handle = status_handle
        self.err_decor = with_snackbar_err_popup(status_handle)
        self.map_reload_callback = map_reload_callback

        self._build_default_content()
    
    def build_content(self, bsmap: BSMap | None) -> None:
        if bsmap is None:
            return

        col = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Image(
                        src_base64=get_base64_img(bsmap.detail.cover_image_filename), 
                        height=222, 
                        width=222, 
                        fit=ft.ImageFit.FIT_WIDTH, 
                        border_radius=ft.border_radius.all(8)
                    ),
                ]),
                ft.Column([
                    ft.TextField(label="Name", read_only=True, value=bsmap.detail.song_name),
                    ft.TextField(label="Song author", read_only=True, value=bsmap.detail.song_author_name),
                    ft.TextField(label="Map author", read_only=True, value=bsmap.detail.level_author_name),
                    ft.Row([
                        ft.TextField(label="BPM", read_only=True, value=f"{bsmap.detail.beats_per_minute:.0f}", width=80),
                        ft.IconButton(
                            tooltip="Play in external player", bgcolor=ft.Colors.BLUE_300,
                            icon_color=ft.Colors.BLUE_900 ,icon=ft.Icons.MUSIC_NOTE, style=ft.ButtonStyle(
                                padding=ft.padding.all(8)
                            ), on_click=self.err_decor(lambda _: self._handle_open_audio(bsmap.detail))
                        ),
                        ft.IconButton(
                            tooltip="Open map folder location", bgcolor=ft.Colors.AMBER_300,
                            icon_color=ft.Colors.BLACK ,icon=ft.Icons.FOLDER_OPEN, style=ft.ButtonStyle(
                                padding=ft.padding.all(8)
                            ), on_click=self.err_decor(lambda _: self._handle_open_folder(bsmap))
                        ),
                        ft.IconButton(
                            tooltip="Search YouTube", bgcolor=ft.Colors.RED_ACCENT_700,
                            icon_color=ft.Colors.WHITE ,icon=ft.Icons.YOUTUBE_SEARCHED_FOR_ROUNDED, style=ft.ButtonStyle(
                                padding=ft.padding.all(8)
                            ), on_click=self.err_decor(lambda _: self._handle_search_youtube(bsmap))
                        ),
                        ft.Container(expand=1),
                        ft.IconButton(
                            tooltip="Delete map", bgcolor=ft.Colors.RED,
                            icon_color=ft.Colors.WHITE ,icon=ft.Icons.DELETE, style=ft.ButtonStyle(
                                padding=ft.padding.all(8)
                            ), on_click=self.err_decor(lambda _: self._handle_delete_map(bsmap))
                        ),
                    ]),
                ], expand=1),
            ], vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Column([
                ft.Row([
                    ft.Row([
                        *[ft.ElevatedButton(text=d.name, disabled=True) 
                        for d in bsmap.detail.difficulties],
                    ]),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ]),
        ])

        self.content.content = col

        if self.content.page:
            self.content.update()
    
    def _build_default_content(self) -> None:
        self.build_content(None)
    
    def _handle_open_audio(self, map_detail: MapDetail) -> None:
        open_audio_file(map_detail.song_filename)
        self.status_handle.pop(f"Opened audio file {map_detail.song_name} in default music player")

    def _handle_search_youtube(self, bsmap: BSMap) -> None:
        self.status_handle.pop(f"Search YouTube for map {bsmap.title}")
        os.system(f'start "" https://www.youtube.com/results?search_query={urllib.parse.quote_plus(bsmap.title)}')

    def _handle_open_folder(self, bsmap: BSMap) -> None:
        self.status_handle.pop(f"Opening map folder {bsmap.name}")
        os.system(f'start explorer.exe {bsmap.path}')

    def _handle_delete_map(self, bsmap: BSMap) -> None:
        shutil.rmtree(bsmap.path)
        self.status_handle.pop(f"Removed map {bsmap.title}")
        self.map_reload_callback()
