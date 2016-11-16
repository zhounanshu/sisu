#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import os
import sys
address = ('', 8081)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

while True:
    data, addr = s.recvfrom(2048)
    if not data:
        print "client has exist"
        break
    with open('log.txt', 'a+') as f:
        log = addr[0] + ": " + data + "\n"
        f.write(log)
        f.close()
s.close()
