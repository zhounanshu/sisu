#!/usr/bin/python env
# -*- coding: utf-8 -*-
import hexdump
import socket
from wifi_config import *
from dbConnection import *
import select
import os
import sys

config = set_time()
config_type = 2

port = 1881
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', port))
s.setblocking(0)
# print "waitting on port:", port
frame_id = []
box = []
error_count = 0
count = 0

# 产生子进程，而后父进程退出
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
# 重定向标准输入流、标准输出流、标准错误
sys.stdout.flush()
sys.stderr.flush()
si = file('/dev/null', 'r')
so = file('/dev/null', 'a+')
se = file('/dev/null', 'a+', 0)
os.dup2(si.fileno(), sys.stdin.fileno())
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())
# 孙子进程的程序内容
while True:
    ready = select.select([s], [], [], 2)
    if ready[0]:
        data, addr = s.recvfrom(4096)
        result = hexdump.dump(data)
        # print "Received:", result, "from", addr
        if result[:8] == "3C 3C 3C":
            raw_data = result.split(' ')
            frame_head = raw_data[: 3]
            frame_content = raw_data[3: -5]
            crc_check = raw_data[-5: -3]
            frame_end = raw_data[-3:]
            frame_type = toInt(frame_content[:2])
            if frame_type == 3:
                if toInt(checkCRC(frame_content)) != toInt(crc_check):
                    print checkCRC(frame_content), crc_check
                    print "crc check error!"
                    continue
                else:
                    if not configFailed():
                        print "config successful........"
            elif frame_type == 4:
                if toInt(checkCRC(frame_content)) != toInt(crc_check):
                    print checkCRC(frame_content), crc_check
                    print "crc check error!"
                    continue
                else:
                    device_id = toInt(
                        get_data(frame_content, wifi_config_frame, 3))
                    frequency = toInt(
                        get_data(frame_content, wifi_config_frame, 13))
                    jiange = toInt(
                        get_data(frame_content, wifi_config_frame, 14))
                    ssid1 = toString(
                        get_data(frame_content, wifi_config_frame, 21))
                    passwd = toString(
                        get_data(frame_content, wifi_config_frame, 23))
                    msg = Frame(config_type, config).frame
                    s.sendto(msg, addr)
            elif frame_type == 100:
                show = {}
                count += 1
                if toInt(checkCRC(frame_content)) != toInt(crc_check):
                    # print checkCRC(frame_content), crc_check
                    print "crc check error!"
                    error_count = count
                else:
                    frame_id += frame_content[2: 6]
                    sample_time = toTime(
                        get_data(frame_content, wdsdhwwd_frame, 2))
                    device_id = toInt(
                        get_data(frame_content, wdsdhwwd_frame, 3))
                    voltage = toInt(
                        get_data(frame_content, wdsdhwwd_frame, 5))
                    ele_quantity = toInt(
                        get_data(frame_content, wdsdhwwd_frame, 6))
                    device_temp = str(toInt(
                        get_data(frame_content, wdsdhwwd_frame, 7)) * 0.01)
                    temperature = toFloat(
                        get_data(frame_content, wdsdhwwd_frame, 13))
                    humidity = toFloat(
                        get_data(frame_content, wdsdhwwd_frame, 14))
                    noise = toFloat(
                        get_data(frame_content, wdsdhwwd_frame, 15))
                    pm2_5 = toFloat(
                        get_data(frame_content, wdsdhwwd_frame, 16))
                    show["time"] = sample_time
                    show["temperature"] = temperature
                    show['humidity'] = humidity
                    show['noise'] = noise
                    show['pm2_5'] = pm2_5
                    show['device_id'] = device_id
                    show['voltage'] = voltage
                    show['ele_quantity'] = ele_quantity
                    show['device_temp'] = device_temp
                    box.append(show)
    else:
        if count > 30:
            error_count = 0
        if len(frame_id) > 0:
            if error_count != 0:
                frame_id = frame_id[:error_count]
                box = box[: error_count]
            if len(frame_id) <= 120:
                frame_id_append = [
                    '00' for i in range(120 - len(frame_id))]
                frame_id += frame_id_append
                answer = Frame(1, frame_id)
            else:
                answer = Frame(1, frame_id[: 120])
            data_answer_frame = answer.frame
            s.sendto(data_answer_frame, addr)
            Post(box)
            box = []
            frame_id = []
            count = 0
