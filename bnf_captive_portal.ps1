
# HTML:
# <input class="button" type="submit" id="boutonAction" name="action" value="Accepter" onclick="document.getElementById('attente').style.display='block';">

# Check if network is on and retry every 5 seconds
$maxRetries = 60 # 5 minutes (5 min = 300 s ; 300/5 = 60 retries)
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
}



