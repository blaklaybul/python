import pandas as pd
from pandas.tseries.resample import TimeGrouper
from pandas.tseries.offsets import DateOffset

dodgers = pd.read_csv('/Users/Michael/Repos/python/TwitterStream/Dodgers.csv')
dodgers['created_at'] = pd.to_datetime(pd.Series(dodgers['created_at']))
dodgers.set_index('created_at', drop=False, inplace=True)
dodgers.index = dodgers.index.tz_localize('GMT').tz_convert('EST')
dodgers.index = dodgers.index - DateOffset(hours = 12)
dodgers.index