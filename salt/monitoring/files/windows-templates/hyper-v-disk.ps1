$returnCode=0
Get-VM | ForEach { $Vm = $_; $_.HardDrives } | ForEach {

    $GetVhd = Get-VHD -Path $_.Path
if(  ((100/($GetVhd.Size / 1GB))*($GetVhd.FileSize / 1GB)) -gt 95)
	{
		echo "WARNING: DISK IS ALMOST FULL!!!"
		$returnCode=1
        }
elseif(  ((100/($GetVhd.Size / 1GB))*($GetVhd.FileSize / 1GB)) -gt 99)
	{
		echo "CRITICAL: DISK IS FULL!!!"
		$returnCode=2
        }

    [pscustomobject]@{

        Vm = $Vm.Name

        Name = $_.Name

        Type = $GetVhd.VhdType

        ProvisionedGB = ($GetVhd.Size / 1GB)

        CommittedGB = ($GetVhd.FileSize / 1GB)
        UsedPercentage = ((100/($GetVhd.Size / 1GB))*($GetVhd.FileSize / 1GB))

    }

}
exit $returnCode
