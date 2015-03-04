Crackq Client
=============

Login to your account (http://hashcrack.org/crackq) to get the API key.

Currently, the following algorithms are supported:

* MD5
* LM
* NTLM
* WPA / WPA2
* Cisco type 7
* Windows Group Policy Preferences (GPP) cpassword
* DESCRYPT / DES(Unix) 
* MD5CRYPT / MD5(Unix) 

WPA/WPA2
--------

To submit your your handshake to the private queue:

`$ wpaclean out.cap captured.cap`

`$ aircrack-ng out.cap -J /tmp/tosubmit`

`$ ./crackqcli.py -t wpa /tmp/tosubmit.hccap`

The private queue submission is similar except for the `-q privq` switch:

`$ ./crackqcli.py -q privq -t wpa /tmp/tosubmit.hccap`

MD5/LM/NTLM
-----------

`$ ./crackqcli.py -t md5 06aa3b7d55df43e7d7fa4aef94811e4a`

`$ ./crackqcli.py -t ntlm ab54d7ae46a72b05388ec24611c96a2d`

To submit to the private queue, use the `-q privq` switch:

`$ ./crackqcli.py -q privq -t md5 06aa3b7d55df43e7d7fa4aef94811e4a`

`$ ./crackqcli.py -q privq -t ntlm ab54d7ae46a72b05388ec24611c96a2d`

The LM hash is submitted as 32 hex-char value, i.e., two halves of the password:
 
`$ ./crackqcli.py -t lm f6dc2e4c788de157ff17365faf1ffe89`

For more information regarding LM hashes refer to the [Crackq FAQ](http://hashcrack.org/crackq_faq)

DESCRYPT/DES(Unix)
------------------

DES-based Unix crypt algorithm is supported by the private queue only:

`$ ./crackqcli.py -q privq -t descrypt ffTEQtUBN6Glk`

MD5CRYPT/MD5(Unix)
------------------

MD5-based Unix crypt algorithm is supported by the private queue only:

`$ ./crackqcli.py -q privq -t md5crypt '$1$abcdefgh$WSwV3CmjYt3iE5AlESn9Z.'`

Cisco type 7/Windows Group Policy Preferences (GPP)
-----------------------------------------------------

These are encodings which are reversible. There is no processing time
involved.

To submit your Cisco type 7 hash:

`$ ./crackqcli.py -t cisco_type7 your_cisco_type7_hash`

To submit your Windows GPP (Group Policy Preferences) `cpassword` hash (found in Groups.xml):

`$ ./crackqcli.py -t gpp your_cpassword_hash`
