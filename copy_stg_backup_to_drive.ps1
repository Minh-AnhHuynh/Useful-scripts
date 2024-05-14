$process = Get-Process GoogleDriveFS -ErrorAction SilentlyContinue

if ($process) {
    Write-Output "Google Drive is already running."
} else {
    Write-Output "Google Drive is not running. Starting it now."
    Start-Process "C:\Program Files\Google\Drive File Stream\68.0.2.0\GoogleDriveFS.exe"

    while (!(Get-Process GoogleDriveFS -ErrorAction SilentlyContinue)) {
        Start-Sleep -Seconds 1
    }
    Write-Output "Google Drive has started successfully."
}


$downloadsPath = "D:\Library\Downloads"
$folders = Get-ChildItem $downloadsPath | Where-Object { $_.Name -like "STG*" }

if ($null -eq $folders) { 
    # Folder does not exist
    Write-Output "Folder does not exist"
    exit
}


# Get the last folder in the array
$folder = $folders[-1]
# Get the last file to backup
$files = Get-ChildItem -Path $folder.FullName


if ($null -eq $files) { 
    # Folder does not exist
    Write-Output "Files does not exist"
    exit
}
# Get the last file to backu^p
$backup_files = $files[-1]



try {
    $destination = "G:\My Drive\Backup\Simple Tab Groups"
    Move-Item -Path $files.FullName -Destination $destination
} catch [System.IO.IOException] {
    Write-Output "Error: The file already exists at the destination."
    break
} catch {
    Write-Output "Error: The destination path was not found."
    break
}



Write-Output "File backed up: $($backup_files.Name)"

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show("STG Backup completed successfully!", "Backup Status", [System.Windows.Forms.MessageBoxButtons]::OK)