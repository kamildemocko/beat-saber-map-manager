import flet as ft

from beat_sabre_map_manager.data.map_detail import MapDetail, get_base64_img, open_audio_file
from beat_sabre_map_manager.ui.status import StatusUI


class MapDetailUI:
    def __init__(self, status_handle: StatusUI) -> None:
        self.content = ft.Container(
            content=ft.Column([]),
            padding=16,
        )
        self.status_handle = status_handle

        self._build_default_content()
    
    def build_content(self, detail: MapDetail) -> None:
        col = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Image(
                        src_base64=get_base64_img(detail.cover_image_filename), 
                        height=222, 
                        width=222, 
                        fit=ft.ImageFit.FIT_WIDTH, 
                        border_radius=ft.border_radius.all(8)
                    ),
                ]),
                ft.Column([
                    ft.TextField(label="Name", read_only=True, value=detail.song_name),
                    ft.TextField(label="Song author", read_only=True, value=detail.song_author_name),
                    ft.TextField(label="Map author", read_only=True, value=detail.level_author_name),
                    ft.Row([
                        ft.TextField(label="BPM", read_only=True, value=f"{detail.beats_per_minute:.0f}", width=80),
                        ft.FilledButton(
                            "Open audio file", bgcolor=ft.Colors.BLUE_300, color=ft.Colors.BLUE_900,  
                            icon_color=ft.Colors.BLUE_900 ,icon=ft.Icons.MUSIC_NOTE, style=ft.ButtonStyle(
                                padding=ft.padding.all(16)
                            # ), on_click=lambda _: open_audio_file(detail.song_filename)),
                            ), on_click=lambda _: self._handle_open_audio(detail)),
                    ])
                ]),
            ], vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Column([
                ft.Row([
                    ft.Row([
                        *[ft.ElevatedButton(text=d.name, disabled=True) 
                        for d in detail.difficulties],
                    ]),
                    ft.FilledButton(
                        "Delete",
                        bgcolor=ft.Colors.RED, 
                        color=ft.Colors.WHITE, 
                        icon_color=ft.Colors.WHITE, 
                        icon=ft.Icons.DELETE, 
                        style=ft.ButtonStyle(
                            padding=ft.padding.all(16)
                        )),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ]),
        ])

        self.content.content = col

        if self.content.page:
            self.content.update()
    
    def _build_default_content(self) -> None:
        empty = MapDetail(
            _version=" ",
            _songName=" ",
            _songAuthorName=" ",
            _levelAuthorName=" ",
            _beatsPerMinute=0,
            _songFilename=" ",
            _coverImageFilename=" ",
            _difficultyBeatmapSets=[],
            difficulties=[],
        )

        self.build_content(empty)
    
    def _handle_open_audio(self, map_detail: MapDetail) -> None:
        open_audio_file(map_detail.song_filename)
        self.status_handle.pop(f"Opened audio file {map_detail.song_name} in default music player")
