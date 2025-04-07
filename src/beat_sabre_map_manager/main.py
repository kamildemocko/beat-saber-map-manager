from loguru import logger
import flet as ft

from beat_sabre_map_manager.app import App


def set_config(page: ft.Page) -> None:
    page.title = "Beat Sabre Map Manager"
    page.window.resizable = False
    page.window.height = 845
    page.window.width = 660
    page.window.center()

def main(page: ft.Page) -> None:
    logger.info("Starting app..")

    set_config(page)
    app = App(page)

    logger.info("Building UI..")
    app.build_ui(page)


if __name__ == "__main__":
    ft.app(main)
