# Play Mallow — Godot Android native client

The native client contains the full non-fortune brain-game catalog. The existing web app remains unchanged and continues to be the live web surface.

## Included

- Portrait mobile shell at 390×844
- Home, Games, Records, Settings, and Result flows
- Versioned local save data under Godot `user://`
- Korean-first UI with an English localization layer
- Sound feedback, haptic feedback, and settings toggles
- First-launch four-skill baseline assessment with a skippable fallback
- Local skill scores, rolling updates, and explainable daily recommendations
- Unified mobile design system with padded surfaces, selective text wrapping,
  48px-or-larger touch targets, and a code-drawn mint slime Mallow mascot
- Memory: `flash`, `count`, `nback`, `cards`, `rev`
- Focus and speed: `stroop`, `switch`, `trail`, `react`, `chop`, `run`, `flank`
- Coordination: `whack`, `catch`, `trace`
- Sight: `spot`, `odd`, `diff`
- Space: `rotate`, `slide`, `fit`
- Sound: `melody`, `rhythm`, `pitch`
- Calculation: `math`, `bubble`, `merge`, `guess`
- Logic: `iq`, `sudoku`, `sort`, `nono`
- Language: `anagram`, `wordsearch`
- Play-style test: `braintype`
- Daily puzzles: `moamoa`, `queens`, `tango`
- Assessment: memory, focus, calculation, and coordination calibration flow

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

The APK includes arm64 and x86_64, is portrait-oriented, and uses package
`com.playmallow.mallow`, version `0.1.0` (version code `1`). The x86_64 slice
allows the debug build to run in the project-local PC emulator. A release
APK/AAB still requires a project-owned non-debug keystore; do not reuse the
generated debug keystore for Google Play.

## Android PC emulator

The project-local Android SDK includes a `PlayMallow_API35` AVD (Pixel 6,
Android 15, x86_64). Build and launch the app from the repository root with:

```powershell
& .\mobile\godot\build-android.ps1
& .\mobile\godot\run-android-emulator.ps1
```

The runner boots the AVD when needed, waits for Android to finish starting,
installs `mobile/godot/build/playmallow-debug.apk`, and opens the app on
`emulator-5554`. It targets only this project-local emulator and does not
operate on a connected physical device.

The runner uses a non-incremental streamed install and launches the Godot
activity directly. This avoids the ADB incremental-install stalls observed on
the project-local emulator.

## Mobile UI system

- `ThemeKit.gd` owns palette, borders, card padding, shadows, and button states.
- `MallowAvatar.gd` draws the hole-free mint slime Mallow mascot at any requested control size.
- Labels wrap only where copy is expected to span lines; compact rows preserve
  their natural width instead of collapsing into vertical text.
- Home, Games, Records, Settings, Result, Assessment, and all 38 game modules share
  one spacing and interaction hierarchy.
- Ambient backdrop motion, slime idle breathing, target glows, and tap easing
  are used for feedback without overwhelming the task.
- Android emulator visual QA covers the assessment flow, result recommendations,
  the expanded Games list, and native touch/game launch at 1080x2400 on Android 15.

## Structure

```text
Main.tscn                 app entry scene
scripts/Main.gd           mobile shell and navigation
scripts/SaveStore.gd      versioned local records/settings
scripts/AudioDirector.gd  procedural feedback tones and haptics
scripts/I18n.gd           Korean/English strings
scripts/ThemeKit.gd       shared mobile visual styles
scripts/AssessmentFlow.gd first-launch baseline assessment
scripts/RecommendationEngine.gd explainable daily recommendation ranking
games/*.gd                independent playable game modules
tests/smoke.gd            headless module instantiation check
```

The next release-hardening slice should add Android back/resume handling, controlled
re-assessment cadence, analytics consent, and release keystore configuration.
