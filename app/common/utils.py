from app.common.objects import CoinsCurrency, CurrencyMap
from binance.client import Client

from datetime import datetime

class IntervalException(Exception):
    pass

class DateFormatException(Exception):
    pass


CURRENT_CURRENCY = 'BTCUSDT'


def get_currencies_list():
    clist = CoinsCurrency.get_currencies_list()
    clist = [value.get('symbol') for value in clist]
    return clist


class Transform():
    
    @staticmethod
    def _transform_interval(interval):
        data = {
            '1D': Client.KLINE_INTERVAL_1DAY,
            '1H': Client.KLINE_INTERVAL_1HOUR,
            '4H': Client.KLINE_INTERVAL_4HOUR,
            '30MIN': Client.KLINE_INTERVAL_30MINUTE
        }
        return data.get(interval.upper())
    
    @staticmethod
    def _transform_date(date):
        str_date = date.strftime('%d %b, %Y')
        return str_date
    
    @staticmethod
    def _validate_date(date_start, date_end):
        try:
            first_date = datetime.strptime(date_start, '%d %b, %Y')
            second_date = datetime.strptime(date_end, '%d %b, %Y')
            if second_date >= first_date:
                return True
            else:
                return False
        except ValueError:
            return False
        
    @staticmethod
    def _get_data(cur_data):
        global CURRENT_CURRENCY
        currency_name = ''.join([cur_data.base_coin, cur_data.target_coin])
        CURRENT_CURRENCY = currency_name
        cur_obj = CoinsCurrency(currency_name)
        interval = Transform._transform_interval(cur_data.interval)
        if not interval:
            raise IntervalException('Unknown interval!')
        k_lines = cur_obj.historical_data(interval, cur_data.start_time, cur_data.end_time)
        close_data = [kl.close_data for kl in k_lines]
        volume_data = [kl.volume_data for kl in k_lines]
        return close_data, volume_data
    
    @staticmethod
    def current_date():
        now = datetime.now()
        str_date = Transform._transform_date(now)
        return str_date
    
    @staticmethod
    def current_price():
        currency = CoinsCurrency(CURRENT_CURRENCY)
        return currency.price
    
    @staticmethod
    def create_map(data):
        cur_name = ''.join([data.base_coin, data.target_coin])
        if not Transform._validate_date(data.start_time, data.end_time):
            raise DateFormatException('Date format error. Check start_time or end_time.')
        close_data, volume_data = Transform._get_data(data)
        if all([close_data, volume_data]):
            heatmap = CurrencyMap(cur_name)
            heatmap.generate(close_data, data.groupby_first_value, 
                            data.groupby_second_value, 'app/static/output_price_map.png', 'Price')
            heatmap.generate(volume_data, data.groupby_first_value, 
                            data.groupby_second_value, 'app/static/output_volume_map.png', 'Volume')
            return True
        return False