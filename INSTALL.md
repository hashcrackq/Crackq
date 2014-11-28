Installation
============

Update your "requests" library version if are getting the following error message:

Traceback (most recent call last):
  File "./crackqcli.py", line 113, in <module>
    print 'Results will be emailed to %s' % r.json()['email']
TypeError: 'dict' object is not callable


This will update the "requests" library:

$ pip install requests --upgrade
