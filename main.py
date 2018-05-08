import requests, os, getpass, pickle, time
from urllib.parse import quote

def main():
    sess = requests.Session()
    ret = ''
    while True:
        host = 'http://210.77.16.21/'
        response = sess.get(host, allow_redirects=False)

        logout_url = response.headers['location']
        response = sess.get(logout_url, allow_redirects=False)

        login_information = response.headers['location']

        def information():# {{{
            if not os.path.isdir('./data'):
                os.mkdir('./data')
            if os.path.isfile('./data/user'):
                with open('./data/user', 'rb') as f:
                    return pickle.load(f)
            username = input('username: ')
            passwd = getpass.getpass('password: ')    
            with open('./data/user', 'wb') as f:
                pickle.dump([username, passwd], f)
            return username, passwd
        # }}}

        username, passwd = information()
        cookies = login_information[login_information.find('?')+1:]

        if cookies[:9] == 'userIndex':
            userIndex = cookies[10:]
            logout = 'http://210.77.16.21/eportal/InterFace.do?method=logout'
            sess.post(logout, {'userIndex': userIndex})
            print('[LOG] logout')
            ret += '[LOG] logout<br>'
            time.sleep(2)
        else:
            break

    data = {# {{{
        'userId': quote(username),
        'password': passwd,
        'service': '',
        'queryString': cookies,
        'operatorPwd': '',
        'operatorUserId': '',
        'validcode': '',
        'passwordEncrypt': 'false',
    }# }}}

    login = 'http://210.77.16.21/eportal/InterFace.do?method=login'
    response = sess.post(login, data=data)
    response.encoding = 'utf-8'

    print('[LOG] server return', response.json()['result'])
    ret += '[LOG] server return' + response.json()['result'] + '<br>'
    return ret

if __name__ == '__main__':
    main()

