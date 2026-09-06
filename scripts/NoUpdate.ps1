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

    # Windows will gradually force the power options with updates
    # please note that Windows will check and perform updates in different ways,
    # disabling the power menu options alone is not enough to not update
}

function PauseUpdates() {
    # Windows update settings only allows a limited datetime set as paused expiration date
    # this is easily bypassed by changing the according registry value to any date we want

    # a date set to year 3001 or higher will return an error on the settings's update page
    # please note that while updates may seem to not be working,
    # Windows will just not read the invalid expiry time and continue to download and enforce updates regardless
    # hence why we set it to a safer datetime in the near future, when Windows will have stopped being of any relevance
    $PauseUpdatesPath = "HKLM:\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings"
    $PauseUpdatesKey = "PauseUpdatesExpiryTime"

    $dt = [datetime]::new(
        2100, # years
        12, # months
        31, # days
        0, 0, 0, # hms
    ).toString("yyyy-MM-ddTHH:mm:ssZ") # converted to registry string datetime format

    Set-ItemProperty -Path $PauseUpdatesPath -Name $PauseUpdatesKey -Value $dt -Type String
}

function DeleteCachedUpdates() {
    Remove-Item -Path "$Env:SystemRoot\SoftwareDistribution\*" -Recurse -Force
}