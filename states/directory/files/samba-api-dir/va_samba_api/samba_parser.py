import sys, re

def parse_data(data):
    data = re.sub('\s\s+', ' ', data)
    data = [x.split(' ') for x in data.split('\n') if 'smbd_audit' in x]
    data = [{'date' : ' '.join(x[0:3]), 'instance' : x[3], 'service' : x[4], 'info' : x[5].split('|')} for x in data if len(x)>=5]
    for x in data:
        info = x['info']
        info[0] = info[0].split('\\')
        try:
            x['info'] = {'username' : info[0][1], 'domain' : info[0][0], 'address' : info[1], 'computer' : info[2], 'action' : info[3], 'success' : info[4], 'folder' : info[5]}
        except Exception :
            pass

    return data

def open_and_parse_log(log_file):
    log_file = open(log_file, 'r').read()
    return parse_data(log_file)

def get_logins_for_user(data, username, data_type = 'log'):
    if data_type == 'log' : data = open_and_parse_log(data)
    else : data = parse_data(data)
    return [x for x in data if x['info']['username'] == username]

def main():
    print open_and_parse_log('openstack_dashboard/salt_utils/fileshare.log')

if __name__ == "__main__":
    main()

