powershell $creds = Get-Credential -Credential Administrator
powershell Copy-Item (Get-Location)-Destination "C:\www\ivan" -ToSession (New-PSSession -ComputerName ec2-18-196-2-127.eu-central-1.compute.amazonaws.com -Credential $creds -UseSSL -SessionOption (New-PsSessionOption -SkipCACheck -SkipCNCheck)) -Recurse
pause