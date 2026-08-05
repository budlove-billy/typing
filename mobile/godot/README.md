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

## Android debug APK

The repository uses a project-local Android toolchain so the web app and native
client can be built side by side without changing the machine-wide setup.

Prerequisites:

- Godot 4.7.1 at `tools/godot/`
- Microsoft OpenJDK 17 at `tools/jdk17/`
- Android SDK at `tools/android/sdk/`
- Godot 4.7.1 export templates installed under the Godot user data directory

The current machine already has the editor settings and templates configured.
To rebuild the debug APK from the repository root:

```powershell
& .\mobile\godot\build-android.ps1
```

Output:

```text
mobile/godot/build/playmallow-debug.apk
```

The APK is arm64, portrait-oriented, package `com.playmallow.mallow`, version
`0.1.0` (version code `1`). A release APK/AAB still requires a project-owned
non-debug keystore; do not reuse the generated debug keystore for Google Play.

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
