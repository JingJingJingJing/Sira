
$curPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$siraPath = $curPath + "\sira"
$siraQueryPath = $curPath + "\sira-query"
#$siraZipPath = $curPath + "\sira.zip"
#Unzip-File -ZipFile $siraZipPath -TargetFolder $curPath
$envPath = [environment]::GetEnvironmentvariable("Path","user")
if(!$envPath.contains($siraPath)){
    $envPath = $envPath + ";" + $siraPath
}
if(!$envPath.contains($siraQueryPath)){
    $envPath = $envPath + ";" + $siraQueryPath
}
[environment]::SetEnvironmentvariable("Path",$envPath,"user")
Pause