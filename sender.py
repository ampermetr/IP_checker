#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2016 Ampermetr <user@localhost>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import socket
import time
import os

addr = str(server_ip)
port = int(server_port)

try:
    with open ('/home/user/myip') as file:
        last_ip = file.read()
except:
    last_ip = ""
    
while True:
    ip = os.popen("wget -O - -q icanhazip.com").read()
    if ip != last_ip:
        with open ('home/user/myip') as file:
            file.write(ip)
        last_ip = ip
        
        sock = socket.socket()
        sock.connect((addr, port))
        text = ("name_PC~" + ip + "~" + time.ctime(time.time())).encode("utf-8")
        sock.send(text)
        sock.close()
    time.sleep(600)
