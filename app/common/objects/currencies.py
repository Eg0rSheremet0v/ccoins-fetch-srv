from app import CLIENT

from datetime import datetime

import logging

class Kline(object):
    
    def __init__(self, *args):
        self.open_timestamp = args[0]
        self.open = args[1]
        self.high = args[2]
        self.low = args[3]
        self.close = args[4]
        self.volume = args[5]
        self.close_timestamp = args[6]
        self.quote_asset_volume = args[7]
        self.n_trades = args[8]
        self.taker_buy_base_asset_volume = args[9]
        self.taker_buy_quote_asset_volume = args[10]
        self.ignore = args[11]    
        
    def __repr__(self):
        desc_string = ""
        close_date = datetime.fromtimestamp(int(self.close_timestamp) / 1000)
        desc_string += f"open time: {self.open_date} -- close time: {self.close_date}\n"
        desc_string += f"open price: {self.open} -- close price: {self.high}\n"
        desc_string += f"high price: {self.high} -- low price: {self.low}\n"
        desc_string += f"volume: {self.volume}\n"
        return desc_string
    
    @property
    def close_data(self):
        return (self.close_date, self.close)
    
    @property
    def volume_data(self):
        return (self.close_date, self.volume)
    
    @property
    def open_data(self):
        return (self.open_date, self.open)
    
    @property
    def open_date(self):
        return datetime.fromtimestamp(int(self.open_timestamp) / 1000)
    
    @property
    def close_date(self):
        return datetime.fromtimestamp(int(self.close_timestamp) / 1000)
    

class CoinsCurrency(object):
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name

    @property
    def price(self):
        response = CLIENT.get_symbol_ticker(symbol=self.name)
        return response.get('price')
            
    def historical_data(self, interval, time_range_start, time_range_stop = None):
        response = CLIENT.get_historical_klines(self.name, interval, time_range_start, time_range_stop)
        klines = [Kline(*data) for data in response]
        return klines
