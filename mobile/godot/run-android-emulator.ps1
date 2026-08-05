param(
    [string]$AvdName = "PlayMallow_API35",
    [string]$PackageName = "com.playmallow.mallow",
    [string]$ApkPath = ""
)

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$sdkRoot = Join-Path $projectRoot "tools\android\sdk"
$emulator = Join-Path $sdkRoot "emulator\emulator.exe"
$adb = Join-Path $sdkRoot "platform-tools\adb.exe"
$avdHome = Join-Path $projectRoot "tools\android\avd"
$androidUser = Join-Path $projectRoot "tools\android\user"
$systemImage = Join-Path $sdkRoot "system-images\android-35\default\x86_64"

if ([string]::IsNullOrWhiteSpace($ApkPath)) {
    $ApkPath = Join-Path $projectRoot "mobile\godot\build\playmallow-debug.apk"
} elseif (-not [System.IO.Path]::IsPathRooted($ApkPath)) {
    $ApkPath = Join-Path $projectRoot $ApkPath
}

foreach ($requiredPath in @($emulator, $adb, $systemImage, $ApkPath)) {
    if (-not (Test-Path $requiredPath)) {
        throw "Android emulator prerequisite is missing: $requiredPath"
    }
}

$env:ANDROID_HOME = $sdkRoot
$env:ANDROID_SDK_ROOT = $sdkRoot
$env:ANDROID_AVD_HOME = $avdHome
$env:ANDROID_USER_HOME = $androidUser
New-Item -ItemType Directory -Force -Path $avdHome, $androidUser | Out-Null

$emulatorProcess = Get-Process emulator -ErrorAction SilentlyContinue
if ($null -eq $emulatorProcess) {
    $arguments = "@$AvdName -no-snapshot -no-boot-anim -gpu swiftshader_indirect -no-audio -no-metrics -sysdir `"$systemImage`""
    $startCommand = "start `"`" /b `"$emulator`" $arguments"
    cmd.exe /d /c $startCommand | Out-Null
}

$ready = $false
for ($attempt = 1; $attempt -le 60; $attempt++) {
    $devices = & $adb devices 2>$null
    if ($devices -match "emulator-5554\s+device") {
        $bootCompleted = (& $adb -s emulator-5554 shell getprop sys.boot_completed 2>$null).Trim()
        if ($bootCompleted -eq "1") {
            $ready = $true
            break
        }
    }
    Start-Sleep -Seconds 3
}

if (-not $ready) {
    throw "Android emulator did not finish booting within 180 seconds."
}

& $adb -s emulator-5554 install --no-incremental -r -d $ApkPath
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

& $adb -s emulator-5554 shell am force-stop $PackageName | Out-Null
& $adb -s emulator-5554 shell am start -n "$PackageName/com.godot.game.GodotAppLauncher" | Out-Null
Write-Output "Running $PackageName on $AvdName (emulator-5554)."
