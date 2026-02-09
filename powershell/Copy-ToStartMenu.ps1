# Copy-ToStartMenu.ps1
# Copies a shortcut from the clipboard path to the Windows Start Menu

# Get the path from clipboard
$clipboardPath = Get-Clipboard

# Validate that clipboard contains a path
if ([string]::IsNullOrWhiteSpace($clipboardPath)) {
    Write-Host "Error: Clipboard is empty!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Clean up the path (remove quotes if present)
$clipboardPath = $clipboardPath.Trim().Trim('"')

# Check if the file exists
if (-not (Test-Path $clipboardPath)) {
    Write-Host "Error: File not found at path: $clipboardPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if it's a .lnk file
if ([System.IO.Path]::GetExtension($clipboardPath) -ne ".lnk") {
    Write-Host "Warning: File is not a .lnk shortcut file. Continuing anyway..." -ForegroundColor Yellow
}

# Define Start Menu paths
$userStartMenu = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
$allUsersStartMenu = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs"

# Ask user which location to use
Write-Host "`nClipboard path: $clipboardPath" -ForegroundColor Cyan
Write-Host "`nWhere do you want to copy the shortcut?" -ForegroundColor Yellow
Write-Host "1. Current user only ($userStartMenu)"
Write-Host "2. All users (requires admin) ($allUsersStartMenu)"
Write-Host ""

$choice = Read-Host "Enter your choice (1 or 2)"

switch ($choice) {
    "1" {
        $destination = $userStartMenu
        $requiresAdmin = $false
    }
    "2" {
        $destination = $allUsersStartMenu
        $requiresAdmin = $true
    }
    default {
        Write-Host "Invalid choice. Defaulting to current user only." -ForegroundColor Yellow
        $destination = $userStartMenu
        $requiresAdmin = $false
    }
}

# Check if running as admin when needed
if ($requiresAdmin) {
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    
    if (-not $isAdmin) {
        Write-Host "`nError: Administrator privileges required for All Users location!" -ForegroundColor Red
        Write-Host "Please run this script as Administrator." -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Get the filename
$fileName = Split-Path $clipboardPath -Leaf
$destinationPath = Join-Path $destination $fileName

# Copy the file
try {
    Copy-Item -Path $clipboardPath -Destination $destinationPath -Force
    Write-Host "`nSuccess! Shortcut copied to:" -ForegroundColor Green
    Write-Host $destinationPath -ForegroundColor Cyan
    Write-Host "`nThe shortcut should now appear in your Start Menu." -ForegroundColor Green
}
catch {
    Write-Host "`nError copying file: $_" -ForegroundColor Red
}

Read-Host "`nPress Enter to exit"
