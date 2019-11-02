$server = "ec2-18-196-2-127.eu-central-1.compute.amazonaws.com"
$accountName = "Administrator"
$origin = Get-Location
$originZip = "$origin\deploy.zip"
$destination = "C:\www\ivan"
$destinationZip = "$destination\deploy.zip"

Remove-Item -Path $originZip
Compress-Archive -Path $origin -DestinationPath $originZip

$so = New-PsSessionOption -SkipCACheck -SkipCNCheck
$creds = Get-Credential -Credential $accountName
$session = New-PSSession -ComputerName $server -Credential $creds -UseSSL -SessionOption $so

Invoke-Command -Session $session -Command { Remove-Item $Using:destination -Force -Recurse }
Copy-Item $originZip $destinationZip -ToSession $session -Recurse