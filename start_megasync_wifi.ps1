$maxRetries = 10 # 10 minutes (30 * 10 seconds)
$retryDelay = 30 # 30 seconds

for ($i = 0; $i -lt $maxRetries; $i++) {
    # Check if the internet connection is valid
    $connectionProfile = Get-NetConnectionProfile
    if ($connectionProfile.IPv4Connectivity -eq "Internet") {
        Write-Host "Internet connection successful."
        Start-Process "C:\Users\Minh-Anh\AppData\Local\MEGAsync\MEGAsync.exe"
        break
    } else {
        # Internet connection is not valid, wait and try again
        Write-Host "No internet connection detected. Waiting $retryDelay seconds before trying again."
        Start-Sleep -Seconds $retryDelay
    }
}

if ($i -eq $maxRetries) {
    # Exceeded the maximum number of retries, exit the script or take other action
    Write-Host "Unable to establish a valid internet connection. MegaSync will not be launched."
}
