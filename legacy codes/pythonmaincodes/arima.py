
# Working code:

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
import datetime



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

plt.figure()
plt.plot(df['Open'])
plt.title('TESLA Stock')
plt.show()

print(ad_test(df['Close']))


stepwise_fit = auto_arima(df['Close'], trace = True, suppress_warnings = True)
	
#the 3 lines of code below extracts the order of the best fit arima model.
summary_string = str(stepwise_fit.summary())
param = re.findall('SARIMAX\(([0-9]+), ([0-9]+), ([0-9]+)',summary_string)
p,d,q = int(param[0][0]) , int(param[0][1]) , int(param[0][2])



train_data, test_data = df[0:int(len(df['Close'])*0.7)], df[int(len(df['Close'])*0.7):]
#train_data=df.iloc[:-30]
#test_data=df.iloc[-30:]

training_data = train_data['Close'].values
test_data = test_data['Close'].values
history = [x for x in training_data]
model_predictions = []
N_test_observations = len(test_data)
for time_point in range(N_test_observations):
	model = ARIMA(history, order=(p,d,q))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	model_predictions.append(yhat)
	true_test_value = test_data[time_point]
	history.append(true_test_value)

pd.DataFrame(model_predictions).to_csv('prediction.csv')

mean = test_data.mean()
print("Mean is:", mean)

rmse = sqrt(mean_squared_error(test_data, model_predictions))
print('Testing Mean Squared Error is {}'.format(rmse))

'''
test_set_range = df[int(len(df)*0.7):].index
plt.plot(test_set_range, model_predictions, color='blue', marker='o', linestyle='dashed',label='Predicted Price')
plt.plot(test_set_range, test_data, color='red', label='Actual Price')
plt.title('TESLA Prices Prediction')
plt.xlabel('Date')
plt.ylabel('Prices')
plt.legend()
plt.show()
'''

final_predictions = []
for i in range(0,2):
	model = ARIMA(df['Close'], order=(p,d,q))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	final_predictions.append(yhat)
	
pd.DataFrame(final_predictions).to_csv('finalPrediction.csv')


'''
model2 = ARIMA(df['Close'], order=(p,d,q))
model2 = model2.fit()

start = datetime.date.today() + datetime.timedelta(days=1)
end = datetime.date.today() + datetime.timedelta(days=2)

index_future_dates = pd.date_range(start = start, end = end)

model_predictions2 = []
pred = model2.predict(start = len(df), end = len(df)+1).rename('Arima Prediction')


model_predictions2.append(pred)
pd.DataFrame(pred).to_csv('prediction2.csv')

pred = np.exp(pred)
pred.index = index_future_dates 
print(pred)
plt.figure(figsize=(8,6))
plt.plot(pred)
plt.title("company")
plt.show()
'''






















'''

# Working code:

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
import datetime



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


df = pd.read_csv("newcompanylist\CANBK.NS\swing trading\CANBK.NS.csv")

plt.figure()
plt.plot(df['Open'])
plt.title('TESLA Stock')
plt.show()

print(ad_test(df['Close']))


stepwise_fit = auto_arima(df['Close'], trace = True, suppress_warnings = True)
	
#the 3 lines of code below extracts the order of the best fit arima model.
summary_string = str(stepwise_fit.summary())
param = re.findall('SARIMAX\(([0-9]+), ([0-9]+), ([0-9]+)',summary_string)
p,d,q = int(param[0][0]) , int(param[0][1]) , int(param[0][2])



train_data, test_data = df[0:int(len(df['Close'])*0.7)], df[int(len(df['Close'])*0.7):]
training_data = train_data['Close'].values
test_data = test_data['Close'].values
history = [x for x in training_data]
model_predictions = []
N_test_observations = len(test_data)
for time_point in range(N_test_observations):
	model = ARIMA(history, order=(p,d,q))
    	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	model_predictions.append(yhat)
	true_test_value = test_data[time_point]
	history.append(true_test_value)

pd.DataFrame(model_predictions).to_csv('prediction.csv')

mean = test_data.mean()
print("Mean is:", mean)

rmse = sqrt(mean_squared_error(test_data, model_predictions))
print('Testing Mean Squared Error is {}'.format(rmse))


test_set_range = df[int(len(df)*0.7):].index
plt.plot(test_set_range, model_predictions, color='blue', marker='o', linestyle='dashed',label='Predicted Price')
plt.plot(test_set_range, test_data, color='red', label='Actual Price')
plt.title('TESLA Prices Prediction')
plt.xlabel('Date')
plt.ylabel('Prices')
plt.legend()
plt.show()


model2 = ARIMA(df['Close'], order=(p,d,q))
model2 = model2.fit()

start = datetime.date.today() + datetime.timedelta(days=1)
end = datetime.date.today() + datetime.timedelta(days=2)

index_future_dates = pd.date_range(start = start, end = end)

model_predictions2 = []
pred = model2.predict(start = len(df), end = len(df)+1).rename('Arima Prediction')


model_predictions2.append(pred)
pd.DataFrame(pred).to_csv('prediction2.csv')

pred = np.exp(pred)
pred.index = index_future_dates 
print(pred)
plt.figure(figsize=(8,6))
plt.plot(pred)
plt.title("company")
plt.show()






'''






