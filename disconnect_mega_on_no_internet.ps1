$maxRetries = 10 # Number of retries before stopping the script
$retryDelay = 10 # Delay between retries in seconds

for ($i = 0; $i -lt $maxRetries; $i++) {
    # Check if the internet connection is valid
    $connectionProfile = Get-NetConnectionProfile
    if ($connectionProfile.IPv4Connectivity -ne "Internet") {
        Write-Host "No internet connection detected. Stopping MEGAsync."
        # Stop the MEGAsync process
        Stop-Process -Name "MEGAsync" -ErrorAction SilentlyContinue
        break
    }
    else {
        # Internet connection is valid, wait and try again
        Write-Host "Internet connection is active. Checking again in $retryDelay seconds."
        Start-Sleep -Seconds $retryDelay
    }
}

if ($i -eq $maxRetries) {
    Write-Host "Internet connection remained active. MEGAsync will continue running."
}