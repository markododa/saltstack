// Proxy auto-config script

function FindProxyForURL(url, host)
{
	//return "PROXY PROXY_HOST.DOMAIN:8080; PROXY va-proxy2.DOMAIN:8080; DIRECT";
	return "PROXY PROXY_HOST:8080; DIRECT";
}
