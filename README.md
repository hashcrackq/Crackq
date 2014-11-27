Crackq Client
=============

Login to your account (http://hashcrack.org/login) to get the API key.

Currently, the two supported formats are md5, ntlm and WPA/WPA2.

WPA/WPA2
--------

`$ wpaclean out.cap captured.cap`

`$ aircrack-ng out.cap -J /tmp/tosubmit.hccap`

`$ ./crackqcli.py -t wpa /tmp/tosubmit.hccap`

MD5/NTLM
--------

`$ ./crackqcli.py -t md5 06aa3b7d55df43e7d7fa4aef94811e4a`
