from flask import Blueprint
from flask_restful import Api

semd = Blueprint('SEMD', __name__)
semd_api = Api(semd)


from .views import *
semd_api.add_resource(devLocation, '/v1/location')
semd_api.add_resource(devRecords, '/v1/dev/data')
semd_api.add_resource(latestRec, '/v1/latest/view')
semd_api.add_resource(latestDevRecord, '/v1/latest/data')
