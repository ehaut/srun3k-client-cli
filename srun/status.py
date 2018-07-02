#!/usr/bin/python
# -*- coding: utf-8 -*-
#!Design by CHN-STUDENT
#!Using on Python 3 and Python2.7

import six
import logging
import sys

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

def GetStatus(config):
	server='http://'+config['server_addr']+':'+str(config['server_port'])+'/cgi-bin/rad_user_info'
	try:
		#f = six.moves.urllib.request.urlopen('http://172.16.154.130/cgi-bin/rad_user_info')
		f = six.moves.urllib.request.urlopen(server)
		return to_str(f.read()) #Byte to string
	except six.moves.urllib.error as e:  
		logging.error(e)
		sys.exit(1)
		

def CheckStatus(data):	
		if data.startswith('not_online'): #if user is not online
			return 0
		else:		#if user is online
			output='''
You are already online.
#########################
#  Here are your info:  #
#########################
Username: '''	
			infolist=[
						data.split(',')[0], #username
						str(float(data.split(',')[6])/1073741824), #data
						str(int(int(data.split(',')[7])/3600)),#Hours
						str(int(int(data.split(',')[7])/60%60)),#Mintues
						str(int(int(data.split(',')[7])%60)),#Seconds
						data.split(',')[8] #IP
					 ]
			output=output+infolist[0]+'\nData: '+infolist[1]+' GB\nTime: '+infolist[2]+'  Hours  '+infolist[3]	\
					+'  Mintues  '+infolist[4]+'  Seconds\nIP: '+infolist[5]+'\n#########################'
			logging.info(output)
			#print(output)
			return 1


if __name__ == '__main__':
	response = GetStatus()
	CheckStatus(response)