import flet as ft

from beat_sabre_map_manager.data.map_detail import MapDetail


class MapDetailUI:
    def __init__(self) -> None:
        self.content: ft.Container | None = None

        self._build_default_content()
    
    def build_content(self, detail: MapDetail) -> None:
        print(detail.cover_image_filename)

        col = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Image(src=f"file://{detail.cover_image_filename}", height=150, width=150, fit=ft.ImageFit.CONTAIN),
                ]),
                ft.Column([
                    ft.TextField(label="Version", read_only=True, value=detail.version),
                    ft.TextField(label="BPM", read_only=True, value=f"{detail.beats_per_minute:.1f}"),
                    ft.Audio(src=f"file://{detail.song_filename}")
                ]),
            ]),
            ft.TextField(label="Name", read_only=True, value=detail.song_name),
            ft.TextField(label="Song author", read_only=True, value=detail.song_author_name),
            ft.TextField(label="Map author", read_only=True, value=detail.level_author_name),
            ft.Row([
                *[ft.ElevatedButton(text=d.name, disabled=True) 
                for d in detail.difficulties]
            ])
        ])

        self.content = ft.Container(
            content=col,
            padding=16,
        )
    
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
