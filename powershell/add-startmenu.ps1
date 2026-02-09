param(
    [Parameter(Mandatory)]
    [string]$ExePath,

    [string]$Name,
    [string]$Arguments = "",
    [switch]$AllUsers
)

if (-not (Test-Path $ExePath)) {
    Write-Error "Executable not found: $ExePath"
    exit 1
}

if (-not $Name) {
    $Name = [IO.Path]::GetFileNameWithoutExtension($ExePath)
}

$ProgramsPath = if ($AllUsers) {
    "$env:ProgramData\Microsoft\Windows\Start Menu\Programs"
} else {
    Join-Path ([Environment]::GetFolderPath("StartMenu")) "Programs"
}

$ShortcutPath = Join-Path $ProgramsPath "$Name.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

$Shortcut.TargetPath = $ExePath
$Shortcut.Arguments = $Arguments
$Shortcut.WorkingDirectory = Split-Path $ExePath
$Shortcut.IconLocation = $ExePath
$Shortcut.Save()

Write-Output "Start Menu shortcut created: $ShortcutPath"

Start-Sleep -Seconds 5

# Parameters to put in Listary to make it work
# Path: powershell.exe
# Parameters: -NoProfile -ExecutionPolicy Bypass -File "D:\Libraries\Code\Personal\Useful-scripts\powershell\add-startmenu.ps1" -ExePath "{action_path}"