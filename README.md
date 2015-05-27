Crackq Client
=============

Login to your account (https://hashcrack.org/crackq) to get the API key. Hash formats are 


Installation
-----------

Refer to (https://hashcrack.org/crackq/page?n=install) for complete installation instructions for Windows, Linux and OS X.

Hash Formats
------------

Currently, the following algorithms are supported:

* NTLM
* MD5
* SHA1
* WPA/WPA2 PSK
* VPN IPSec IKE (aggressive mode) MD5
* DESCRYPT / DES(Unix)
* MD5CRYPT / FreeBSD MD5 / Cisco IOS MD5 / MD5(Unix)
* PHPASS MD5 Wordpress, Joomla, phpBB3

WPA/WPA2
--------

To submit your your handshake:

`$ wpaclean out.cap captured.cap`

`$ aircrack-ng out.cap -J /tmp/tosubmit`

`$ ./crackqcli.py -t wpa /tmp/tosubmit.hccap`

Refer to (https://hashcrack.org/crackq/page?n=wpa) for details.

MD5/SHA1/NTLM
-------------

`$ ./crackqcli.py -t md5 [hash]`

`$ ./crackqcli.py -t ntlm [hash]`

SHA1 hashes are 40 hex characters:

`$ ./crackqcli.py -t sha1 35029a2e592be14756b3bd91fbf873d9e2885713`

DESCRYPT/DES(Unix)
------------------

`$ ./crackqcli.py -t descrypt [hash]`

MD5CRYPT/MD5(Unix)
------------------

`$ ./crackqcli.py -t md5crypt '$1$abcdefgh$WSwV3CmjYt3iE5AlESn9Z.'`

IPSec IKE PSK
-------------

Refer to (https://hashcrack.org/crackq/page?n=ike) for details.
