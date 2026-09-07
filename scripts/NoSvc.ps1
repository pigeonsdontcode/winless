function DisableService($name) {
    Set-Service -Name $name -StartupType Disabled
    Stop-Service -Name $name -Force

    Write-Host "Service: $name has been disabled"
}

function DisableParentalControls() {
    DisableService("WpcMonSvc")
}

# please stop Microsoft from using your device as a public update cdn
# it hords quite alot of your network traffic
function DisableDeliveryOptimization() {
    DisableService("DoSvc")
}

function DisableRemoteManagement() {
    DisableService("WinRM")
}

function DisableUserExperiences() {
    DisableService("DiagTrack")
}