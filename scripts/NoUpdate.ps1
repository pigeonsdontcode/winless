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