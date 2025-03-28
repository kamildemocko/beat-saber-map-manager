import flet as ft
import importlib.metadata

from loguru import logger

VERSION = importlib.metadata.version("beat_sabre_map_manager")

class BottomActionsUI:
    def __init__(self) -> None:
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
                    on_click=self._handle_add_map,
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
    
    def _handle_add_map(self, e: ft.ControlEvent) -> None:
        logger.info("Adding map..")
