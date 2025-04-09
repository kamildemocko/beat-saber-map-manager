from typing import Callable

import flet as ft


class TopActionsUI:
    def __init__(
        self, 
        map_reload_callback: Callable
    ) -> None:
        self.map_reload_callback = map_reload_callback

        self.content = ft.Container(
            content=ft.Row([]),
            padding=16,
        )

        self.build_content()

    def build_content(self) -> None:
        col = ft.Column([
                ft.Text("test"),
        ])

        self.content = col
    