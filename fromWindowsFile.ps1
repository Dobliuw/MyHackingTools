# Get script name 
$scriptName = $MyInvocation.MyCommand.Name

# Validate Arguments
if($args.Count -lt 3){
    Write-Host "`n`t Usage: $scriptName <host IP> <host PORT> <FILE TO TRANSFER>`n`n"
    exit 1 
}

# Validate Port function
function validatePort($port){
    $portToValidate = [int]$port
    return ($portToValidate -ge 0 -and $portToValidate -le 65535)
}

# Validate Host function
function validateHost($ip){
    return ($ip -match '\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
}

# Read host IP and PORT
$targetIP = $args[0]
$targetPort = $args[1]
# Read file to transfer
$pathFile = $args[2]

if(-not (validatePort $targetPort)) {
    Write-Host "`n`t[!] INVALID HOST PORT: $targetPort. Please insert a correct one (0-65.535).`n`n"
    exit 1
}
if (-not (validateHost $targetIP)){
    Write-Host "`n`t[!] INVALID HOST IP: $targetIP. Pleaser insert a correct format (0.0.0.0 - 255.255.255.255).`n`n" 
    exit 1 
}
if (-not (Test-Path $pathFile)){
    Write-Host "`n`t[!] FILE PATH $pathFile TO TRANSFER NOT FOUND.`n`n"
    exit 1 
}

# Read file content
Write-Host "`n`t[i] Trying read $pathFile content...`n"
$fileContent = Get-Content -Path $pathFile -Raw

# Try to create a TCP client and connect to host target
Write-Host "`t[i] Trying to connect to host $targetIP\:$targetPort...`n"
$client = New-Object System.Net.Sockets.TcpClient
$client.Connect($targetIP, $targetPort)
Write-Host "`t`t[+] Successfully connected.`n"

# Get the network stream
$stream = $client.GetStream()

# Convert file content to bytes and send it over the network stream
Write-Host "`t[i] Converting file $pathFile to bytes...`n"
$bytesToSend = [System.Text.Encoding]::ASCII.GetBytes($fileContent)
$stream.Write($bytesToSend, 0, $bytesToSend.Length)
Write-Host "`t[+] File successfully sended.`n`n"

# Close the network stream and TCP client
$stream.Close()
$client.Close()