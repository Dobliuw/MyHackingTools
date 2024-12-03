param (
    [string]$macAddress # Get the MAC address
)

if ($macAddress){
    $length = $macAddress.Length
    
    if($macAddress -match ":"){
        $macAddress = $macAddress -replace ":", "-" # Parse format FF:FF:FF to FF-FF-FF
    }

    $macAddress = $macAddress.Substring(0, [math]::Floor($length/2)) # Get the first half
    
    # MODIFY THIS LINE WITH THE HARDCODED PATH TO THE OUI DB
    $ouiDatabase = Get-Content "C:\Hacking\wordlists\oui_db.txt" # Consult to local DB

    $result = $ouiDatabase | ForEach-Object -Begin {
        $capture = $false
        $contextLines = 4
        $contextCounter = 0
    } -Process {
        if ($_ -match $macAddress) {
            # Encontrar el match
            Write-Output "$_"
            $capture = $true
            $contextCounter = 0
        } elseif ($capture -and $contextCounter -lt $contextLines) {
            # Capturar las líneas posteriores
            Write-Output  "$_"
            $contextCounter++
            if ($contextCounter -ge $contextLines) {
                $capture = $false
            }
        }
    } 

    if($result){
        Write-Output $result
    }else{
        Write-Output "[!] MAC $macAddress not found."
    }
}else{
    Write-Error "[!] Please insert a valid MAC. (Example: $PSCommandPath FF:FF:FF:FF:FF:FF)"
}