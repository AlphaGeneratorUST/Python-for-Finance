import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
from statsmodels.tsa.arima_model import ARIMA

plt.rcParams.update({'figure.figsize': (9, 7), 'figure.dpi': 120})


# Load the 5min bar data
path = "C:/Users/huobi/quant/data/test_minbar/futures_data"
ticker = "btcusdt"
df = pd.read_csv("{}/huobi_{}_5min_bar.csv".format(path, ticker), index_col=0, parse_dates=True)
df['lag1_rtn'] = df['close'].pct_change()
# print(df.head(20))
# print(len(df))
df['lag1_rtn'].plot()
plt.show()

# Test the stationarity of df['lag1_rtn']
test_period = 10*24*15
result = adfuller(df['lag1_rtn'][:-test_period].dropna())
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

# Adf Test / KPSS Test / PP Test
ADF_test = ndiffs(df['lag1_rtn'][:-test_period].dropna(), test='adf')
print(ADF_test)
KPSS_test = ndiffs(df['lag1_rtn'][:-test_period].dropna(), test='kpss')
PP_test = ndiffs(df['lag1_rtn'][:-test_period].dropna(), test='PP')

# Find the order of the AR term [p]: p = 0
plot_pacf(df['lag1_rtn'][:-test_period].dropna())
plt.show()

# Find the order of the MA term [q]: q = 0
plot_acf(df['lag1_rtn'][:-test_period].dropna())
plt.show()

# Build the ARIMA model
model = ARIMA(df['lag1_rtn'][:-test_period], order=(0, 0, 0))
model_fit = model.fit()
print(model_fit.summary())

# Plot residual errors
residuals = pd.DataFrame(model_fit.resid)
fig, ax = plt.subplots(1,2)
residuals.plot(title="Residuals", ax=ax[0])
residuals.plot(kind='kde', title='Density', ax=ax[1])
plt.show()

# Actual vs Fitted
model_fit.plot_predict(dynamic=False)
plt.show()


# Create Training and Test
train = df.value[:85]
test = df.value[85:]

# Build Model
model = ARIMA(train, order=(3, 2, 1))
fitted = model.fit(disp=-1)
print(fitted.summary())

# Forecast
fc, se, conf = fitted.forecast(15, alpha=0.05)  # 95% conf

# Make as pandas series
fc_series = pd.Series(fc, index=test.index)
lower_series = pd.Series(conf[:, 0], index=test.index)
upper_series = pd.Series(conf[:, 1], index=test.index)

# Plot
plt.figure(figsize=(12,5), dpi=100)
plt.plot(train, label='training')
plt.plot(test, label='actual')
plt.plot(fc_series, label='forecast')
plt.fill_between(lower_series.index, lower_series, upper_series,
                 color='k', alpha=.15)
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=8)
plt.show()
