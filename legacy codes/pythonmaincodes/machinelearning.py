from scipy import stats
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.models import Sequential
import time
 
df = pd.read_csv('Companies\ADANIPORTS.NS\swing trading\ADANIPORTS.NS.csv')

# convert everything to logarithmic values first to apply central limit theorem. Read about it.
open_log = np.log(df['Open'])
high_log = np.log(df['High'])
low_log = np.log(df['Low'])
close_log = np.log(df['Close'])


df = pd.DataFrame({'Open': open_log,'High': high_log,'Low': low_log,'Close': close_log})

'''
scaler = MinMaxScaler()
scaler.fit(df)
NewData = scaler.transform(df)
'''

pd.set_option('display.max_rows', None)
#newdf = pd.DataFrame(NewData,columns=['Open','High','Low','Close'])
newdf = pd.DataFrame(df,columns=['Open','High','Low','Close'])

newdf.to_csv('logout.csv', index=False) 

