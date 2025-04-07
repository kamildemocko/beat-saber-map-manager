import flet as ft
import importlib.metadata

from beat_sabre_map_manager.data.new_map import add_new_map
from beat_sabre_map_manager.ui.status import StatusUI

VERSION = importlib.metadata.version("beat_sabre_map_manager")

class BottomActionsUI:
    def __init__(self, status_handle: StatusUI) -> None:
        self.status_handle = status_handle

        self.content = ft.Container(
            content=ft.Row([]),
            padding=16,
        )

        self.build_content()

    def build_content(self) -> None:
        col = ft.Column([
            ft.Row([
                ft.FilledButton(
                    "Add new map", 
                    bgcolor=ft.Colors.BLUE_200, 
                    color=ft.Colors.BLUE_900, 
                    icon_color=ft.Colors.BLUE_900,  
                    icon=ft.Icons.ADD, 
                    style=ft.ButtonStyle(
                        padding=ft.padding.all(16)
                    ),
                    on_click=self._handle_add_new_map,
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
    
    def process_user_picked_files(self, e: ft.FilePickerResultEvent) -> None:
        """Process the files selected in the file picker dialog"""
        if e.files is None:
            return

        results = []
        for file in e.files:
            result = add_new_map(file.path)
            results.append(result)
        
        if results:
            self.status_handle.pop("\n".join(results))
