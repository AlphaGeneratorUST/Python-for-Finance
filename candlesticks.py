import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates


style.use('ggplot')

start = dt.datetime(2017,1,1)
end = dt.datetime.now()

df = web.DataReader('TSLA', 'yahoo', start, end)
# print(df.head())
df.to_csv('TSLA.csv')
# df.plot()
# plt.show()

# df['Adj Close'].plot()
# plt.show()

df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
# print(df.head())

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

# plt.show()

df1 = pd.read_csv('TSLA.csv', parse_dates=True, index_col=0)
# print(df1.head())

df_ohlc = df1['Adj Close'].resample('10D').ohlc()
df_volume = df1['Volume'].resample('10D').sum()

# print(df_ohlc, df_volume)

df_ohlc.reset_index(inplace=True)
print(df_ohlc['Date'])
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
print(df_ohlc['Date'])

ax3 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax4 = plt.subplot2grid((6,1), (5,0), colspan=1, rowspan=1, sharex=ax3)

ax3.xaxis_date()

candlestick_ohlc(ax3, df_ohlc.values, width=5, colorup='g')
ax4.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()

