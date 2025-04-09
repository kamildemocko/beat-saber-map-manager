from loguru import logger
import flet as ft

from beat_sabre_map_manager.app import App


def set_config(page: ft.Page) -> None:
    page.title = "Beat Sabre Map Manager"
    page.window.resizable = False
    page.window.height = 1024
    page.window.width = 640
    page.window.center()

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.AMBER,
            secondary=ft.colors.AMBER_200,
            error=ft.colors.RED,
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
