asnp Citrix*
Get-BrokerDesktopGroup -Property Name
Get-BrokerMachine -Property MachineName,CatalogName #| ForEach 
#Get-BrokerMachine -MachineName $_.MachineName -Property LoadIndex,FaultState,InMaintenanceMode,SessionsPending,SessionCount
