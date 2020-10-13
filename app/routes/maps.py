from app import app, ns_root, ns_base
from app.schemas import rp_coins_schema
from app.common import utils

from flask_restplus import Resource
from flask import Response, request, render_template, url_for, make_response

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import io

import logging

class Converter:
    
    @staticmethod
    def request_to_obj(req):
        class NewObject(object):
            def __init__(self, **kwargs):
                self.__dict__ = kwargs
        new_object = NewObject(**req.json)
        return new_object

@ns_root.route("/api/version")
class Version(Resource):
    
    @ns_root.doc(description='Get version')
    def get(self):
        return {'version': f"v{app.config.get('APP_VERSION')}"}
    

@ns_root.route("/maps")
class Maps(Resource):
    
    @ns_root.doc(description='Get info about maps.')
    def get(self):
        return make_response(render_template('index.html'))
    
    @ns_root.expect(rp_coins_schema)
    @ns_root.doc(description='Get map for the currency.')
    def post(self):
        try:
            coins_data = Converter.request_to_obj(request)
            if utils.Transform.create_map(coins_data):
                return {'code': 200, 'status': 'Success'}
            else:
                return {'code': 401, 'status': 'Data Transform Failed'}
        except BaseException as ex:
            logging.error('An Error occurred while getting currency map:')
            logging.error(ex)
            return {
                'code': 400,
                'error': str(ex)
            }
            
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response