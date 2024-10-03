# Set the network profile to BNF
$connectionProfile = New-Object -TypeName System.Net.NetworkInformation.ConnectionProfile
$connectionProfile.Name = "BNF"
Set-Variable -Name "Get-NetConnectionProfile" -Value { return $connectionProfile } -Force

# Mock the Invoke-WebRequest cmdlet to simulate a successful internet connection
$webRequest = New-Object -TypeName System.Net.HttpWebResponse
$webRequest.StatusCode = 200
Set-Variable -Name "Invoke-WebRequest" -Value { return $webRequest } -Force

# Run the script
& "D:\Library\Code\Useful scripts\bnf_captive_portal.ps1"

# Assuming your script sets a variable `$isConnected` to $true upon successful connection


if ($response.StatusCode -eq 200) {
    Write-Host "Test Passed: Internet connection successful."
}
else {
    Write-Host "Test Failed: Internet connection not successful."
}