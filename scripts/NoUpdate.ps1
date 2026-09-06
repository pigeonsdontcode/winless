$UpdateSvcList = @(
    'wuauserv', # overall service for updates, also enables Windows Update Agent api
    'UsoSvc', # Update Orchestrator Service, responsible for scheduling and enforcing updates
    'BITS', # Background Intelligent Transfer Service, windows updates rely on this
    'WaaSMedicSvc', # Responsible for repairing the ability to update if it breaks (another way for Microsoft to push updates down your throat)
)

function DisableUpdateServices() {
    foreach($svc in $UpdateSvcList) {
        Set-Service -Verbose -Name $svc -StartupType Disabled
        Stop-Service -Verbose -Name $svc -Force
    }
}

function RemovePowerOptions() {
    $PowerMenuRegPath = "HKLM:\SOFTWARE\Microsoft\WindowsUpdate\Orchestrator"
    $PowerMenuRegKey = "ShutdownFlyoutOptions"

    Set-ItemProperty -Path $PowerMenuRegPath -Name $PowerMenuRegKey -Value 5 -Type DWORD
    # expected value is a 4-bit binary table / 0000
    # 0 first digit = update & shutdown (this is always a lie, it reboots after update)
    # 0 second digit = shutdown
    # 0 third digit = update & reboot
    # 0 fourth digit = restart

    # the ideal value would be 0101 (show shutdown + restart)
    # which equals to 5 in decimal format

    # windows will gradually force the power options with updates
    # please note that windows will check and perform updates in different ways,
    # disabling the power menu options alone is not enough to not update
}

function PauseUpdates() {

}

function DeleteCachedUpdates() {

}