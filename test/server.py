#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import os
import datetime
import sys
import hexdump

address = ('', 808)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

pid = os.fork()
if pid > 0:
    sys.exit(0)
# 修改子进程工作目录
os.chdir('/')
# 创建新的会话，子进程成为会话的首进程
os.setsid()
# 修改工作目录的umask
os.umask(0)
# 创建孙子进程, 而后子进程退出
pid = os.fork()
if pid > 0:
    sys.exit(0)

while True:
    data, addr = s.recvfrom(2048)
    if not data:
        print "client has exist"
        break
    with open('log.txt', 'a+') as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': \n'
        log = addr[0] + ": " + hexdump.dump(data)+ "\n"
        f.write(now + log)
        f.close()
s.close()
