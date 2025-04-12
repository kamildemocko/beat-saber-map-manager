# Beat Saber Map Manager
## Overview
A comprehensive tool to manage and organize your Beat Saber custom maps.

## Features
- View your custom maps
- Play, show folder or open Beatsaver web
- Easily install maps
- Sort maps by interpret or song name

## Screenshot
![image](https://github.com/user-attachments/assets/ea7003ed-5418-4cf8-a5c4-702393fa4b26)


## Install with installer
Download and run the installer from the [latest release](https://github.com/kamildemocko/beat-saber-map-manager/releases/latest) page.

## Installation from source

### Prerequisities
`uv`
- package manager

### Install
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
flet pack .\src\beat_sabre_map_manager\main.py --icon assets\icon.ico --pyinstaller-build-args --onedir --name "Beat Sabre Map Manager"
```

## Licence
MIT

## Acknowledgments
- [Flet](https://flet.dev/) for the UI framework
- [uv](https://github.com/astral-sh/uv) for dependency management
- [Inno Setup Script Wizard](https://jrsoftware.org/isinfo.php) for creating the installer
- Beat Saber community for inspiration
```
