# Local development tools

Godot is installed locally for this project at:

```text
tools/godot/Godot_v4.7.1-stable_win64.exe
```

Verified version:

```text
4.7.1.stable.official.a13da4feb
```

The executable and downloaded archive are intentionally ignored by Git because they are large local tool artifacts. The official source was the [Godot 4.7.1 stable archive](https://godotengine.org/download/archive/4.7.1-stable/).

Android build tools are also installed locally for the native vertical slice:

```text
tools/jdk17/jdk-17.0.20+8
tools/android/cmdline-tools/latest
tools/android/sdk
```

The SDK uses Platform-Tools, Build-Tools 35.0.1, Android Platform 35,
CMake 3.10.2.4988404, and NDK 28.1.13356709. Rebuild the debug APK with
`mobile/godot/build-android.ps1`. The export template is kept under
`tools/godot/export_templates/4.7.1.stable` and copied into the local Godot
user data directory by the build script.
