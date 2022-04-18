import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import Error


api_key = 'V7HJCNIV37CXYXXI'

ts = TimeSeries(key=api_key, output_format='pandas')
data_ts, meta_data_ts = ts.get_intraday(symbol='NSE:HDFCBANK', interval='1min', outputsize='full')

period1 = 50
period2 = 200

ti = TechIndicators(key=api_key, output_format = 'pandas')

data_ti, meta_data_ti = ti.get_ema(symbol='NSE:HDFCBANK', interval='1min',
					time_period=period1, series_type='close')

data_ti2, meta_data_ti2 = ti.get_ema(symbol='NSE:HDFCBANK', interval='1min',
					time_period=period2, series_type='close')

df1 = data_ti.tail(1)
df2 = data_ti2.tail(1)




mydb = mysql.connector.connect(

  host="localhost",
  user="root",
  passwd="123stories",
  database="alphavantageclose",
  port=3306
)

mycursor = mydb.cursor()

sql = "INSERT INTO alphavantageclose (Price) VALUES (%s)"
val = (df1)

mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")


total = pd.concat([df1, df2], axis=1)

print(total)
