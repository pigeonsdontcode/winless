function ClearTemp() {
    $ItemList = @(
        "$Env:SystemRoot\Temp\*",
        "$Env:Temp\*"
    )

    foreach($item in $ItemList) {
        Remove-Item -Path $item -Recurse -Force
    }
}

function ClearPrefetch() {
    Remove-Item -Path "$Env:windir\Prefetch\*" -Recurse -Force
}

function ClearBin() {
    Clear-RecycleBin -Force
}