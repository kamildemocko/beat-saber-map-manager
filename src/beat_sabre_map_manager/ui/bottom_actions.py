import flet as ft

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
                ft.FilledButton("Remove this map", bgcolor=ft.Colors.RED ,color=ft.Colors.WHITE, icon_color=ft.Colors.WHITE ,icon="delete", style=ft.ButtonStyle(
                        padding=ft.padding.all(16)
                    )),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.Container(
                    content=ft.Text("v0.1.0", size=10, color=ft.colors.GREY_400),
                    margin=ft.margin.only(top=8),
                    alignment=ft.alignment.bottom_right,
                )
            ], alignment=ft.MainAxisAlignment.END)
        ])

        self.content = col
