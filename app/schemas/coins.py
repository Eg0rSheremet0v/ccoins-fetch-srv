import flask_restplus as rp
from app import api

def create_schema():
    data = {
        'base_coin': rp.fields.String(required=True, description='Base coin of the currency'),
        'target_coin': rp.fields.String(required=True, description='Target coin of the currency'),
        'interval': rp.fields.String(required=True, description='Interval of messurements. <1m/30m/1H/4H/1M/...>'),
        'start_time': rp.fields.String(required=True, description='Start time. <1 Jan, 2020>'),
        'end_time': rp.fields.String(required=True, description='End time. <1 Aug, 2020>'),
        'groupby_first_value': rp.fields.String(required=True, description='First value of groupping method <minute, hour, day, month, year>'),
        'groupby_second_value': rp.fields.String(required=True, description='Second value of groupping method <minute, hour, day, month, year>'),
    }
    return data

rp_coins_schema = api.model('Currency Data', create_schema())