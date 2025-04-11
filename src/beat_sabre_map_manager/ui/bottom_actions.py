from typing import Callable
import os
from pathlib import Path

import flet as ft
import importlib.metadata

from beat_sabre_map_manager.data.new_map import add_new_map
from beat_sabre_map_manager.ui.status import StatusUI
from beat_sabre_map_manager.error_handling import with_snackbar_err_popup

VERSION = importlib.metadata.version("beat_sabre_map_manager")

class BottomActionsUI:
    def __init__(
        self, 
        game_path: Path,
        status_handle: StatusUI, 
        map_reload_callback: Callable
    ) -> None:
        self.game_path = game_path
        self.status_handle = status_handle
        self.err_decor = with_snackbar_err_popup(status_handle)
        self.map_reload_callback = map_reload_callback

        self.content = ft.Container(
            content=ft.Row([]),
            padding=16,
        )

        self.build_content()

    def build_content(self) -> None:
        col = ft.Column([
            ft.Row([
                ft.FilledButton(
                    "Install | ZIP file", 
                    tooltip="Install one or more maps in ZIP format",
                    color=ft.Colors.BLACK, 
                    icon_color=ft.Colors.BLACK,  
                    icon=ft.Icons.ADD, 
                    style=ft.ButtonStyle(
                        padding=ft.padding.all(16),
                        bgcolor={
                            ft.ControlState.DEFAULT: ft.Colors.SECONDARY,
                            ft.ControlState.HOVERED: ft.Colors.PRIMARY,
                        },
                    ),
                    on_click=self.err_decor(self._handle_add_new_map),
                ),
                ft.FilledButton(
                    "Get | Beatsaver", 
                    tooltip="Opens a www.beatsaver.com in a browser",
                    color=ft.Colors.BLACK, 
                    icon_color=ft.Colors.BLACK,  
                    icon=ft.Icons.OPEN_IN_BROWSER, 
                    style=ft.ButtonStyle(
                        padding=ft.padding.all(16),
                        bgcolor={
                            ft.ControlState.DEFAULT: ft.Colors.SECONDARY,
                            ft.ControlState.HOVERED: ft.Colors.PRIMARY,
                        },
                    ),
                    on_click=self.err_decor(lambda _: self._handle_get_maps()),
                ),
                ft.FilledButton(
                    "Create | Beatmapper", 
                    tooltip="Opens a www.beatmapper.app in a browser",
                    color=ft.Colors.BLACK, 
                    icon_color=ft.Colors.BLACK,  
                    icon=ft.Icons.INTERESTS_ROUNDED, 
                    style=ft.ButtonStyle(
                        padding=ft.padding.all(16),
                        bgcolor={
                            ft.ControlState.DEFAULT: ft.Colors.SECONDARY,
                            ft.ControlState.HOVERED: ft.Colors.PRIMARY,
                        },
                    ),
                    on_click=self.err_decor(lambda _: self._handle_crate_maps()),
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.Container(
                    content=ft.Text(VERSION, size=10, color=ft.colors.GREY_400),
                    margin=ft.margin.only(top=8),
                    alignment=ft.alignment.bottom_right,
                )
            ], alignment=ft.MainAxisAlignment.END)
        ])

        self.content = col
    
    def _handle_add_new_map(self, e: ft.ControlEvent) -> None:
        """Handle click event on the 'Add new map' button"""
        pick_files_dialog = ft.FilePicker(on_result=self.process_user_picked_files)
        e.page.overlay.append(pick_files_dialog)
        e.page.update()
        pick_files_dialog.pick_files(
            dialog_title="Select Beat Saber map files",
            allowed_extensions=["zip"],
            allow_multiple=True
        )

    def _handle_get_maps(self) -> None:
        self.status_handle.pop("Opening www.beatsaber.com")
        os.system('start "" https://beatsaver.com')

    def _handle_crate_maps(self) -> None:
        self.status_handle.pop("Opening www.beatmapper.app")
        os.system('start "" https://beatmapper.app')
    
    def process_user_picked_files(self, e: ft.FilePickerResultEvent) -> None:
        """Process the files selected in the file picker dialog"""
        if e.files is None:
            return

        results = []
        oks = 0
        for file in e.files:
            ok, result = add_new_map(self.game_path, file.path)
            if ok:
                oks += 1

            results.append(result)
        
        if results:
            self.status_handle.pop("\n".join(results))

        if oks > 0:
            self.map_reload_callback()
