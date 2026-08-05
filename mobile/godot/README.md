# Play Mallow — Godot Android vertical slice

This is the first native client slice for Play Mallow. The existing web app remains unchanged and continues to be the live web surface.

## Included

- Portrait mobile shell at 390×844
- Home, Games, Records, Settings, and Result flows
- Versioned local save data under Godot `user://`
- Korean-first UI with an English localization layer
- Sound feedback, haptic feedback, and settings toggles
- `flash`: card-pair memory game
- `bubble`: target-sum touch game
- `trace`: touch path coordination game

## Run locally

From the repository root on Windows:

```powershell
$godot = "tools/godot/Godot_v4.7.1-stable_win64.exe"
& $godot --path mobile/godot --editor
```

For a headless project import check:

```powershell
& $godot --headless --path mobile/godot --editor --quit
```

For the game module smoke test:

```powershell
& $godot --headless --path mobile/godot --audio-driver Dummy --script res://tests/smoke.gd
```

## Structure

```text
Main.tscn                 app entry scene
scripts/Main.gd           mobile shell and navigation
scripts/SaveStore.gd      versioned local records/settings
scripts/AudioDirector.gd  procedural feedback tones and haptics
scripts/I18n.gd           Korean/English strings
scripts/ThemeKit.gd       shared mobile visual styles
games/*.gd                independent playable game modules
tests/smoke.gd            headless module instantiation check
```

The next slice should add real art/audio assets, Android back/resume handling, and device testing before porting additional games.
