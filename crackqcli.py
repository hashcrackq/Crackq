#!/usr/bin/env python
#
# support@hashcrack.org
# v0.18b

import json
import sys
import getopt
import os
import zlib
import base64
import re
from urllib2 import Request, urlopen, URLError, HTTPError

SERVER = 'https://hashcrack.org'
ENDPOINTS = {
                'user_email' : '/crackq/v0.1/user_email',
                'submit'     : '/crackq/v0.1/submit'
            }
API_KEY = None
PRIVQ_HASH_TYPES = ['wpa', 'descrypt', 'md5crypt', 'md5', 'ntlm']
PUBQ_HASH_TYPES  = ['lm', 'ntlm', 'md5', 'wpa', 'gpp', 'cisco_type7']

def banner():
    sys.stdout.write('hashcrack.org crackq client v0.18b\n\n')

def usage(argv0):
    print '%s [-q privq|pubq] [-t|--type] [md5|ntlm|lm|gpp|cisco_type7|wpa|md5crypt|descrypt] [hash|hccap]' % argv0
    print '-t --type        supported formats: md5, ntlm, lm, gpp, wpa, md5crypt or descrypt'
    print '-q               queue type: pubq or privq' 
    print '-h --help        help'

def validate_hash(_hash, _hash_type):
    if _hash_type == 'descrypt':
       if re.match('^[\./0-9A-Za-z]{13,13}$', _hash) is None:
           return False
    elif _hash_type == 'md5crypt':
       if re.match('^\$1\$[\./0-9A-Za-z]{0,8}\$[\./0-9A-Za-z]{22,22}$', _hash) is None:
           return False
    elif _hash_type == 'cisco_type7':
       if re.match('^[0-9][0-9][0-9A-Fa-f]+$', _hash) is None:
           return False
    elif _hash_type == 'gpp':
       #if len(_hash) != 43:
       #    return False
       # pad it if needed
       base64str_pad=_hash + (4 - len(_hash)%4) * '='
       try:
           cpassword = base64.b64decode(base64str_pad)
       except TypeError:
           print 'error'
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
	    sys.stdout.write('[-] ERROR: API KEY NOT FOUND\n')
            sys.exit(-1)
    except IOError:
        save_config()

if __name__ == '__main__':
    _type = None
    qtype = 'pubq'

    banner()

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 't:hq:', ['type=', 'help'])
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
       if o == '-q':
	   if a not in ('pubq', 'privq'):
	       sys.stdout.write('[-] ERROR: INVALID QUEUE TYPE\n')
	       sys.exit(-1)
           qtype = a

    if len(args) != 1:
       usage(sys.argv[0])
       sys.exit(-1)

    _content = args[0]
     
    if not _type or (_type not in PRIVQ_HASH_TYPES and _type not in PUBQ_HASH_TYPES):
	sys.stdout.write('[-] ERROR: INVALID HASH TYPE\n')
        sys.exit(-1)

    if qtype == 'privq' and _type not in PRIVQ_HASH_TYPES:
	sys.stdout.write('[-] ERROR: NOT SUPPORTED BY PRIVQ\n')
        sys.exit(-1)

    if qtype == 'pubq' and _type not in PUBQ_HASH_TYPES:
	sys.stdout.write('[-] ERROR: NOT SUPPORTED BY PUBQ\n')
        sys.exit(-1)

    if _type != 'wpa' and not validate_hash(_content, _type):
        sys.exit(-1)
                
    load_config()
 
    try:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = {'key': API_KEY}

	sys.stdout.write('[+] Retrieving email...\n')
        req = Request(SERVER + ENDPOINTS['user_email'])
        req.add_header('Content-Type', 'application/json')
        res = urlopen(req, json.dumps(data))
        data = json.load(res)
	sys.stdout.write('[+] Results will be emailed to: %s\n' % data['email'])
	sys.stdout.write('[+] Public queue submissions left: %s\n' % data['pubq_limit'])
	sys.stdout.write('[+] Private queue submissions left: %s\n' % data['privq_limit'])

        if qtype == 'pubq':
            if (data['pubq_limit'] > 0):
	        sys.stdout.write('[+] Sending to public queue...\n')
            else:
	        sys.stdout.write('[-] ERROR: NO PUBLIC QUEUE SUBMISSIONS LEFT\n')
                sys.exit(-1)
	else:
            if (data['privq_limit'] > 0):
	        sys.stdout.write('[+] Sending to private queue...\n')
            else:
	        sys.stdout.write('[-] ERROR: NO PRIVATE QUEUE SUBMISSIONS LEFT\n')
                sys.exit(-1)

        if _type == 'wpa':
            try:
                f = open(_content, 'r')
            except IOError:
		sys.stdout.write('[-] ERROR: Cannot find %s\n' % _content)
                sys.exit(-1)
    
            _raw = f.read()
            if len(_raw) != 392:
		sys.stdout.write('[-] ERROR: hccap file is invalid or multiple essids detected\n')
                sys.exit(-1)

            _content = base64.b64encode(zlib.compress(_raw))
            f.close()
     
	data = {'key': API_KEY, 'content': _content, 'type': _type, 'q': qtype}
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
