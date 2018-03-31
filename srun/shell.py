#!/usr/bin/python
# -*- coding: utf-8 -*-
#!Design by CHN-STUDENT
#!Using on Python 3 and Python2.7

from __future__ import absolute_import, division, print_function, \
    with_statement

import os
import json
import sys
import getopt
import logging

#from srun.common import action
from srun.common import to_bytes, to_str

VERBOSE_LEVEL = 5

verbose = 0

def check_python():
    info = sys.version_info
    if info[0] == 2 and not info[1] >= 6:
        print('Python 2.6+ required')
        sys.exit(1)
    elif info[0] == 3 and not info[1] >= 3:
        print('Python 3.3+ required')
        sys.exit(1)
    elif info[0] not in [2, 3]:
        print('Python version not supported')
        sys.exit(1)

def print_exception(e):
    global verbose
    logging.error(e)
    if verbose > 0:
        import traceback
        traceback.print_exc()


def print_srun():
    version = ''
    try:
        import pkg_resources
        version = pkg_resources.get_distribution('srun-cli').version
    except Exception:
        pass
    print('srun-cli %s' % version)


def find_config():
    config_path = 'config.json'
    if os.path.exists(config_path):
        return config_path
    config_path = os.path.join(os.path.dirname(__file__), '../', 'config.json')
    if os.path.exists(config_path):
        return config_path
    return None

def check_config(config):
	if not config.get('username', None):
		logging.error('username not specified')
		print_help()
		sys.exit(2)
	if not config.get('password', None):
		logging.error('password not specified')
		print_help()
		sys.exit(2)
	if 'SERVER_ADDR' in config:
		config['server_addr'] = str(config['server_addr'])
	if 'SERVER_PORT' in config:
		config['server_port'] = int(config['server_port'])
	if 'ACID' in config:
		config['acid'] = int(config['acid'])
	if 'TYPE' in config:
		config['type'] = int(config['type'])
	if 'DROP' in config:
		config['drop'] = int(config['drop'])
	if 'POP' in config:
		config['pop'] = int(config['pop'])
	if 'MAC' in config:
		config['mac'] = int(config['mac'])

def get_config():
    global verbose

    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-s: %(message)s')				
	
    shortopts = 'hvqs:p:u:k:m:a:P:t:d:M:c:'
    longopts = ['help', 'version']
    try:
        config_path = find_config()
        optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)

        for key, value in optlist:
            if key == '-c':
                config_path = value

        if config_path:
            logging.info('loading config from %s' % config_path)
            with open(config_path, 'rb') as f:
                try:
                    config = parse_json_in_str(f.read().decode('utf8'))
                except ValueError as e:
                    logging.error('found an error in config.json: %s',
                                  e.message)
                    sys.exit(1)
        else:
            config = {}

        v_count = 0
        for key, value in optlist:
            if key == '-s':
                config['server_addr'] = to_bytes(value)
            elif key == '-p':
                config['server_port'] = int(value)
            elif key == '-u':
                config['username'] = to_bytes(value)
            elif key == '-k':
                config['password'] = to_bytes(value)
            elif key == '-m':
                config['method'] = to_str(value)
            elif key == '-a':
                config['acid'] = to_bytes(value)
            elif key == '-P':
                config['POP'] = int(value)
            elif key == '-t':
                config['type'] = int(value)
            elif key == '-d':
                config['drop'] = int(value)
            elif key == '-M':
                config['mac'] = to_str(value)	
            
            elif key == '-v':
                v_count += 1
                # '-vv' turns on more verbose mode
                config['verbose'] = v_count
           
            elif key in ('-h', '--help'):
                print_help()
                sys.exit(0)
            elif key == '--version':
                print_srun()
                sys.exit(0)
           
            elif key == '-q':
                v_count -= 1
                config['verbose'] = v_count
    except getopt.GetoptError as e:
        print(e, file=sys.stderr)
        print_help()
        sys.exit(2)

    if not config:
        logging.error('config not specified')
        print_help()
        sys.exit(2)
        
    config['server_addr'] = to_str(config.get('server_addr', '172.16.154.130'))
    config['server_port'] = config.get('server_port', 69)	
    config['username'] = to_str(config.get('username', b''))
    config['password'] = to_str(config.get('password', b''))
    config['verbose'] = config.get('verbose', False)
    config['acid'] = config.get('acid',1)
    config['type'] = config.get('type',3)
    config['drop'] = config.get('drop',1)
    config['pop'] = config.get('pop',0)
    config['mac'] = to_str(config.get('mac',b'02:00:00:00:00:00'))
    config['method']=to_str(config.get('method',b''))
	
    logging.getLogger('').handlers = []
    logging.addLevelName(VERBOSE_LEVEL, 'VERBOSE')
    if config['verbose'] >= 2:
        level = VERBOSE_LEVEL
    elif config['verbose'] == 1:
        level = logging.DEBUG
    elif config['verbose'] == -1:
        level = logging.WARN
    elif config['verbose'] <= -2:
        level = logging.ERROR
    else:
        level = logging.INFO
    verbose = config['verbose']
    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    check_config(config)

    return config
						
		
def print_help():
	 print('''usage: srun-cli [OPTION]...
A Command line interface for Srun3k Client for HAUT

You can supply configurations via either config file or command line arguments.

Action Options:
  -c CONFIG              path to config file
  -s SERVER_ADDR         server address, default:172.16.154.130
  -p SERVER_PORT         server port, default:69
  -u USERNAME            username
  -k PASSWORD            password
  -a ACID            	 acid, default:1
  -t TYPE                type, default:3
  -d DROP                drop, default:0
  -P POP                 pop, default:1
  -M MAC                 MAC, default:02:00:00:00:00:00
  -m METHOD              action method:login or logout, default:accroding your status
						 
General Options:
  -h, --help             show this help message and exit
  -v, -vv                verbose mode
  --version              show version information
  
 Online help: <https://github.com/CHN-STUDENT/srun-cli>
	 
''')

def _decode_list(data):
    rv = []
    for item in data:
        if hasattr(item, 'encode'):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.items():
        if hasattr(value, 'encode'):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


def parse_json_in_str(data):
    # parse json and convert everything from unicode to str
    return json.loads(data, object_hook=_decode_dict)
