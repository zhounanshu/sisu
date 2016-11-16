#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from config import *
import datetime
import json
import urllib2

data = {
  "device_id":"1144",
  "time": "2016-11-16 12:52:22",
  "temperature": "25.4",
  "humidity": "63.3",
  "pm2_5": "7",
  "noise": "53",
  "device_temp": "21.2",
  "ele_quantity": "94",
  "voltage": "4.3"
}

def uploadFlow(data, url):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    jdata = json.dumps(data)
    try:
        response = urllib2.urlopen(req, jdata.encode('utf-8'))
    except:
        with open('log.txt', 'a+') as f:
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log = time + ': ' + url + '\n'
            f.writelines(log)
            f.close()

def Post(arg):
        # for arg in args:
        buf = {}
        buf['datetime'] = arg["time"]
        buf['temperature'] = arg["temperature"]
        buf['humidity'] = arg['humidity']
        buf['noise'] = arg['noise']
        buf['pm2_5'] = arg['pm2_5']
        buf['uuid'] = arg['device_id']
        buf['valtage'] = arg['voltage']
        buf['dev_qua'] = arg['ele_quantity']
        buf['dev_temp'] = arg['device_temp']
        print buf
        uploadFlow(buf, post_urls['latestURL'])
        uploadFlow(buf, post_urls['devDataURL'])








