
# HTML:
# <input class="button" type="submit" id="boutonAction" name="action" value="Accepter" onclick="document.getElementById('attente').style.display='block';">

# Check if network is on and retry every 5 seconds
$maxRetries = 120 # 10 minutes (10 min = 600 s ; 600/5 = 120 retries)
$retryDelay = 5 # 5 seconds
for ($i = 0; $i -lt $maxRetries; $i++) {
    $connectionProfile = Get-NetConnectionProfile
    if ($connectionProfile.Name -eq "BNF") {
        $url = "http://detectportal.firefox.com/canonical.html"
        $body = @{action = "Accepter" }

        Invoke-WebRequest -Uri $url -Method Post -Body $body
        Write-Host "Successful connection to BNF portal."
        # Wait for 2 seconds before closing
        Start-Sleep -Seconds 2
        break
    }
    else {
        # Internet connection is not valid, wait and try again
        Write-Host "No internet connection detected. Waiting $retryDelay seconds before trying again."
        Start-Sleep -Seconds $retryDelay
    }
    if ($i -eq $maxRetries) {
        # Exceeded the maximum number of retries, exit the script or take other action
        Write-Host "Unable to establish a valid internet connection. Can't access internet through BNF Captive Portal."
    }
}

# Create a scheduled task to run the script every day at user log on
# Exemple: New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal

# $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File ""D:\Library\Code\Useful scripts\bnf_captive_portal.ps1"""
# $trigger = New-ScheduledTaskTrigger -AtLogOn
# $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries
# $principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount

# Register-ScheduledTask -TaskName "BNF Captive Portal" -Action $action -Trigger $trigger -Settings $settings -Principal $principal
