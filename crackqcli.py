#!/usr/bin/env python
#
# Vitaly Nikolenko
# vnik@hashcrack.org
# v0.1
import requests
import json
import sys
import getopt

######### CONFIGURATION ######### 
API_KEY = 'YOUR API KEY HERE'
#################################

url = "http://hashcrack.org/crackq/v0.1/submit"

def usage(argv0):
    print '%s [-t|--type] md5|ntlm hash' % argv0
    print '-t --type        hash type, either md5 or ntlm'
    print '-h --help        help'

def validate_hash(_hash):
    if len(_hash) != 32:
        print 'Invalid hash'
        return False
    try:
        int(_hash, 16)
    except ValueError:
        print 'The hash is not in hex'
        return False

    return True

if __name__ == '__main__':
    _hash = None
    _type = None

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

    _hash = args[0]
     
    if not validate_hash(_hash):
        sys.exit(-1)
                
    if not _type or (_type != 'ntlm' and _type != 'md5'):
        print 'Hash type is invalid'
        sys.exit(-1)

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = {'key': API_KEY, 'hash': _hash, 'type': _type}

    r = requests.post(url, data=json.dumps(data), headers=headers)

    if r.status_code != 201:
        print 'There was an error submitting the hash.'
    print r.json()['msg']
