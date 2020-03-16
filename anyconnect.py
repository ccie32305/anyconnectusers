#/usr/bin/env python
import sys
import re
import requests
import getpass
import socket
import os
import threading
import datetime
from netmiko import ConnectHandler
from netaddr import *
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
ASA_LIST = ['asa_a','asa_b','asa_c']

def get_anyconnect_users(ip):
        cisco_asa = {
        'device_type': 'cisco_asa',
        'ip': ip,
        'username': USERNAME,
        'password': PASSWORD,
        'secret': PASSWORD,
        'verbose': False,
        }
        net_connect = ConnectHandler(**cisco_asa)
        net_connect.enable()
        show_vpn_summary = net_connect.send_config_set("show vpn-")
        net_connect.disconnect()
        for line in show_vpn_summary.splitlines():
                if 'Total Active' in line:
                        return int(re.search('\d+',line).group(0))
while 1:
        file = open('anyconnect.csv',"a")
        sum = 0
        entry = ""
        entry = entry + str(datetime.datetime.now()) + ";"
        for device in ASA_LIST:
                try:
                        result = get_anyconnect_users(device)
                        entry = entry + str(result) + ';'
                        sum = sum + result
                        print('{0:10s} : {1:3d}'.format(device, result))
                except:
                        pass
        print(f'SUM      : {sum}')
        entry = entry + str(sum) + ";"
        print(datetime.datetime.now())
        file.write(entry + "\n")
        file.close()
