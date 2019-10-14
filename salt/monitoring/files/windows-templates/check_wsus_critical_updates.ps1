# This is a little basic script I have written to query a WSUS server 
# about the updates needed by the system.
#
# It will only return a Critical status if there are any Critical Security Updates, 
# or Critical Updates waiting to be applied.
#
# I by no mean pretend to be a profesionnal scripter, so feel free
# to modify as you see fit!
#
# Written by: Alexandre Beauclair
# Date: April 12th 2012

#Declaring base variables. You can change the $wsusserver value if needed.
$wsusserver = "localhost"
$securityCritical = 0
$criticalUpdates = 0

#Load required assemblies

[void][reflection.assembly]::LoadWithPartialName("Microsoft.UpdateServices.Administration")

#Create necessary objects

$wsus = [Microsoft.UpdateServices.Administration.AdminProxy]::getUpdateServer($wsusserver,$False)
$updatescope = New-Object Microsoft.UpdateServices.Administration.UpdateScope

#Specify we are looking for updates which are Not Approved, and Not Installed.

$updatescope.ApprovedStates = [Microsoft.UpdateServices.Administration.ApprovedStates]::NotApproved
$updatescope.IncludedInstallationStates = [Microsoft.UpdateServices.Administration.UpdateInstallationStates]::NotInstalled

#Find how many updates are available.

$checkSecurityCritical = $wsus.GetUpdates($updatescope) | where {$_.UpdateClassificationTitle -eq "Security Updates"} | ft MsrcSeverity -AutoSize | FIND /c " Critical"
$checkCriticalUpdates = $wsus.GetUpdates($updatescope) | where {$_.UpdateClassificationTitle -eq "Critical Updates"} | ft UpdateClassificationTitle | FIND /c "Critical Updates"

$securityCritical += $checkSecurityCritical
$criticalUpdates += $checkCriticalUpdates


#Return message and exit code accordingly.

if(($securityCritical -gt 0) -or ($criticalUpdates -gt 0)){
	Write-Host "CRITICAL - There are updates waiting to be applied. Critical Updates: $criticalUpdates   Critical Security Updates: $securityCritical"
	exit 2
}else{
	Write-Host "OK - There are no critical updates waiting to be applied."
	exit 0
}



