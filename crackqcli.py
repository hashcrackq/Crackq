#!/usr/bin/env python
#
# Vitaly Nikolenko
# vnik@hashcrack.org
# v0.15b

import json
import sys
import getopt
import os
import zlib
import base64
from urllib2 import Request, urlopen, URLError, HTTPError

SERVER = 'https://hashcrack.org'
ENDPOINTS = {
                'user_email' : '/crackq/v0.1/user_email',
                'submit'     : '/crackq/v0.1/submit'
            }
API_KEY = None

def banner():
    sys.stdout.write('hashcrack.org crackq client v0.15b\n\n')

def usage(argv0):
    print '%s [-t|--type] [md5|ntlm|lm|wpa] [hash|hccap]' % argv0
    print '-t --type        supported formats: md5, ntlm, lm or wpa'
    print '-h --help        help'

def validate_hash(_hash):
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

    home_path = os.getenv("HOME")
    sys.stdout.write('Enter your API key: ')
    key = sys.stdin.readline().strip()

    try:
        conf = open(home_path + '/.crackq', 'w')
    except IOError:
	sys.stdout.write('[-] ERROR: Cannot write to %s\n' % home_path)
        sys.exit(-1)
        
    conf.write('key:%s\n' % key)
    API_KEY = key

def load_config():
    global API_KEY

    home_path = os.getenv("HOME")
    try:
        conf = open(home_path + '/.crackq', 'r')
        for l in conf.readlines():
            k, v = l.split(':')
            if k == 'key':
                API_KEY = v.strip()
        if not API_KEY:
	    sys.stdout.write('[-] ERROR: API key is not found\n')
            sys.exit(-1)
    except IOError:
        save_config()

if __name__ == '__main__':
    _type = None
    banner()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 't:h', ['type=', 'help'])
    except getopt.GetoptError as err:
        print str(err)
        usage(sys.argv[0])
        sys.exit(-1)

    for o, a in optlist:
       if o in ('-h', '--help'):
           usage(sys.argv[0])
           sys.exit()
       if o in ('-t', '--type'):
           _type = a

    if len(args) != 1:
       usage(sys.argv[0])
       sys.exit(-1)

    _content = args[0]
     
    if not _type or (_type != 'ntlm' and _type != 'md5' and _type != 'lm' and _type != 'wpa'):
	sys.stdout.write('[-] ERROR: INVALID HASH TYPE\n')
        sys.exit(-1)

    if _type != 'wpa' and not validate_hash(_content):
        sys.exit(-1)
                
    load_config()
 
    try:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = {'key': API_KEY}

	sys.stdout.write('[+] Retrieving email...\n')
        req = Request(SERVER + ENDPOINTS['user_email'])
        req.add_header('Content-Type', 'application/json')
        res = urlopen(req, json.dumps(data))
	sys.stdout.write('[+] Results will be emailed to: %s\n' % json.load(res)['email'])

        if _type == 'wpa':
            try:
                f = open(_content, 'r')
            except IOError:
		sys.stdout.write('[-] ERROR: Cannot find %s\n' % _content)
                sys.exit(-1)
    
            _content = base64.b64encode(zlib.compress(f.read()))
            f.close()
    
            if len(_content) > 392:
		sys.stdout.write('[-] ERROR: Not a hccap file or multiple essids detected\n')
                sys.exit(-1)
     
	sys.stdout.write('[+] Sending the hash...\n')
        data = {'key': API_KEY, 'content': _content, 'type': _type}
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
