$process = Get-Process GoogleDriveFS -ErrorAction SilentlyContinue

if ($process) {
    Write-Output "Google Drive is already running."
} else {
    Write-Output "Google Drive is not running. Starting it now."
    Start-Process "googledrive"

    while (!(Get-Process GoogleDriveFS -ErrorAction SilentlyContinue)) {
        Start-Sleep -Seconds 2
    }
    Write-Output "Google Drive has started successfully."
}

# Get the user's Downloads folder
$downloadsPath = (New-Object -ComObject Shell.Application).Namespace('shell:Downloads').Self.Path
$folders = Get-ChildItem $downloadsPath | Where-Object { $_.Name -like "STG*" }

if ($null -eq $folders) { 
    # Folder does not exist
    Write-Output "Folder does not exist"
    exit
}


# Get the last folder in the array
$folder = $folders[-1]
# Get the files in the folder
$files = Get-ChildItem -Path $folder.FullName


if ($null -eq $files) { 
    # Files does not exist
    Write-Output "Files does not exist"
    exit
}
# Get the last file to backup
$backup_files = $files | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# Get the computer name
# $computerName = $env:COMPUTERNAME
# Limited to 15 characters, switching to hostname
$computerName = $(hostname)
# Convert the computer name to CamelCase

$camelCaseComputerName = -join ($computerName -split '[_ ]' | ForEach-Object { 
    if ($_ -eq '-') { 
        $_ 
    } else { 
        $_.Substring(0,1).ToUpper() + $_.Substring(1).ToLower() 
    } 
})

# Define the destination path
$destination_backup = "G:\My Drive\Backup\Simple Tab Groups"

# Create a unique folder name based on the computer name
$uniqueFolderName = Join-Path -Path $destination_backup -ChildPath $camelCaseComputerName

# Ensure the unique folder exists
if (-not (Test-Path -Path $uniqueFolderName)) {
    New-Item -Path $uniqueFolderName -ItemType Directory | Out-Null
}

# Update the destination to include the unique folder
$destination = $uniqueFolderName

# Copy the file to the destination with error handling
# Copy the file to the destination with error handling
try {
    Copy-Item -Path $backup_files.FullName -Destination $destination -ErrorAction Stop
    Write-Output "File backed up: $($backup_files.Name) to $destination"
    
    # Verify if the file exists in the destination folder
    $destinationFilePath = Join-Path -Path $destination -ChildPath $backup_files.Name
    if (Test-Path -Path $destinationFilePath) {
        Write-Output "File successfully verified in destination: $destinationFilePath"
    } else {
        Write-Output "File copy verification failed: $($backup_files.Name) not found in destination: $destination"
    }
} catch {
    Write-Output "Error copying file: $_"
}

# Do post backup cleanup of local files
Write-Output "Starting post-backup cleanup of local files..."

# Remove all folders except the most recent one
$folders | Where-Object { $_.FullName -ne $folder.FullName } | ForEach-Object {
    Remove-Item -Path $_.FullName -Recurse -Force
    Write-Output "Removed folder: $($_.FullName)"
}

Write-Output "STG Backup completed successfully!"
Start-Sleep -Seconds 5