param(
    [ValidateSet("debug", "release")]
    [string]$Mode = "debug",
    [string]$OutputPath = ""
)

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$godotProject = Join-Path $projectRoot "mobile\godot"
$godot = Join-Path $projectRoot "tools\godot\Godot_v4.7.1-stable_win64.exe"
$javaHome = Join-Path $projectRoot "tools\jdk17\jdk-17.0.20+8"
$sdkRoot = Join-Path $projectRoot "tools\android\sdk"
$godotUser = Join-Path $projectRoot ".godot-user"
$godotCache = Join-Path $projectRoot ".godot-cache"
$templateSource = Join-Path $projectRoot "tools\godot\export_templates\4.7.1.stable"
$templateDestination = Join-Path $godotUser "Godot\export_templates\4.7.1.stable"

foreach ($requiredPath in @($godot, (Join-Path $javaHome "bin\java.exe"), (Join-Path $sdkRoot "platform-tools\adb.exe"), (Join-Path $templateSource "android_debug.apk"))) {
    if (-not (Test-Path $requiredPath)) {
        throw "Android build prerequisite is missing: $requiredPath"
    }
}

New-Item -ItemType Directory -Force -Path $godotUser, $godotCache, $templateDestination | Out-Null
Copy-Item -Path (Join-Path $templateSource "*") -Destination $templateDestination -Recurse -Force

$env:APPDATA = $godotUser
$env:LOCALAPPDATA = $godotCache
$env:JAVA_HOME = $javaHome
$env:ANDROID_HOME = $sdkRoot
$env:ANDROID_SDK_ROOT = $sdkRoot
$env:PATH = ((Join-Path $javaHome "bin") + ";" + (Join-Path $sdkRoot "platform-tools") + ";" + $env:PATH)

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $godotProject ("build\playmallow-{0}.apk" -f $Mode)
} elseif (-not [System.IO.Path]::IsPathRooted($OutputPath)) {
    $OutputPath = Join-Path $projectRoot $OutputPath
}

New-Item -ItemType Directory -Force -Path (Split-Path $OutputPath) | Out-Null
$exportFlag = if ($Mode -eq "release") { "--export-release" } else { "--export-debug" }
& $godot --headless --path $godotProject $exportFlag "Android" $OutputPath
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Get-Item -LiteralPath $OutputPath | Select-Object FullName, Length, LastWriteTime
