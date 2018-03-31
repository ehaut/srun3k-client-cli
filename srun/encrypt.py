#!/usr/bin/python
# -*- coding: utf-8 -*-
#!Design by CHN-STUDENT
#!Using on Python 3 and Python2.7


from __future__ import absolute_import, division, print_function, \
    with_statement

import os
import sys
import logging

#from srun.common import to_bytes,to_str

def username_encrypt(username):
    result = '{SRUN3}\r\n'
    return result + ''.join([chr(ord(x) + 4) for x in username])


def password_encrypt(password, key='1234567890'):
    result = list()
    for i in range(len(password)):
        ki = ord(password[i]) ^ ord(key[len(key) - i % len(key) - 1])
        _l = chr((ki & 0x0F) + 0x36)
        _h = chr((ki >> 4 & 0x0F) + 0x63)

        if i % 2 == 0: result.extend((_l, _h))
        else: result.extend((_h, _l))
    return ''.join(result)

