$server = "ec2-18-196-2-127.eu-central-1.compute.amazonaws.com"
$accountName = "Administrator"
$origin = Get-Location
$destination = "C:\www\ivan"
$so = New-PsSessionOption -SkipCACheck -SkipCNCheck
$creds = Get-Credential -Credential $accountName
$session = New-PSSession -ComputerName $server -Credential $creds -UseSSL -SessionOption $so
Copy-Item $origin $destination -ToSession $session -Recurse