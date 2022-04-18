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

scaler = MinMaxScaler()
scaler.fit(df)
NewData = scaler.transform(df)

pd.set_option('display.max_rows', None)
newdf = pd.DataFrame(NewData,columns=['Open','High','Low','Close'])

newdf.to_csv('logout.csv', index=False) 

X_train, X_test, y_train, y_test = train_test_split(newdf, y, test_size=0.3, shuffle=False)
print(X_train)





















'''

train, test = train_test_split(newdf, test_size=0.3, shuffle=False)
print(train)


model = Sequential() 

input_layer = Dense(32, input_shape=(4,)) 
model.add(input_layer) 

hidden_layer = Dense(64, activation='relu') 
model.add(hidden_layer) 

output_layer = Dense(1) 
model.add(output_layer)

model.compile(loss='mse', optimizer='rmsprop', metrics = ['accuracy'])
model.fit(train,epochs=10, verbose=0)

'''






'''
model = Sequential()

model.add(LSTM(units = 50,input_dim = 4))
model.add(Dropout(0.2))

model.add(LSTM(100))
model.add(Dropout(0.2))

model.add(Dense(output_dim = 1))
model.add(Activation('relu'))

start = time.time()
model.compile(loss='mse', optimizer='rmsprop')

print('compile time', time.time()-start)

model.fit(X_train, y_train, batch_size=512, nb_epoch=1, validation_split=0.05)


predictions = lstm.predict_sequences_multiple(model,X_test,50,50)
lstm.plot_results_multile(predictions,y_test,50)
'''