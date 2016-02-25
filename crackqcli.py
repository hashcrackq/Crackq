#!/usr/bin/env python
#
# Hashcrack Crackq command line client
#
# Email: support[at]hashcrack.org
# Web:   hashcrack.org

import json
import sys
import getopt
import os
import zlib
import base64
import re
from urllib2 import Request, urlopen, URLError, HTTPError

SERVER = 'https://hashcrack.org'
CONFIG_PATH = None
ENDPOINTS = {
                'user_email' : '/crackq/v0.1/user_email',
                'submit'     : '/crackq/v0.1/submit',
                'client_ver' : '/crackq/v0.1/client_ver'
            }
API_KEY = None
MYVER = '0.4'
HASH_TYPES = ['wpa',
              'descrypt',
              'md5crypt',
              'md5',
              'ntlm',
              'sha1',
              'pdf',
              'phpass',
              'mysql']

def banner():
    sys.stdout.write('Crackq client %s\n' % MYVER)
    sys.stdout.write('support@hashcrack.org\n\n')

def usage(argv0):
    sys.stdout.write('%s [-t|--type hash_type] [hash|file_path]\n' % argv0)
    sys.stdout.write('-t --type        see supported hash types below\n')
    sys.stdout.write('-h --help        help\n\n')
    sys.stdout.write('Supported hash types:\n')
    sys.stdout.write('md5              Unsalted MD5 hashes\n')
    sys.stdout.write('ntlm             Windows NTLM hashes\n')
    sys.stdout.write('sha1             Unsalted SHA1 hashes\n')
    sys.stdout.write('wpa              WPA/WPA2 handshakes\n')
    sys.stdout.write('md5crypt         MD5CRYPT / FreeBSD MD5 / Cisco IOS MD5 / MD5(Unix)\n')
    sys.stdout.write('descrypt         DESCRYPT / DES(Unix)\n')
    sys.stdout.write('pdf              PDF 1.4 - 1.6\n')
    sys.stdout.write('phpass           PHPASS (Wordpress, Joomla and phpBB3)\n')
    sys.stdout.write('mysql            MYSQL4.1+ (double SHA1)\n')

def validate_hash(_hash, _hash_type):
    if _hash_type == 'descrypt':
       if re.match('^[\./0-9A-Za-z]{13,13}$', _hash) is None:
           return False
    elif _hash_type == 'md5crypt':
       if re.match('^\$1\$[\./0-9A-Za-z]{0,8}\$[\./0-9A-Za-z]{22,22}$', _hash) is None:
           return False
    elif _hash_type == 'phpass':
       if re.match('^\$[PH]\$[0-9A-Z][./0-9A-Za-z]{30,30}$', _hash) is None:
           return False
    elif _hash_type == 'pdf':
       if re.match('^\$pdf\$[0-9A-Z][./0-9A-Za-z]{30,30}$', _hash) is None:
           return False
    elif _hash_type == 'sha1' or _hash_type == 'mysql':
        if len(_hash) != 40:
            sys.stdout.write('[-] ERROR: Invalid hash\n')
            return False
        try:
            int(_hash, 16)
        except ValueError:
            sys.stdout.write('[-] ERROR: The hash is not in hex\n')
            return False
    else:
        if len(_hash) != 32:
            sys.stdout.write('[-] ERROR: Invalid hash\n')
            return False
        try:
            int(_hash, 16)
        except ValueError:
            sys.stdout.write('[-] ERROR: The hash is not in hex\n')
            return False
    return True

def save_config():
    global API_KEY
    global CONFIG_PATH

    sys.stdout.write('Enter your API key: ')
    key = sys.stdin.readline().strip()

    try:
        conf = open(CONFIG_PATH, 'w')
    except IOError:
        sys.stdout.write('[-] ERROR: Cannot write to %s\n' % CONFIG_PATH)
        sys.exit(-1)

    conf.write('key:%s\n' % key)
    API_KEY = key

