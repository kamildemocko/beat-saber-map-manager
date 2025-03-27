import flet as ft

from beat_sabre_map_manager.data.map_detail import MapDetail, get_base64_img, open_audio_file


class MapDetailUI:
    def __init__(self) -> None:
        self.content = ft.Container(
            content=ft.Column([]),
            padding=16,
        )

        self._build_default_content()
    
    def build_content(self, detail: MapDetail) -> None:
        col = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Image(
                        src_base64=get_base64_img(detail.cover_image_filename), 
                        height=265, 
                        width=265, 
                        fit=ft.ImageFit.FIT_WIDTH, 
                        border_radius=ft.border_radius.all(8)
                    ),
                ]),
                ft.Column([
                    ft.TextField(label="Name", read_only=True, value=detail.song_name),
                    ft.TextField(label="Song author", read_only=True, value=detail.song_author_name),
                    ft.TextField(label="Map author", read_only=True, value=detail.level_author_name),
                    ft.TextField(label="BPM", read_only=True, value=f"{detail.beats_per_minute:.1f}"),
                    ft.OutlinedButton(text="Open audio file", on_click=lambda _: open_audio_file(detail.song_filename)),
                ]),
            ]),
            ft.Row([
                *[ft.ElevatedButton(text=d.name, disabled=True) 
                for d in detail.difficulties]
            ], alignment=ft.MainAxisAlignment.START, expand=1)
        ], spacing=50)

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
