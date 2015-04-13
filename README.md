Crackq Client
=============

Login to your account (https://hashcrack.org/crackq) to get the API key.

Currently, the following algorithms are supported:

* MD5
* SHA1
* NTLM
* WPA / WPA2
* DESCRYPT / DES(Unix) 
* MD5CRYPT / MD5(Unix) 
* IPSec IKE PSK (Aggressive Mode) MD5

WPA/WPA2
--------

To submit your your handshake:

`$ wpaclean out.cap captured.cap`

`$ aircrack-ng out.cap -J /tmp/tosubmit`

`$ ./crackqcli.py -t wpa /tmp/tosubmit.hccap`

Refer to (https://hashcrack.org/crackq/page?n=wpa) for details.

MD5/SHA1/NTLM
-------------

`$ ./crackqcli.py -t md5 06aa3b7d55df43e7d7fa4aef94811e4a`

`$ ./crackqcli.py -t ntlm ab54d7ae46a72b05388ec24611c96a2d`

SHA1 hashes are 40 hex characters:

`$ ./crackqcli.py -t sha1 35029a2e592be14756b3bd91fbf873d9e2885713`

DESCRYPT/DES(Unix)
------------------

`$ ./crackqcli.py -t descrypt ffTEQtUBN6Glk`

MD5CRYPT/MD5(Unix)
------------------

`$ ./crackqcli.py -t md5crypt '$1$abcdefgh$WSwV3CmjYt3iE5AlESn9Z.'`

IPSec IKE PSK
-------------

Refer to (https://hashcrack.org/crackq/page?n=ike) for details.
