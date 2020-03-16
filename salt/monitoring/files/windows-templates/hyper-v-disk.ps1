$returnCode=0
Get-VM | ForEach { $Vm = $_; $_.HardDrives } | ForEach {
    $GetVhd = Get-VHD -Path $_.Path
    $ProvisionedGB = ($GetVhd.Size / 1GB)
    $CommittedGB = ($GetVhd.FileSize / 1GB)
    $UsedPercentage = ((100/($GetVhd.Size / 1GB))*($GetVhd.FileSize / 1GB))
if(  $UsedPercentage -gt 99 -and $usedPercentage -lt 101)
	{
		echo "CRITICAL: DISK IS FULL!!!"
		$returnCode=2
[pscustomobject]@{

        Vm = $Vm.Name
        Name = $_.Name
        ProvisionedGB = $ProvisionedGB
        CommittedGB = $CommittedGB
        UsedPercentage = $UsedPercentage

    }

        }
elseif(  $UsedPercentage -gt 95 -and $usedPercentage -lt 101 )
	{
		echo "WARNING: DISK IS ALMOST FULL!!!"
		if ($returnCode -ne 2){
			$returnCode=1
		}
[pscustomobject]@{

        Vm = $Vm.Name
        Name = $_.Name
        ProvisionedGB = $ProvisionedGB
        CommittedGB = $CommittedGB
        UsedPercentage = $UsedPercentage

    }

        }

#    [pscustomobject]@{
#
#        Vm = $Vm.Name
#        Name = $_.Name
#        ProvisionedGB = $ProvisionedGB
#        CommittedGB = $CommittedGB
#        UsedPercentage = $UsedPercentage
#
#    }

}
exit $returnCode
