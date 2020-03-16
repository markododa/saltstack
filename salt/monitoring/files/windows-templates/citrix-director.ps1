function Global:Invoke-ODataTransform ($records) {

    $propertyNames = ($records | Select -First 1).content.properties |
        Get-Member -MemberType Properties |
        Select -ExpandProperty name

    foreach($record in $records) {

        $h = @{}
        $h.ID = $record.ID
        $properties = $record.content.properties

        foreach($propertyName in $propertyNames) {
            $targetProperty = $properties.$propertyName
            if($targetProperty -is [System.Xml.XmlElement]) {
                $h.$propertyName = $targetProperty.'#text'
            } else {
                $h.$propertyName = $targetProperty
            }
        }

        [PSCustomObject]$h
    }
}

$connections = ""
$uri = "http://localhost/Citrix/Monitor/OData/v1/Data/Sessions?`$expand=Connections"
$connections = Invoke-ODataTransform(Invoke-RestMethod -Uri $uri -UseDefaultCredentials)

foreach($connection in $connections)
{
    $output = $connection | Get-Member -MemberType Properties | ForEach-Object {
        $key = $_.Name
        $value = $connection.$key
        '{0}="{1}"' -f $key,$value
    }

    Write-Host $output
}

