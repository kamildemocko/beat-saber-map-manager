# Beat Saber Map Manager
## Overview
A comprehensive tool to manage and organize your Beat Saber custom maps.

## Features
- Map library organization
- Playlist management
- Map metadata viewing
- Easy installation of custom maps
- Sorting and filtering capabilities

## Screenshot
![image](https://github.com/user-attachments/assets/ea7003ed-5418-4cf8-a5c4-702393fa4b26)


## Installation from source
```cmd
git clone https://github.com/kamildemocko/beat-saber-map-manager.git
cd beat-sabre-map-manager
uv sync
```

## Running from source
```cmd
uv run python .\src\beat_sabre_map_manager\main.py
```

## Packaging
```cmd
flet pack .\src\beat_sabre_map_manager\main.py --icon assets\icon.ico --pyinstaller-build-args --onedir
```

## Licence
MIT

## Acknowledgments
- [Flet](https://flet.dev/) for the UI framework
- [uv](https://github.com/astral-sh/uv) for dependency management
- Beat Saber community for inspiration
```
