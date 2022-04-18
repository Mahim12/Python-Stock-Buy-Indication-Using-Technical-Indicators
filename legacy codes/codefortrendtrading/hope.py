import pandas as pd
import pandas_datareader as web
import datetime
import csv
import talib as ta
import numpy as np
import mysql.connector
import time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="yahoodata"
)

mycursor = mydb.cursor()


def swingtrading():

	total_calls_a_day= 1
	while total_calls_a_day<6:	
		total_calls_a_day+=1


		start = datetime.datetime(2017, 9, 1)
		end = datetime.datetime.today()

	#List = ["SBIN.NS","PNB.NS","DABUR.NS","BOSCHLTD.NS","APOLLOTYRE.NS","ONGC.NS","NTPC.NS","POWERGRID.NS","ICICIPRULI.NS","PFC.NS","BAJAJHLDNG.NS","IBULHSGFIN.NS","MARUTI.NS","EXIDEIND.NS","HEROMOTOCO.NS","BAJAJ-AUTO.NS","EICHERMOT.NS","TVSMOTOR.NS","BHARATFORG.NS","KOTAKBANK.NS","ADANIPOWER.NS","ZEEL.NS","TATASTEEL.NS","YESBANK.NS","WIPRO.NS","UPL.NS","UNIONBANK.NS","VEDL.NS","HINDALCO.NS","TATAMOTORS.NS","TATAPOWER.NS","SAIL.NS","RBLBANK.NS","BANDHANBNK.NS","MOTHERSUMI.NS","NCC.NS","NBCC.NS","JSWSTEEL.NS","LT.NS","JINDALSTEL.NS","IDFC.NS","ITC.NS","INFRATEL.NS","IOC.NS","GLENMARK.NS","COALINDIA.NS","GMRINFRA.NS","HDFCBANK.NS","EDELWEISS.NS","ICICIGI.NS","GAIL.NS","FEDERALBNK.NS","BPCL.NS","ABCAPITAL.NS","ASHOKLEY.NS","AXISBANK.NS","IDFCFIRSTB.NS","INDUSINDBK.NS","ICICIBANK.NS","BANKINDIA.NS","BANKBARODA.NS","BEL.NS","BERGEPAINT.NS","BHEL.NS","BHARTIARTL.NS","BIOCON.NS","EQUITAS.NS","FCONSUMER.NS","INFIBEAM.NS","M&M.NS","INFY.NS","PEL.NS","AUROPHARMA.NS","DRREDDY.NS","DIVISLAB.NS","CIPLA.NS","LUPIN.NS","SUNPH# ARMA.NS","CADILAHC.NS","BAJAJFINSV.NS","M&MFIN.NS","BRITANNIA.NS","COLPAL.NS","GODREJCP.NS","TATACONSUM.NS","MARICO.NS","JUBLFOOD.NS","EMAMILTD.NS","GODREJIND.NS","UBL.NS","MCDOWELL-N.NS","TATAELXSI.NS","MINDTREE.NS","HEXAWARE.NS","HCLTECH.NS","TECHM.NS","NIITTECH.NS","TCS.NS","JUSTDIAL.NS","SAREGAMA.NS","INOXLEISUR.NS","PVR.NS","SUNTV.NS","HINDZINC.NS","HINDCOPPER.NS","RATNAMANI.NS","PRESTIGE.NS","OBEROIRLTY.NS","GODREJPROP.NS","SUNTECK.NS"]

		companylist = pd.read_csv('500companies.csv')
		companies = companylist['Symbol']


		
		for x in companies:
			company = '{fname}'.format(fname = x)
	 
			companyname = web.DataReader('{fname}'.format(fname = x), 'yahoo', start, end)
 
			companyname.to_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))

			technical_indicators = pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))

			open = technical_indicators['Open']
			high = technical_indicators['High']
			low = technical_indicators['Low']
			close = technical_indicators['Close']
			volume = technical_indicators['Volume']


	
			#calculating ema values using ta-lib
			ema_value_3 = ta.EMA(np.array(close),3)
			ema_value_5 = ta.EMA(np.array(close),5)
			ema_value_8 = ta.EMA(np.array(close),8)
			ema_value_13 = ta.EMA(np.array(close),13)
			ema_value_21 = ta.EMA(np.array(close),21)
			ema_value_34 = ta.EMA(np.array(close),34)

			#exporting ema values to csv file in a specified folder
			pd.DataFrame(ema_value_3).to_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_3.csv'.format(fname = x))
			pd.DataFrame(ema_value_5).to_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_5.csv'.format(fname = x))
			pd.DataFrame(ema_value_8).to_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_8.csv'.format(fname = x))
			pd.DataFrame(ema_value_13).to_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_13.csv'.format(fname = x))
			pd.DataFrame(ema_value_21).to_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_21.csv'.format(fname = x))
			pd.DataFrame(ema_value_34).to_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_34.csv'.format(fname = x))	



			retrieveEma_3 = pd.read_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_3.csv'.format(fname = x))
			retrieve_ema_value_3 = retrieveEma_3['0'].iloc[-1]

			retrieveEma_5 = pd.read_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_5.csv'.format(fname = x))
			retrieve_ema_value_5 = retrieveEma_5['0'].iloc[-1]

			retrieveEma_8 = pd.read_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_8.csv'.format(fname = x))
			retrieve_ema_value_8 = retrieveEma_8['0'].iloc[-1]
	
			retrieveEma_13 = pd.read_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_13.csv'.format(fname = x))
			retrieve_ema_value_13 = retrieveEma_13['0'].iloc[-1]

			retrieveEma_21 = pd.read_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_21.csv'.format(fname = x))
			retrieve_ema_value_21 = retrieveEma_21['0'].iloc[-1]

			retrieveEma_34 = pd.read_csv('companies/{fname}/swing trading/trend trading/{fname}_ema_value_34.csv'.format(fname = x))
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
			pd.DataFrame(adx_value).to_csv('companies/{fname}/swing trading/trend trading/{fname}_adx_value.csv'.format(fname = x))

			retrieveADX = pd.read_csv('companies/{fname}/swing trading/trend trading/{fname}_adx_value.csv'.format(fname = x))
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
			pd.DataFrame(rsi_value).to_csv('companies/{fname}/swing trading/trend trading/{fname}_rsi_value.csv'.format(fname = x))

			retrieveRSI = pd.read_csv('companies/{fname}/swing trading/trend trading/{fname}_rsi_value.csv'.format(fname = x))
			retrieve_rsi_value = retrieveRSI['0'].iloc[-1]

			rsivalue = str(retrieve_rsi_value)


			mycursor.execute("TRUNCATE TABLE `"+ '{fname}_swingtrading_technical_value'.format(fname = x) +"`")

			sql = "INSERT INTO `"+ '{fname}_swingtrading_technical_value'.format(fname = x) + "` (ticker, emacrossover, adxvalue, rsivalue) VALUES (%s, %s, %s, %s)"
			val = (company, emavalue, adxvalue, rsivalue)
			mycursor.execute(sql, val)

			mydb.commit()
			print(company)

		time.sleep(3600)

if __name__ == '__main__':
	swingtrading()
		
    
	
	

 









