# Check if network is on and retry every 5 seconds
$minutes = 5
$retryDelay = 5 # 5 seconds
$maxRetries = $minutes * 60 / $retryDelay # 5 minutes (5 min = 5*60s ; 300/5 = 60 retries)
$maxDuration = 300 # Define maxDuration to avoid undefined variable error
for ($i = 0; $i -lt $maxRetries; $i++) {
    try {
        # Attempt to connect to the portal
        $connectionProfile = Get-NetConnectionProfile
        if ($connectionProfile.Name -ne "BNF") {
            Write-Host "The network is not BNF. Waiting $retryDelay seconds before trying again."
            Start-Sleep -Seconds $retryDelay
            continue
        }

        $url = "http://detectportal.firefox.com/canonical.html"
        $body = @{action = "Accepter" }
        $maxDuration = 60 # Maximum duration in seconds (1 minute)
        $startTime = Get-Date

        while ((Get-Date).AddSeconds(-$maxDuration) -lt $startTime) {
            try {
                Invoke-WebRequest -Uri $url -Method Post -Body $body | Out-Null
                Write-Host "Attempted connection to BNF portal."
        
                # Check if the internet connection is successful
                Write-Host "Waiting $($retryDelay * 2) seconds before checking"
                Start-Sleep -Seconds ($retryDelay * 2)
                Write-Host "Checking if connection to Google is possible."
                $webRequest = Invoke-WebRequest -Uri "http://www.google.com" -Method Head
                if ($webRequest.StatusCode -eq 200) {
                    Write-Host "Internet connection is successful."
                    break
                }
                else {
                    Write-Output "Request failed. Retrying..."
                    Start-Sleep -Seconds $retryDelay
                }
            } 
            catch {
                Write-Host "Attempt $i : No internet connection detected or portal connection failed. Waiting $retryDelay seconds before trying again."
                Start-Sleep -Seconds $retryDelay
            }
        }
    }
    catch {
        Write-Host "Attempt $i : Error occurred. Waiting $retryDelay seconds before trying again."
        Start-Sleep -Seconds $retryDelay
    }
}

if ($i -eq $maxRetries) {
    # Exceeded the maximum number of retries, exit the script or take other action
    Write-Host "Unable to establish a valid internet connection. Can't access internet through BNF Captive Portal."
}

# Create a scheduled task to run the script every day at user log on
# Exemple: New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal
# Run as administrator in powershell

# $action = New-ScheduledTaskAction -Execute "powershell" -Argument "-File ""D:\Library\Code\Useful scripts\bnf_captive_portal.ps1"""
# $trigger = New-ScheduledTaskTrigger -AtLogOn
# $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries
# $principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount
# Register-ScheduledTask -TaskName "BNF Captive Portal" -Action $action -Trigger $trigger -Settings $settings -Principal $principal

