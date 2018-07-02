#!/usr/bin/python
# -*- coding: utf-8 -*-
#!Design by CHN-STUDENT
#!Using on Python 3 and Python2.7

from __future__ import absolute_import, division, print_function, \
    with_statement

import sys
import os
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from srun import shell,status,common
#from srun.common import login,logout
#from srun import encrypt

def main():
	shell.check_python()

	# fix py2exe
	if hasattr(sys, "frozen") and sys.frozen in \
			("windows_exe", "console_exe"):
		p = os.path.dirname(os.path.abspath(sys.executable))
		os.chdir(p)

	config = shell.get_config()
	
	response = status.GetStatus(config)
	user_status = status.CheckStatus(response)
	if ((user_status == 0) and (config['method'] == 'login' or not config['method'])):
		common.login(config)
	elif ((user_status == 1) and (config['method'] == 'logout' or not config['method'])):
		common.logout(config)
	elif ((user_status == 0) and (config['method'] == 'logout')):
		logging.warn('\nYou are not online.If you want to login,\n'
					 'please using # srun-cli -u username -k password -m login ,\n'
					 'or input method with none.')
	elif ((user_status == 1) and (config['method'] == 'login')):
		logging.warn('\nYou are online.If you want to logout,\n'
					 'please using # srun-cli -u username -k password -m logout ,\n'
					 'or input method with none.')

if __name__ == '__main__':
    main()