def load_config():
    global API_KEY
    global CONFIG_PATH

    if os.name == 'nt':
        CONFIG_PATH = os.getenv('APPDATA') + '\Crackq.cfg'
    elif os.name == 'posix':
        CONFIG_PATH = os.getenv("HOME") + '/.crackq'
    else:
        sys.stdout.write('[-] ERROR: Unsupported OS\n')
        sys.exit(-1)
    try:
        conf = open(CONFIG_PATH, 'r')
        for l in conf.readlines():
            k, v = l.split(':')
            if k == 'key':
                API_KEY = v.strip()
        if not API_KEY:
	    sys.stdout.write('[-] ERROR: API KEY NOT FOUND\n')
            sys.exit(-1)
    except IOError:
        save_config()

if __name__ == '__main__':
    _type = None
    banner()

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 't:huq:', ['type=', 'help', 'update'])
    except getopt.GetoptError as err:
        print str(err)
        usage(sys.argv[0])
        sys.exit(-1)

    for o, a in optlist:
       if o in ('-h', '--help'):
           usage(sys.argv[0])
           sys.exit(0)
       if o in ('-u', '--update'):
           os.system('git pull')
           sys.exit(0)
       if o in ('-t', '--type'):
           _type = a

    try:
        # check for updates
        sys.stdout.write('[+] Checking the current client version...\n')
        if urlopen(SERVER + ENDPOINTS['client_ver']).read() != MYVER:
            sys.stdout.write('[-] WARNING: NEW CLIENT VERSION IS AVAILABLE: https://hashcrack.org/crackq/page?n=install#update\n')
            sys.exit(-1)

        if len(args) != 1:
           usage(sys.argv[0])
           sys.exit(-1)

        _content = args[0]
         
        if not _type or _type not in HASH_TYPES:
            sys.stdout.write('[-] ERROR: INVALID HASH TYPE\n')
            sys.exit(-1)

        if (_type != 'wpa' and _type != 'pdf') and not validate_hash(_content, _type):
            sys.stdout.write('[-] ERROR: INVALID HASH FORMAT\n')
            sys.exit(-1)
                    
        load_config()

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = {'key': API_KEY}

        sys.stdout.write('[+] Retrieving email...\n')
        req = Request(SERVER + ENDPOINTS['user_email'])
        req.add_header('Content-Type', 'application/json')
        res = urlopen(req, json.dumps(data))
        data = json.load(res)
        sys.stdout.write('[+] Results will be emailed to: %s\n' % data['email'])
        sys.stdout.write('[+] Submissions left: %s\n' % data['privq_limit'])

        if (data['privq_limit'] > 0):
            sys.stdout.write('[+] Sending to the queue...\n')
        else:
	    sys.stdout.write('[-] ERROR: NO QUEUE SUBMISSIONS LEFT. PURCHASE SUBMISSION QUOTA AT https://hashcrack.org/crackq_buy\n')
            sys.exit(-1)

        if _type == 'wpa':
            try:
                f = open(_content, 'rb')
            except IOError:
                sys.stdout.write('[-] ERROR: Cannot find %s\n' % _content)
                sys.exit(-1)
    
            _raw = f.read()
            if _type == 'wpa' and len(_raw) != 392:
                sys.stdout.write('[-] ERROR: hccap file is invalid or multiple essids detected\n')
                sys.exit(-1)

            _content = base64.b64encode(zlib.compress(_raw))
            f.close()

        data = {'key': API_KEY, 'content': _content, 'type': _type, 'q': 'privq'}
        req = Request(SERVER + ENDPOINTS['submit'])
        req.add_header('Content-Type', 'application/json')
        res = urlopen(req, json.dumps(data))
        sys.stdout.write('[+] Done\n')
    except HTTPError as e:
        sys.stdout.write('[-] ERROR: HTTP %d - %s\n' % (e.code, json.load(e)['msg']))
        sys.exit(-1)
    except URLError as e:
        sys.stdout.write('[-] ERROR: UNREACHABLE - %s\n' % e.reason)
        sys.exit(-1)
