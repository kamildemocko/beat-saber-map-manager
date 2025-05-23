from loguru import logger
import flet as ft

from beat_saber_map_manager.app import App


def set_config(page: ft.Page) -> None:
    page.title = "Beat Saber Map Manager"
    page.window.resizable = False
    page.window.height = 1024
    page.window.width = 640
    page.window.maximizable = False
    page.window.center()

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.AMBER,
            secondary=ft.Colors.AMBER_200,
            tertiary=ft.Colors.AMBER_ACCENT_700,
            error=ft.Colors.RED,
        )
    )

def main(page: ft.Page) -> None:
    logger.info("Starting app..")

    set_config(page)
    app = App(page)

    logger.info("Building UI..")
    app.build_ui(page)


if __name__ == "__main__":
    ft.app(main)
