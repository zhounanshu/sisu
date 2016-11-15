#!/usr/bin/env python
# -*- coding: utf-8 -*-


def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object. """
    json = {}
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        json[col.name] = getattr(model, col.name)
    return json


def to_json_list(model_list):
    json_list = []
    for model in model_list:
        json_list.append(to_json(model))
    return json_list
