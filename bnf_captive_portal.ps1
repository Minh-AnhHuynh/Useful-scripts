# Step 1: Check if BNF Wi-Fi network is available and retry if necessary
$wifiName = "BNF"
$maxWifiRetries = 10
$wifiRetryDelay = 10  # Retry every 10 seconds for Wi-Fi connection
$wifiConnected = $false

for ($j = 0; $j -lt $maxWifiRetries; $j++) {
    $availableNetworks = netsh wlan show networks

    if ($availableNetworks -match $wifiName) {
        Write-Host "$wifiName network found. Attempting to connect..."
        netsh wlan connect name=$wifiName
        Write-Host "Waiting 5 seconds before continuing."
        Start-Sleep -Seconds 5  # Wait for 5 seconds to connect to Wi-Fi

        # Check if connected to BNF
        $connectionProfile = Get-NetConnectionProfile
        if ($connectionProfile.Name -eq $wifiName) {
            Write-Host "Connected to $wifiName network."
            $wifiConnected = $true
            break
        }
    }
    else {
        Write-Host "$wifiName network not available yet. Retrying in $wifiRetryDelay seconds..."
    }

    Start-Sleep -Seconds $wifiRetryDelay
}

# Exit script if unable to connect to Wi-Fi after retries
if (-not $wifiConnected) {
    Write-Host "Unable to connect to $wifiName Wi-Fi after $maxWifiRetries retries. Exiting script."
    exit
}

$maxRetries = 12
$retryDelay = 10

for ($i = 0; $i -lt $maxRetries; $i++) {
    try {
        # Attempt to connect to the portal
        $connectionProfile = Get-NetConnectionProfile
        if ($connectionProfile.Name -ne $wifiName) {
            Write-Host "The network is not BNF. Waiting $retryDelay seconds before trying again."
            Start-Sleep -Seconds $retryDelay
            continue
        }

        $url = "http://detectportal.firefox.com/canonical.html"
        $body = @{action = "Accepter" }

        Invoke-WebRequest -Uri $url -Method Post -Body $body | Out-Null
        Write-Host "Attempted connection to BNF portal."
        
        # Step 3: Check if the internet connection is successful
        Write-Host "Waiting $retryDelay seconds before checking."
        Start-Sleep -Seconds $retryDelay
                


        if ($connectionProfile.IPv4Connectivity -eq "LocalNetwork") {
            Write-Host "Connected to BNF but haven't passed BNF portal."
        }

        if ($connectionProfile.IPv4Connectivity -eq "Internet") {
            Write-Host "Internet connection is successful. Exiting script."
            exit  # Exit the script upon successful internet connection
        }
        else {
            Write-Output "Request failed. Retrying..."
            Start-Sleep -Seconds $retryDelay
        } 
    }
    catch {
        Write-Host "Attempt $i : Error occurred. Waiting $retryDelay seconds before trying again."
        Start-Sleep -Seconds $retryDelay
    }
}

# If all retries failed
Write-Host "Unable to establish a valid internet connection. Can't access internet through BNF Captive Portal."

# Create a scheduled task to run the script every day at user log on
# Exemple: New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal
# Run as administrator in powershell

# $action = New-ScheduledTaskAction -Execute "powershell" -Argument "-File ""D:\Library\Code\Useful scripts\bnf_captive_portal.ps1"""
# $trigger = New-ScheduledTaskTrigger -AtLogOn
# $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries
# $principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount
# Register-ScheduledTask -TaskName "BNF Captive Portal" -Action $action -Trigger $trigger -Settings $settings -Principal $principal

