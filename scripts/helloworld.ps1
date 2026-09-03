function Test1() {
    Write-Host "helloworld"
}

function Test2() {
    Write-Host "hello moon"
}

function openCalc() {
    Start-Process calc.exe
}

function openSettings() {
    Start-Process ms-settings:
}

function openExplorer() {
    Start-Process explorer.exe
}