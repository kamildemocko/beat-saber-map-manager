import os
import urllib.parse
from typing import Callable
import shutil

import flet as ft

from beat_saber_map_manager.data.map_detail import MapDetail, get_base64_img, open_audio_file
from beat_saber_map_manager.data.maps import BSMap
from beat_saber_map_manager.ui.status import StatusUI
from beat_saber_map_manager.error_handling import with_snackbar_err_popup


class MapDetailUI:
    """
    UI component for displaying map details.
    This class is responsible for creating the UI for the map details,
    including the cover image, song name, author names, and action buttons.
    It also handles the actions for opening the audio file, opening the map folder,
    opening the map on beatsaver.com, searching YouTube, and deleting the map.
    """
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
                        ft.TextField(label="BPM", read_only=True, value=f"{bsmap.detail.beats_per_minute:.0f}", width=70),
                        ft.IconButton(
                            tooltip="Play in external audio player", 
                            icon_color=ft.Colors.BLACK ,icon=ft.Icons.MUSIC_NOTE, style=ft.ButtonStyle(
                                padding=ft.padding.all(8),
                                bgcolor={
                                    ft.ControlState.DEFAULT: ft.Colors.SECONDARY,
                                    ft.ControlState.HOVERED: ft.Colors.PRIMARY,
                                },
                            ), on_click=self.err_decor(lambda _: self._handle_open_audio(bsmap.detail))
                        ),
                        ft.IconButton(
                            tooltip="Open map folder location", 
                            icon_color=ft.Colors.BLACK ,icon=ft.Icons.FOLDER_OPEN, style=ft.ButtonStyle(
                                padding=ft.padding.all(8),
                                bgcolor={
                                    ft.ControlState.DEFAULT: ft.Colors.SECONDARY,
                                    ft.ControlState.HOVERED: ft.Colors.PRIMARY,
                                },
                            ), on_click=self.err_decor(lambda _: self._handle_open_folder(bsmap))
                        ),
                        ft.IconButton(
                            tooltip="Open map on www.beatsaver.com", 
                            icon_color=ft.Colors.BLACK ,icon=ft.Icons.CHROME_READER_MODE, style=ft.ButtonStyle(
                                padding=ft.padding.all(8),
                                bgcolor={
                                    ft.ControlState.DEFAULT: ft.Colors.SECONDARY,
                                    ft.ControlState.HOVERED: ft.Colors.PRIMARY,
                                },
                            ), on_click=self.err_decor(lambda _: self._handle_open_beatsaver(bsmap))
                        ),
                        ft.IconButton(
                            tooltip="Search YouTube", 
                            icon_color=ft.Colors.BLACK ,icon=ft.Icons.MANAGE_SEARCH, style=ft.ButtonStyle(
                                padding=ft.padding.all(8),
                                bgcolor={
                                    ft.ControlState.DEFAULT: ft.Colors.SECONDARY,
                                    ft.ControlState.HOVERED: ft.Colors.PRIMARY,
                                },
                            ), on_click=self.err_decor(lambda _: self._handle_search_youtube(bsmap))
                        ),
                        ft.Container(expand=1),
                        ft.IconButton(
                            tooltip="Delete map", 
                            icon_color=ft.Colors.WHITE ,icon=ft.Icons.DELETE, style=ft.ButtonStyle(
                                padding=ft.padding.all(8),
                                bgcolor={
                                    ft.ControlState.DEFAULT: ft.Colors.RED,
                                    ft.ControlState.HOVERED: ft.Colors.RED_900,
                                },
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
        """
        Open the audio file in the default music player.

        Args:
            map_detail (MapDetail): Map detail object containing the song filename.
        """
        open_audio_file(map_detail.song_filename)
        self.status_handle.pop(f"Opened audio file {map_detail.song_name} in default music player")

    def _handle_open_beatsaver(self, bsmap: BSMap) -> None:
        """
        Open the map on beatsaver.com.

        Args:
            bsmap (BSMap): Map to open.
        """
        self.status_handle.pop(f"Open map on www.beatsaver.com with id: {bsmap.uid}")
        os.system(f'start "" https://beatsaver.com/maps/{bsmap.uid}')

    def _handle_search_youtube(self, bsmap: BSMap) -> None:
        """
        Search YouTube for the map.

        Args:
            bsmap (BSMap): Map to search for.
        """
        self.status_handle.pop(f"Search YouTube for map {bsmap.title}")
        os.system(f'start "" https://www.youtube.com/results?search_query={urllib.parse.quote_plus(bsmap.title)}')

    def _handle_open_folder(self, bsmap: BSMap) -> None:
        """
        Open map folder in file explorer.

        Args:
            bsmap (BSMap): Map to open.
        """
        self.status_handle.pop(f"Opening map folder {bsmap.name}")
        os.system(f'start explorer.exe {bsmap.path}')

    def _handle_delete_map(self, bsmap: BSMap) -> None:
        """
        Delete map from disk and remove it from the list of maps.

        Args:
            bsmap (BSMap): Map to delete.
        """
        shutil.rmtree(bsmap.path)
        self.status_handle.pop(f"Removed map {bsmap.title}")
        self.map_reload_callback()
