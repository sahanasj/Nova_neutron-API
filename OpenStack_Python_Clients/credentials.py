def get_credentials():
    d = {}    
    d['USER'] = raw_input('Enter Username:')
    d['PASS'] = raw_input('Enter password:')
    d['TENANT'] = raw_input('Enter Tenant Name:')
    d['IP'] = raw_input('Enter your Server IP:')
    d['AUTH_URL'] = str('http://'+ d['IP'] + ':5000/v2.0')
    return d

details = get_credentials()
