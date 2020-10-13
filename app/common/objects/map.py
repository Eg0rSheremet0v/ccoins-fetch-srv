import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sbn

class CurrencyMap(object):
    
    def __init__(self, cur_name):
        self.cur_name = cur_name

    
    def _to_df(self, data, groupby_first, groupby_second):
        data = np.array(data)
        coin_df = pd.DataFrame(data, columns=["DATE", self.cur_name])
        coin_df = coin_df.set_index("DATE")
        coin_df[self.cur_name] = pd.to_numeric(coin_df[self.cur_name], errors='coerce')
        coin_df.dropna(inplace=True)
        df_m = coin_df.copy()
        groupping_data = {
            'minute': [i.minute for i in df_m.index],
            'hour': [i.hour for i in df_m.index],
            'day': [i.day for i in df_m.index],
            'month': [i.month for i in df_m.index],
            'year': [i.year for i in df_m.index]
        }
        df_m[groupby_first] = groupping_data[groupby_first]
        df_m[groupby_second] = groupping_data[groupby_second]
        df_m = df_m.groupby([groupby_first, groupby_second]).mean()
        df_m = df_m.unstack(level=0)
        return df_m
    
    def generate(self, data, groupby_first, groupby_second, file_name, target_name):
        df = self._to_df(data, groupby_first, groupby_second)
        fig, ax = plt.subplots(figsize=(11, 9))
        sbn.heatmap(df).set_title(f"Heatmap of {target_name} <{self.cur_name}>").figure.savefig(file_name)
        