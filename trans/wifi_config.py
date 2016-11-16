#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import struct

time_start = "2000-01-01 00:00:00"
base_time = datetime.datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S")
wifi_config_frame = [2, 4, 4, 4, 2, 1, 1, 1, 4, 4, 4, 4, 4, 2, 2, 4, 2, 40, 4,
                     2, 40, 32, 1, 32, 1, 32, 1, 32, 1, 1, 4, 4, 4, 4, 4, 4, 4,
                     4, 4, 4, 4, 4, 4]
config_answer_frame = [2, 4, 1]
wdsdhwwd_frame = [2, 4, 4, 4, 1, 1, 1, 2, 2, 2, 2, 4, 2, 4, 4, 4, 4]
wifi_data_answer_frame = [2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                          4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]


def get_data(frame, frame_lens, order):
    count = 0
    i = 0
    for value in frame_lens:
        if i == order:
            start = count
            end = count + value
            break
        count += value
        i += 1
    result = frame[start: end]
    return result


def toString(values):
    temp = ''
    for value in values:
        if value is not "00":
            temp += value.decode('hex')
    return temp


def toInt(values):
    i = len(values)
    temp = 0
    for value in values:
        i -= 1
        weight = 256 ** i
        temp += int(value, 16) * weight
    return temp


def toIp(values):
    ip = ''
    for temp in values:
        ip += str(int(temp, 16))
        ip += '.'
    return ip[: -1]


def toTime(value):
    temp = base_time + datetime.timedelta(seconds=toInt(value))
    return temp.strftime('%Y-%m-%d %H:%M:%S')


def toFloat(values):
    temp = ''
    if len(values) < 4:
        values = ['00' for i in range(4 - len(values))] + values
    for value in values:
        temp += value
    return str(struct.unpack('f', temp.decode('hex'))[0])


def checkCRC(message):
    u8MSBInfo = 0x00
    u16CrcData = 0xffff
    for data in message:
        u16CrcData = u16CrcData ^ int(data, 16)
        for i in range(8):
            u8MSBInfo = u16CrcData & 0x0001
            u16CrcData = u16CrcData >> 1
            if u8MSBInfo != 0:
                u16CrcData = u16CrcData ^ 0xA001
    return int_to_hex(u16CrcData, 2)


def crc16(x):
    b = 0xA001
    a = 0xFFFF
    for byte in x:
        a = a ^ int(byte, 16)
        for i in range(8):
            last = a % 2
            a = a >> 1
            if last == 1:
                a = a ^ b
    aa = '0' * (6 - len(hex(a))) + hex(a)[2:]
    return aa
# CONFIG_FRAME


def int_to_hex(para, length):
    result = []
    temp = []
    data = str(format(para, 'x'))
    if (len(data)) < 2 * length:
        for i in range(2 * length - len(data)):
            data = '0' + data
    for i in range(len(data) / 2):
        result.append(data[2 * i: 2 * i + 2])
    distance = length - len(result)
    if distance != 0:
        temp = ['00' for n in range(distance)]
    return temp + result


def str_to_hex(para, length):
    result = []
    temp = []
    data = para.encode('hex')
    result = [data[2 * i: 2 * i + 2] for i in range(len(data) / 2)]
    distance = length - len(result)
    if distance != 0:
        temp = ['00' for i in range(distance)]
    return result + temp


def set_time():
    config_type = ['00', '02']
    delta_time = datetime.datetime.now() - base_time
    delta_seconds = delta_time.seconds + delta_time.days * 24 * 3600
    return config_type + int_to_hex(delta_seconds, 4)


# set frequency mins
def set_frequency(mins):
    config_type = ['00', '09']
    return config_type + int_to_hex(mins, 2)


# set send intervals
def set_intervals(counts):
    config_type = ['00', '0A']
    return config_type + int_to_hex(counts, 2)


# set sever ip and port
def set_host(host, port, flag):
    if flag == 1:
        config_host_type = ['00', '0B']
        config_port_type = ['00', '0C']
    elif flag == 2:
        config_host_type = ['00', '0E']
        config_port_type = ['00', '0F']
    else:
        print "you are setting wrong flag!"
    host_list = []
    elements = host.split('.')
    for element in elements:
        host_list += int_to_hex(int(element), 1)
    port_list = int_to_hex(port, 2)
    addr_host = config_host_type + host_list
    addr_port = config_port_type + port_list
    return addr_host + addr_port


# set ssid and password
def set_wifi(ssid, passwd, flag):
    if flag == 1:
        config_ssid_type = ['00', '11']
        config_pwd_type = ['00', '13']
    elif flag == 2:
        config_ssid_type = ['00', '14']
        config_pwd_type = ['00', '16']
    else:
        print "with ssid: you are setting wrong flag!"
    ssid_config = config_ssid_type + str_to_hex(ssid, 32)
    passwd_config = config_pwd_type + str_to_hex(passwd, 32)
    return ssid_config + passwd_config


# config answer frame
def configFailed(frame):
    flag = True
    device_id = toInt(frame[2: 6])
    if toInt(frame[6]) == 0:
        flag = False
        print "the device", device_id, "config failed!"
        return flag


class Frame(object):

    def __init__(self, frame_type, arg):
        self.frame_type = int_to_hex(frame_type, 2)
        self.arg = arg
        self.start = ['3C', '3C', '3C']
        self.end = ['3E', '3E', '3E']
        self.temp = ''
        self.crc = checkCRC(self.frame_type + self.arg)
        temp = self.start + self.frame_type + self.arg + self.crc + self.end
        frame = ''
        for value in temp:
            frame += value
        self.temp = frame
        self.frame = frame.decode('hex')

    def get_frame(self):
        return self.frame
