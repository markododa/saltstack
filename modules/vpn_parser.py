import sys

def parse_list_as_dict(parsed_list, index = 0):
    return {parsed_list[i][index] : {parsed_list[0][j] : parsed_list[i][j] for j in range(0, len(parsed_list[i]))} for i in range(1, len(parsed_list))}

def parse_list(parsed_list):
    return [{parsed_list[0][j] : parsed_list[i][j] for j in range(0, len(parsed_list[i]))} for i in range(1, len(parsed_list))]

def parse_data(data):
    #First separate tables to routing and client list
    client_list, routing_table = data.split('ROUTING TABLE')

    #Then separate routing table from global stats
    routing_table, global_stats = routing_table.split('GLOBAL STATS')

    #Separate each list by rows and then each row by values in that row and trim some unneeded lines.
    #Client list has 2 lines we don't need - the one that says CLIENT LIST and the 'last updated' one. 
    #Global stats has a couple lines we need to avoid. 
    client_list, routing_table, global_stats = [client.split(',') for client in client_list.split('\n')[2:] if client], [entry.split(',') for entry in routing_table.split('\n') if entry], global_stats.split('\n')[1:-2]

    #Create dictionaries for client list and routing table
    client_list = parse_list(client_list)
    routing_table = parse_list(routing_table)
    return {'client_list' : client_list, 'routing_table' : routing_table, 'global_stats' : global_stats}

def open_and_parse_log(log_file):
    log_file = open(log_file, 'r').read()
    return parse_data(log_file)

def get_logins(log_file = '/var/log/openvpn.log'):
    data = open(log_file, 'r').read()
    data = [x.split(' ') for x in data.split('\n') if 'Peer Connection Initiated' in x]
    return [{'login_time' : ' '.join(x[0:4]), 'ip_address' : x[5], 'username' : x[6][1:-1]} for x in data]

def get_logins_for_user(username, log_file = '/var/log/openvpn.log'):
    return [x for x in get_logins(log_file) if x['username'] == username]

def main():
    log_file = sys.argv[1]
    print open_and_parse_log(log_file)

if __name__ == "__main__":
    main()
