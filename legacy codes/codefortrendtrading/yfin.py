import yfinance as yf
import time
import pandas as pd
import datetime
import talib as ta
import numpy as np
import csv
import time
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="yahoodata"
)

mycursor = mydb.cursor()


total_calls_a_day= 1
while total_calls_a_day<50:
	total_calls_a_day+=1

	
	# List = ["SBIN.NS"]

	companylist = pd.read_csv('500companies.csv')
	companies = companylist['Symbol']
		
	for x in companies:
		company = '{fname}'.format(fname = x)

		data = yf.download(tickers=x,period="5d",interval="1m")
		data.to_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}.csv'.format(fname = x))

		technical_indicators_intraday = pd.read_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}.csv'.format(fname = x))

		open = technical_indicators_intraday['Open']
		high = technical_indicators_intraday['High']
		low = technical_indicators_intraday['Low']
		close = technical_indicators_intraday['Close']
		volume = technical_indicators_intraday['Volume']


		#calculating ema values using ta-lib
		ema_value_3 = ta.EMA(np.array(close),3)
		ema_value_5 = ta.EMA(np.array(close),5)
		ema_value_8 = ta.EMA(np.array(close),8)
		ema_value_13 = ta.EMA(np.array(close),13)
		ema_value_21 = ta.EMA(np.array(close),21)
		ema_value_34 = ta.EMA(np.array(close),34)

		#exporting ema values to csv file in a specified folder
		pd.DataFrame(ema_value_3).to_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_3.csv'.format(fname = x))
		pd.DataFrame(ema_value_5).to_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_5.csv'.format(fname = x))
		pd.DataFrame(ema_value_8).to_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_8.csv'.format(fname = x))
		pd.DataFrame(ema_value_13).to_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_13.csv'.format(fname = x))
		pd.DataFrame(ema_value_21).to_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_21.csv'.format(fname = x))
		pd.DataFrame(ema_value_34).to_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_34.csv'.format(fname = x))	



		retrieveEma_3 = pd.read_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_3.csv'.format(fname = x))
		retrieve_ema_value_3 = retrieveEma_3['0'].iloc[-1]

		retrieveEma_5 = pd.read_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_5.csv'.format(fname = x))
		retrieve_ema_value_5 = retrieveEma_5['0'].iloc[-1]

		retrieveEma_8 = pd.read_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_8.csv'.format(fname = x))
		retrieve_ema_value_8 = retrieveEma_8['0'].iloc[-1]
	
		retrieveEma_13 = pd.read_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_13.csv'.format(fname = x))
		retrieve_ema_value_13 = retrieveEma_13['0'].iloc[-1]

		retrieveEma_21 = pd.read_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_21.csv'.format(fname = x))
		retrieve_ema_value_21 = retrieveEma_21['0'].iloc[-1]

		retrieveEma_34 = pd.read_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_ema_value_34.csv'.format(fname = x))
		retrieve_ema_value_34 = retrieveEma_34['0'].iloc[-1]

		if retrieve_ema_value_3 > retrieve_ema_value_5 and retrieve_ema_value_3 > retrieve_ema_value_8 and retrieve_ema_value_3 > retrieve_ema_value_13 and retrieve_ema_value_3 > retrieve_ema_value_21 and retrieve_ema_value_3 > retrieve_ema_value_34 and retrieve_ema_value_5 > retrieve_ema_value_8 and retrieve_ema_value_5 > retrieve_ema_value_13 and retrieve_ema_value_5 > retrieve_ema_value_21 and retrieve_ema_value_5 > retrieve_ema_value_34 and retrieve_ema_value_8 > retrieve_ema_value_13 and retrieve_ema_value_8 > retrieve_ema_value_21 and retrieve_ema_value_8 > retrieve_ema_value_34 and retrieve_ema_value_13 > retrieve_ema_value_21 and retrieve_ema_value_13 > retrieve_ema_value_34 and retrieve_ema_value_21 > retrieve_ema_value_34:	
			emavalue = "buy"
		elif retrieve_ema_value_3 < retrieve_ema_value_5 and retrieve_ema_value_3 < retrieve_ema_value_8 and retrieve_ema_value_3 < retrieve_ema_value_13 and retrieve_ema_value_3 < retrieve_ema_value_21 and retrieve_ema_value_3 < retrieve_ema_value_34 and retrieve_ema_value_5 < retrieve_ema_value_8 and retrieve_ema_value_5 < retrieve_ema_value_13 and retrieve_ema_value_5 < retrieve_ema_value_21 and retrieve_ema_value_5 < retrieve_ema_value_34 and retrieve_ema_value_8 < retrieve_ema_value_13 and retrieve_ema_value_8 < retrieve_ema_value_21 and retrieve_ema_value_8 < retrieve_ema_value_34 and retrieve_ema_value_13 < retrieve_ema_value_21 and retrieve_ema_value_13 < retrieve_ema_value_34 and retrieve_ema_value_21 < retrieve_ema_value_34:	
			emavalue = "sell"
		else:
			emavalue = "wait for the signal"


		#calculating adx values using ta-lib
		adx_value = np.array(ta.ADX(high,low,close,14))
	
		#exporting adx values to csv file in a specified folder
		pd.DataFrame(adx_value).to_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_adx_value.csv'.format(fname = x))

		retrieveADX = pd.read_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_adx_value.csv'.format(fname = x))
		retrieve_adx_value = retrieveADX['0'].iloc[-1]


		if retrieve_adx_value > 0 and retrieve_adx_value < 25:
			adxvalue = "Weak Trend"

		if retrieve_adx_value > 25 and retrieve_adx_value < 50:
			adxvalue = "Strong Trend"

		if retrieve_adx_value > 50 and retrieve_adx_value < 75:
			adxvalue = "Very strong Trend"

		if retrieve_adx_value > 75 and retrieve_adx_value < 100:
			adxvalue = "Extremely strong Trend"



	
		#calculating rsi values using ta-lib
		rsi_value = np.array(ta.RSI(close,14))

		#exporting rsi values to csv file in a specified folder
		pd.DataFrame(rsi_value).to_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_rsi_value.csv'.format(fname = x))

		retrieveRSI = pd.read_csv('companies/{fname}/intraday trading/trend trading yfinance module/{fname}_rsi_value.csv'.format(fname = x))
		retrieve_rsi_value = retrieveRSI['0'].iloc[-1]

		rsivalue = str(retrieve_rsi_value)

		mycursor.execute("TRUNCATE TABLE `"+ '{fname}_intraday_yfinance_module_technical_value'.format(fname = x) +"`")

		sql = "INSERT INTO `"+ '{fname}_intraday_yfinance_module_technical_value'.format(fname = x) + "` (ticker, emacrossover, adxvalue, rsivalue) VALUES (%s, %s, %s, %s)"
		val = (company, emavalue, adxvalue, rsivalue)
		mycursor.execute(sql, val)

		mydb.commit()
		
		data1 = data.tail(1)
		print(data1)
		
	time.sleep(300)
