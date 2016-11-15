#!/usr/bin/env python
# -*- cdoing: utf-8 -*-
from . import db


class Location(db.Model):
    """docstring for Location"""
    id = db.Column(db.Integer, primary_key=True)
    campus = db.Column(db.String(100), nullable=False)
    building_name = db.Column(db.String(100), nullable=False)
    room_name = db.Column(db.String(100), nullable=False)
    uuid = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, campus, building_name, room_name, uuid):
        self.campus = campus
        self.building_name = building_name
        self.room_name = room_name
        self.uuid = uuid


class devData(db.Model):
    """docstring for devData"""
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.String(100), nullable=False)
    humidity = db.Column(db.String(100), nullable=False)
    pm2_5 = db.Column(db.String(100), nullable=False)
    noise = db.Column(db.String(100), nullable=False)
    dev_temp = db.Column(db.String(100), nullable=False)
    dev_qua = db.Column(db.String(100), nullable=False)
    valtage = db.Column(db.String(100), nullable=False)

    def __init__(
            self, uuid, datetime, temperature, humidity, pm2_5,
            noise, dev_temp, dev_qua, valtage):
        self.uuid = uuid
        self.datetime = datetime
        self.temperature = temperature
        self.humidity = humidity
        self.pm2_5 = pm2_5
        self.noise = noise
        self.dev_temp = dev_temp
        self.dev_qua = dev_qua
        self.valtage = valtage


class lastestRecord(db.Model):
    """docstring for lastestRecord"""
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.String(100), nullable=False)
    humidity = db.Column(db.String(100), nullable=False)
    pm2_5 = db.Column(db.String(100), nullable=False)
    noise = db.Column(db.String(100), nullable=False)
    dev_temp = db.Column(db.String(100), nullable=False)
    dev_qua = db.Column(db.String(100), nullable=False)
    valtage = db.Column(db.String(100), nullable=False)

    def __init__(
            self, uuid, datetime, temperature, humidity, pm2_5,
            noise, dev_temp, dev_qua, valtage):
        self.uuid = uuid
        self.datetime = datetime
        self.temperature = temperature
        self.humidity = humidity
        self.pm2_5 = pm2_5
        self.noise = noise
        self.dev_temp = dev_temp
        self.dev_qua = dev_qua
        self.valtage = valtage
