# Change the current working directory to the script directory
Set-Location -Path $PSScriptRoot

# Run the node command and capture its output
$output = node epic-games

# Display the output in the terminal
$output | Write-Output

# Get the last line of the output
$lastLine = $output[-1]

# Check the content of the last line and display a success message
if ($lastLine -eq "  Claimed successfully!" -or $lastLine -eq "  Already in library! Nothing to claim.") {
    Write-Output "Success: $lastLine"
} else {
    Write-Output "Failure: $lastLine"
}   

# Pause for 30 seconds
Start-Sleep -Seconds 30