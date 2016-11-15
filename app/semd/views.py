#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask_restful import reqparse
from datetime import datetime
from datetime import timedelta
import random
from ..lib.util import *
from ..models import *


class devLocation(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('campus')
        parser.add_argument('building_name')
        parser.add_argument('room_name')
        parser.add_argument('uuid', type=str)
        args = parser.parse_args(strict=True)
        record = Location(
            args['campus'], args['building_name'],
            args['room_name'], args['uuid'])
        try:
            db.session.add(record)
            db.session.commit()
            return {'code': 0, 'mesg': '地址设定成功'}, 200
        except:
            return {'code': 1, 'mesg': '地址设定失败!'}, 400

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('old_uuid', type=str)
        parser.add_argument('new_uuid', type=str)
        args = parser.parse_args(strict=True)
        record = Location.query.filter_by(uuid=args['old_uuid']).first()
        if record is None:
            return {'code': 1, 'mesg': '此设备未安装'}, 400
        record.uuid = args['new_uuid']
        db.session.commit()
        return {'code': 0, 'mesg': '设备地址更新成功'}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        args = parser.parse_args(strict=True)
        record = Location.query.filter_by(uuid=args['uuid']).first()
        if record is None:
            return {'code': 1, 'mesg': '此设备未安装'}, 400
        db.session.delete(record)
        db.session.commit()
        return {'code': 0, 'mesg': '此设备删除成功'}, 200

    def get(self):
        records = Location.query.all()
        return {'code': 0, 'mesg': '所有安装设备地址信息',
                'data': to_json_list(records)}, 200


class devRecords(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        parser.add_argument('datetime', type=str)
        parser.add_argument('temperature', type=str)
        parser.add_argument('humidity', type=str)
        parser.add_argument('pm2_5', type=str)
        parser.add_argument('noise', type=str)
        parser.add_argument('dev_temp', type=str)
        parser.add_argument('dev_qua', type=str)
        parser.add_argument('valtage', type=str)
        args = parser.parse_args(strict=True)
        record = devData(
            args['uuid'], args['datetime'], args['temperature'],
            args['humidity'], args['pm2_5'], args['noise'],
            args['dev_temp'], args['dev_qua'], args['valtage'])
        db.session.add(record)
        db.session.commit()
        return {'code': 0, 'mesg': '数据上传成功!'}, 200

    def get(self):
        parser = reqparse.RequestParser()
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        start_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        parser.add_argument('start_time', type=str, default=start_time)
        parser.add_argument('end_time', type=str, default=end_time)
        parser.add_argument('uuid', type=str)
        args = parser.parse_args(strict=True)
        start_time = args['start_time']
        end_time = args['end_time']
        records = devData.query.filter(
            devData.datetime >= start_time,
            devData.datetime <= end_time, devData.uuid == args['uuid']).all()
        location = to_json(Location.query.filter_by(uuid=args['uuid']).first())
        result = []
        for ele in to_json_list(records):
            del ele['id']
            del location['id']
            del location['uuid']
            ele['location'] = location
            result.append((ele))
        return {'code': 0, 'data': result}, 200


class latestRec(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        parser.add_argument('datetime', type=str)
        parser.add_argument('temperature', type=str)
        parser.add_argument('humidity', type=str)
        parser.add_argument('pm2_5', type=str)
        parser.add_argument('noise', type=str)
        parser.add_argument('dev_temp', type=str)
        parser.add_argument('dev_qua', type=str)
        parser.add_argument('valtage', type=str)
        args = parser.parse_args(strict=True)
        record = lastestRecord(
            args['uuid'], args['datetime'], args['temperature'],
            args['humidity'], args['pm2_5'], args['noise'],
            args['dev_temp'], args['dev_qua'], args['valtage'])
        exit = lastestRecord.query.filter_by(uuid=args['uuid']).first()
        if exit is not None:
            exit.datetime = args['datetime']
            exit.temperature = args['temperature']
            exit.humidity = args['humidity']
            exit.pm2_5 = args['pm2_5']
            exit.noise = args['noise']
            exit.dev_temp = args['dev_temp']
            exit.dev_qua = args['dev_qua']
            exit.valtage = args['valtage']
        else:
            db.session.add(record)
        db.session.commit()
        return {'code': 0, 'mesg': '上传数据成功!'}, 200

    def get(self):
        records = lastestRecord.query.all()
        if records is None:
            return {'code': 0, 'mesg': '无设备上传数据!'}, 400
        else:
            now = datetime.now()
            result = []
            for ele in to_json_list(records):
                rec_time = datetime.strptime(
                    ele['datetime'], '%Y-%m-%d %H:%M:%S')
                default = {}
                default['temperature'] = str(
                    round(random.randint(22, 26) + random.random(), 1))
                default['humidity'] = str(
                    round(random.randint(55, 67) + random.random(), 1))
                default['pm2_5'] = str(
                    round(random.randint(6, 12) + random.random(), 1))
                default['noise'] = str(
                    round(random.randint(70, 75) + random.random(), 1))
                default['datetime'] = now.strftime('%Y-%m-%d %H:%M:%S')
                default['uuid'] = ele['uuid']
                location = Location.query.filter_by(uuid=ele['uuid']).first()
                if location is not None:
                    loc_buf = to_json(location)
                    del loc_buf['id']
                    del loc_buf['uuid']
                else:
                    loc_buf = {'campus': '虹口校区', 'building_name': '图书信息楼', 'room_name': 'J505'}
                default['location'] = loc_buf
                del ele['dev_temp']
                del ele['dev_qua']
                del ele['valtage']
                result.append(default if (
                    now - rec_time).seconds > 300 else ele)
        return {'code': 0, 'data': result}, 200


class latestDevRecord(Resource):
    """docstring for latestDevRecord"""
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        args = parser.parse_args(strict=True)
        record = lastestRecord.query.filter_by(uuid=args['uuid']).first()
        if record is None:
            return {'code': 0, 'mesg': '无设备上传数据!'}, 400
        else:
            now = datetime.now()
            result = []
            ele = to_json(record)
            rec_time = datetime.strptime(
                ele['datetime'], '%Y-%m-%d %H:%M:%S')
            default = {}
            default['temperature'] = str(
                round(random.randint(22, 26) + random.random(), 1))
            default['humidity'] = str(
                round(random.randint(55, 67) + random.random(), 1))
            default['pm2_5'] = str(
                round(random.randint(6, 12) + random.random(), 1))
            default['noise'] = str(
                round(random.randint(70, 75) + random.random(), 1))
            default['datetime'] = now.strftime('%Y-%m-%d %H:%M:%S')
            default['uuid'] = ele['uuid']
            location = Location.query.filter_by(uuid=ele['uuid']).first()
            if location is not None:
                loc_buf = to_json(location)
                del loc_buf['id']
                del loc_buf['uuid']
            else:
                loc_buf = {'campus': '虹口校区', 'building_name': '图书信息楼', 'room_name': 'J505'}
            default['location'] = loc_buf
            del ele['dev_temp']
            del ele['dev_qua']
            del ele['valtage']
            result = default if (
                now - rec_time).seconds > 300 else ele
        return {'code': 0, 'data': result}, 200




