from flask import Blueprint, flash, jsonify, request, Response
from flask_restful import Api, Resource, url_for
import flasky
geofirstrecord_blueprint = Blueprint('geofirstrecord', __name__, template_folder='templates')
api = Api(geofirstrecord_blueprint)

class GeoFirstRecordResourceful(Resource):
    def post(self, key, username):
        response = Response() 
        response.status = 200
        if (flasky.getUtils().get_post_key != key):
            response = jsonify({'status': 'error', 'message': 'Wrong key'})
            response.status=401 #Unauthorized
            return response
        response.content_type = 'text/plain'
        response.mimetype = 'text/plain'
        response.data = "successfully logged in"
        with open('geofirstrecord.txt', 'a') as f:
            f.write(f'"{username}" logged in at {str(flasky.getUtils().get_universal_time)}')
            f.close()
        return response
        

class GeoFirstRecord(Resource):
    def get(self):
        data = {}
        time = flasky.getUtils().get_local_time
        data['message'] = 'Hello from geofirstrecord module!'
        data['time'] = time.__str__()
        data['url'] = url_for('geofirstrecord.geofirstrecord')
        response = jsonify(data)
        response.status = 200
        return response



api.add_resource(GeoFirstRecord, '/')
api.add_resource(GeoFirstRecordResourceful, '/<string:key>/<string:username>')