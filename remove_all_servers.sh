echo ==================
echo Removing standalone servers
consul kv get providers/va_standalone_servers
consul kv put providers/va_standalone_servers remove_all_servers.json
echo ==================
echo Removing servers
consul kv get -recurse server
consul kv delete -recurse server
