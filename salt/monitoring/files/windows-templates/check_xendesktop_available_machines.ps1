#################################################################################
#
# NAME: 	check_xendesktop_available_machines.ps1
#
# COMMENT:  Script to check how many  machines are available in a Citrix XenDesktop 
#           Desktopgroup with Icinga/Nagios + NRPE/NSClient++
# 
#           The script has to be executed on the server which is running XenDesktop Brokerservice
#
#			NRPE Handler to use with NSClient++:
#			[NRPE Handlers]
#           command[check_xendesktop_available_machines]=cmd /c echo scripts\check_xendesktop_available_machines.ps1 "$ARG1$" "$ARG2$" "$ARG3$"; exit($lastexitcode) | powershell.exe -command -
#
#
# ARGUMENTS: 
# 1: Name of the Desktopgroup which should be checked
# 2: warning value
# 3: critical value
#
#
# CHANGELOG:
# 1.0  2015-08-13 - initial version
#           
#################################################################################
# Copyright (C) 2015 Mark Rittinghaus, rittinghaus.mark@lumberg.com
#
# This program is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software 
# Foundation; either version 3 of the License, or (at your option) any later 
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with 
# this program; if not, see <http://www.gnu.org/licenses>.
#################################################################################

$DesktopGroupName = $args[0]
$wlevel = $args[1]
$clevel = $args[2]

$returnStateOK = 0
$returnStateWarning = 1
$returnStateCritical = 2
$returnStateUnknown = 3

asnp citrix*
import-module -name citrix.xendesktop.admin
$BrokerServiceStatus = Get-BrokerServiceStatus
#Check BrokerServiceStatus
if ( $BrokerServiceStatus.ServiceStatus -ne "OK" )
    { 
    $NagiosDescription = "Critical - BrokerServiceStatus is $BrokerServiceStatus.ServiceStatus"
    $NagiosStatus = $returnStateCritical 
    }
else
    {
    #Get available machines 
    $available_machines = (get-brokermachine -SummaryState Available -DesktopGroupName "$DesktopGroupName").count    

     if ($available_machines -gt $wlevel) {
            $NagiosStatus = $returnStateOK
        } elseif ($available_machines -lt $clevel) {
            $NagiosStatus = $returnStateCritical
        } elseif ($available_machines -lt $wlevel) {
            $NagiosStatus = $returnStateWarning
        } else {

            $NagiosStatus = $returnStateUnknown
        }    
        $NagiosPerfData = "|available_machines=" + $available_machines + ";" + $wlevel + ";" + $clevel
        $NagiosDescription = "$available_machines machines available"
    }
    
#Output     
if ($NagiosStatus -eq "2") 
{
	Write-Host "CRITICAL: " $NagiosDescription" "$NagiosPerfData
} 
elseif ($NagiosStatus -eq "1")
{
	Write-Host "WARNING: " $NagiosDescription" "$NagiosPerfData
} 
elseif ($NagiosStatus -eq "0")
{
	Write-Host "OK: " $NagiosDescription" "$NagiosPerfData
} 
else 
{
	Write-Host "UNKOWN: " $NagiosDescription" "$NagiosPerfData
    $NagiosStatus = $returnStateUnknown
}

exit $NagiosStatus		