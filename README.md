Crackq Client
=============

Crackq is an online distributed GPU-accelerated password cracker designed to
help penetration testers and network auditors check for weak passwords. It
supports a number of hash types and we are actively adding new algorithms.

Login to your account (https://hashcrack.org/crackq) to get the API key.

Installation
-----------

Refer to (https://hashcrack.org/crackq/page?n=install) for complete
installation instructions for Windows, Linux and OS X.

Hash Formats
------------

Currently, the following algorithms are supported:

* NTLM
* MD5
* SHA1
* WPA / WPA2 PSK
* VPN IPSec IKE (aggressive mode) MD5
* descrypt / DES(Unix)
* md5crypt / FreeBSD MD5 / Cisco IOS MD5 / MD5(Unix)
* PHPass MD5 (Wordpress, Joomla, phpBB3)

Submitting Hashes
-----------------

Refer to our FAQ for detailed instructions on submitting hashes
(https://hashcrack.org/crackq_faq).

```
$ ./crackqcli.py -h
Crackq client 0.3.1
support@hashcrack.org

./crackqcli.py [-t|--type hash_type] [hash|file_path]
-t --type        see supported hash types below
-h --help        help

Supported hash types:
md5              Unsalted MD5 hashes
ntlm             Windows NTLM hashes
sha1             Unsalted SHA1 hashes
wpa              WPA/WPA2 handshakes
md5crypt         MD5CRYPT / FreeBSD MD5 / Cisco IOS MD5 / MD5(Unix)
descrypt         DESCRYPT / DES(Unix)
ike_md5          VPN IPSec IKE (MD5) preshared keys
phpass           phpass (Wordpress, Joomla and phpBB3)
```
