import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from pandas import datetime
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.preprocessing import MinMaxScaler
from pmdarima import auto_arima
from pmdarima.arima import ADFTest
import warnings
import re

warnings.filterwarnings("ignore")

def ad_test(dataset):
	dftest = adfuller(dataset, autolag="AIC")
	print("1. ADF:", dftest[0])
	print("2. p-value:", dftest[1])
	print("3. no. of lags:", dftest[2])
	print("4. no. of observations:", dftest[3])
	print("5. Critical values:", dftest[4])
	for key, val in dftest[4].items():
		print("\t",key, ":", val)

	return dftest[1]



df = pd.read_csv("newcompanylist\DRREDDY.NS\swing trading\DRREDDY.NS.csv")

'''
# convert everything to logarithmic values first to apply central limit theorem. Read about it.
open_log = np.log(df['Open'])
high_log = np.log(df['High'])
low_log = np.log(df['Low'])
close_log = np.log(df['Close'])

df = pd.DataFrame({'Date':df['Date'], 'Open': open_log,'High': high_log,'Low': low_log,'Close': close_log})

pd.set_option('display.max_rows', None)
newdf = pd.DataFrame(df,columns=['Date','Open','High','Low','Close'])
newdf.to_csv('logout.csv', index=False) 

df = pd.read_csv("logout.csv", index_col="Date", parse_dates=True)
df = df.dropna()
''' 

#if ad_test(df['Close'])<=0.05: #P-VALUE extracted from the ad_test function. For best results the p-value should be less than 0.05.
stepwise_fit = auto_arima(df['Close'], trace = True, suppress_warnings = True)
	
#the 3 lines of code below extracts the order of the best fit arima model.
summary_string = str(stepwise_fit.summary())
param = re.findall('SARIMAX\(([0-9]+), ([0-9]+), ([0-9]+)',summary_string)
p,d,q = int(param[0][0]) , int(param[0][1]) , int(param[0][2])	
#print(stepwise_fit.summary())

train, test = df[0:int(len(df)*0.9)], df[int(len(df)*0.9):]
print(train.shape, test.shape)

model = ARIMA(train['Close'], order=(p,d,q))
model = model.fit()
#print(model.summary())


start = len(train)
end=len(train)+len(test)-1
pred = model.predict(start=start, end=end)
pred.index=df.index[start:end+1]
print(pred)

pred.plot()
test['Close'].plot()


print("Avg is:", test['Close'].mean())

rmse = sqrt(mean_squared_error(pred, test['Close']))
print("Root mean square error:", rmse)


model2 = ARIMA(df['Close'], order=(p,d,q))
model2 = model2.fit()

index_future_dates = pd.date_range(start = '18-12-2020', end = '19-12-2020')
#pred = model2.predict(start = len(df), end = len(df)+1).rename('Arima Prediction')

final_predictions = []
pred = model2.forecast()
yhat = pred[0]
final_predictions.append(yhat)


pd.DataFrame(final_predictions).to_csv('finalPredictionarimacheck.csv')

'''
pred = np.exp(pred)
pred.index = index_future_dates 
print(pred)
plt.figure(figsize=(8,6))
plt.plot(pred)
plt.title("company")
plt.show()
'''

