#!/usr/bin/env python

import base64
import random
import string

'''
    Password must be at least 9 characters long.
    It should have:
        ABCDEFG... (atleast 2 uppercase characters)
        1234567... (atleast 2 digits)
        .?%*!+)... (atleast 1 punctuation/symbol)
        abcdefg... (lowercase characters)
'''

username = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
password = ("%s%s%s%s") % (''.join(random.choice(string.ascii_uppercase) for i in range(5)),
                           ''.join(random.choice(string.digits) for i in range(5)),
                           ''.join(random.choice(string.punctuation) for i in range(5)),
                           ''.join(random.choice(string.ascii_lowercase) for i in range(5)))

print "username = \"%s\"" % (username)
print "password = \"%s\"" % (password)
