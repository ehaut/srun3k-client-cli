#!/usr/bin/python
# -*- coding: utf-8 -*-
#!Design by CHN-STUDENT
#!Using on Python 3 and Python2.7


from __future__ import absolute_import, division, print_function, \
    with_statement

import logging	
from srun.encrypt import username_encrypt,password_encrypt
import six
from srun import status

def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s


def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s

def login(config):
    logging.info('Start to login.')
    username = username_encrypt(config['username'])
    password = password_encrypt(config['password'])
    login_data = six.moves.urllib.parse.urlencode([('action','login'),
                              ('username',username),
                              ('password',password),
                              ('drop',config['drop']),
                              ('pop',config['pop']),
                              ('type',config['type']),
                              ('n','117'),
                              ('mbytes','0'),
                              ('minutes','0'),
                              ('ac_id',config['acid']),
                              ('mac',config['mac'])
                              ])
    try:
		#req = 'http://172.16.154.130:69/cgi-bin/srun_portal'
        req ='http://'+config['server_addr']+':'+str(config['server_port'])+'/cgi-bin/srun_portal'
        d = to_bytes(login_data)
        f = six.moves.urllib.request.urlopen(req,data=d)
        response=to_str(f.read())
        if response.startswith('login_ok'):
            logging.info('Login successfully!')
            response = status.GetStatus(config)
            user_status = status.CheckStatus(response)
        elif response == 'login_error#E2553: Password is error.':
            logging.error('Your password is error.')
        elif response == 'login_error#E2531: User not found.':
            logging.error('Can not find your account.')
        elif response == 'login_error#INFO failed, BAS respond timeout.':
            logging.error('Acid is error,you need to change it,\n'
                            '                             e.g. # srun-cli -u username -k password -a 2')
    except six.moves.urllib.error.URLError as e:  
        logging.error(e)
        sys.exit(1)
    
def logout(config):
	logging.info('Start to logout.')
	username = username_encrypt(config['username'])
	logout_data = six.moves.urllib.parse.urlencode([('action','logout'),
							  ('username',username),
							  ('type',config['type']),
							  ('mac',config['mac']),
							  ('ac_id',config['acid'])
							  ])
	try:
		#req = 'http://172.16.154.130:69/cgi-bin/srun_portal'
		req ='http://'+config['server_addr']+':'+str(config['server_port'])+'/cgi-bin/srun_portal'
		d = to_bytes(logout_data)
		f = six.moves.urllib.request.urlopen(req,data=d)
		response=to_str(f.read())
		if response == 'logout_ok':
			logging.info('Logout successfully!')
		elif response == 'login_error#You are not online.':
			logging.warn('You are not online.')
	except six.moves.urllib.error.URLError as e:  
		logging.error(e)
		sys.exit(1)
	