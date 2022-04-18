from multiprocessing import Process
import sys
import bs4
import requests
from bs4 import BeautifulSoup
import csv
from scipy import stats
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime
import mysql.connector
import time
import talib as ta
import numpy as np
import math
from scipy.stats import pearsonr
import os
from pandas.io import sql
import sqlalchemy
import yfinance as yf
import statistics 
import itertools


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="hybridtactics"
)

mycursor = mydb.cursor()


def Diff(firstextraction, passedon):
    return (list(list(set(firstextraction)-set(passedon)) + list(set(passedon)-set(firstextraction))))


#For sorting a list.
def sortSecond(val): 
    return val[1] 

# For calculating the closest value from a list compared to K. For percentile
def closest(list, K):      
    return list[min(range(len(list)), key = lambda i: abs(list[i]-K))] 

val = 40
#to identify oversold conditions. The function below checks whether any of the last 10 rsi value is less than 40
def CheckForLess(retrieve_rsi_list, val):  
	for x in retrieve_rsi_list:
		if x <= val:  
			return True
	return False

upVal = 68
#to identify overbought conditions. The function below checks whether any of the last 10 rsi value is greater than 65
def CheckForMore(retrieve_rsi_list, upVal):  
	for x in retrieve_rsi_list:
		if x >= upVal:  
			return True
	return False

Volumeval = 5    
#to identify if any of the last 5 intraday volume values is less than 5.
def CheckForLessVolume(intradayVolumelist, Volumeval):  
	for x in intradayVolumelist:
		if x >= Volumeval:  
			return True
	return False



sloperange = 30 #HOW MANY DAYS SWING SLOPE DO YOU WANT TO CALCULATE?
percentiledays = 10 #how many days percentile, mean, median, max do you want to calculate?


#companylist = pd.read_csv('NIFTY50.csv')
companylist = pd.read_csv('mainCompanylist.csv')
companies = companylist['Symbol']


def ParsePrice():
	passedon = []

	database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('root', '', 'localhost', 'hybridtactics'))

	total_calls_a_day= 1
	while total_calls_a_day<250:
		total_calls_a_day+=1
		my_list = []
		
		for x in range(0, 2):
		
			company = 'https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php'
			r=requests.get(company)
			soup=bs4.BeautifulSoup(r.text,"lxml")
			for price in soup.find_all('span', attrs={'class':'gld13'}):
				head, sep, tail = price.text.partition('Add')
				my_list.append(head)
		
			
			firstextraction = [v for i, v in enumerate(my_list) if i % 2 != 0] #removes all the odd indexed strings from the list because there were two values of same company being extracted.
			#print("First is", firstextraction)
			list_difference = [item for item in firstextraction if item not in passedon]
			print("Difference is", Diff(firstextraction, passedon))

			moneyControlObj = pd.DataFrame(Diff(firstextraction, passedon), columns = ['Company']) 
			moneyControlObj.to_sql(con=database_connection, name='moneycontrol', if_exists='replace')
			
			passedon = firstextraction
	
			time.sleep(120)


		firstextraction.clear() 
		passedon.clear()	
		time.sleep(480)
			



mycursor.execute("SELECT Company FROM `swingtrend`")
table_rows = mycursor.fetchall()
		
def intraday():
	total_calls_a_day= 1
	database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('root', '', 'localhost', 'hybridtactics'))

	while total_calls_a_day<75:	
		total_calls_a_day+=1

		slopelist = list()
		slopeuplist = list()
		sloperangelist = list()
		companylistforbbsqueeze	= list()

		intraday_list = []
		rangestrategylist = []	
		bollingerlist = []
		bollingermidlist = []
		bollingerIntradaylist = []

		
		mycursor.execute("SELECT Company FROM `swingtrend`")
		table_rows = mycursor.fetchall()
		

		for [z] in table_rows:	
			intraday_list.append(z)

		for c in intraday_list:

			company = '{fname}'.format(fname = c)
			emaFiveListForMode = []
			emaEightListForMode = []
			emathirteenListForMode = []
				

			# GET INTRADAY DATA
			data = yf.download(tickers=c,period="1d",interval="1m")
			data.to_csv('companies/{fname}/intraday trading/{fname}_intraday.csv'.format(fname = c))
			company = '{fname}'.format(fname = c)

			technical_indicators_intraday = pd.read_csv('companies/{fname}/intraday trading/{fname}_intraday.csv'.format(fname = c))

			open = technical_indicators_intraday['Open']
			high = technical_indicators_intraday['High']
			low = technical_indicators_intraday['Low']
			close = technical_indicators_intraday['Close']
			intradayAvgVolume = technical_indicators_intraday['Volume'].head(-1).tail(5).mean()
			intradayVolumelist = technical_indicators_intraday['Volume'].head(-1).tail(5).tolist()
			#print(company, intradayVolumelist)
			
			lastFiveValueList = technical_indicators_intraday['Close'].tail(5).tolist()

			bblastfivevalue = technical_indicators_intraday['Close'].head(-1).tail(5).mean()
			BBPercentileClose = technical_indicators_intraday['Close'].iloc[-1]
			BBPercentileClose = float(BBPercentileClose)

		
			x = technical_indicators_intraday['Close'].tail(sloperange).tolist()
			v = technical_indicators_intraday['Volume'].tail(sloperange).tolist()

		
		
			lastprice = technical_indicators_intraday['Close'].iloc[-1]
			lastprice = float(lastprice)

			xForRange = technical_indicators_intraday['Close'].tail(10).tolist()
			yForRange = range(len(xForRange))


			y = range(len(x))

			best_fit_line = np.poly1d(np.polyfit(y, x, 1))(y)

			#slope = (y[-1] - y[0]) / (x[-1] - x[0])
			angle = np.rad2deg(np.arctan2(y[-1] - y[0], x[-1] - x[0]))
			angle = float(angle)


			slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
			slope = float(slope)
			slopeV, interceptV, r_valueV, p_valueV, std_errV = stats.linregress(v,y)

			slopeT, intercept, r_value, p_value, std_err = stats.linregress(xForRange,yForRange)


			swingupper, swingmiddle, swinglower = np.array(ta.BBANDS(close, 20, 2, 2, 0))

			pd.DataFrame(swingupper).to_csv('companies/{fname}/intraday trading/{fname}_upperband.csv'.format(fname = c))
			pd.DataFrame(swingmiddle).to_csv('companies/{fname}/intraday trading/{fname}_middleband.csv'.format(fname = c))
			pd.DataFrame(swinglower).to_csv('companies/{fname}/intraday trading/{fname}_lowerband.csv'.format(fname = c))


			upperband = pd.read_csv('companies/{fname}/intraday trading/{fname}_upperband.csv'.format(fname = c))
			upperbandvalue = upperband['0'].tail(5)
			upperbandvalue = upperbandvalue.mean()

			middleband = pd.read_csv('companies/{fname}/intraday trading/{fname}_middleband.csv'.format(fname = c))
			middlebandlastvalue = middleband['0'].iloc[-1]
			middlebandvalue = middleband['0'].head(-1).tail(5)
			middlebandvalue = middlebandvalue.mean()
			

			lowerband = pd.read_csv('companies/{fname}/intraday trading/{fname}_lowerband.csv'.format(fname = c))
			lowerbandvalue = lowerband['0'].tail(5)
			lowerbandvalue = lowerbandvalue.mean()


			#calculating rsi values using ta-lib
			rsi_value = np.array(ta.RSI(close,14))

			#exporting rsi values to csv file in a specified folder
			pd.DataFrame(rsi_value).to_csv('companies/{fname}/intraday trading/{fname}_rsi_value.csv'.format(fname = c))

			retrieveRSI = pd.read_csv('companies/{fname}/intraday trading/{fname}_rsi_value.csv'.format(fname = c))
			
			retrieve_rsi_list = retrieveRSI['0'].tail(20).tolist()
			
			xForRSI = retrieveRSI['0'].tail(10).tolist()
			yForRSI = range(len(xForRSI))
			slopeRSI, intercept, r_value, p_value, std_err = stats.linregress(xForRSI,yForRSI)


			retrieve_rsi_value = retrieveRSI['0'].iloc[-1]
			retrieve_rsi_value = float(retrieve_rsi_value)

			rsiForRangeBreakout = retrieveRSI['0'].head(-10).tail(10).mean()
			rsiForRangeBreakout = float(rsiForRangeBreakout)
			
		
			#calculating ADX values using ta-lib
			adx_value = np.array(ta.ADX(high,low,close,14)) 

			pd.DataFrame(adx_value).to_csv("companies/{fname}/intraday trading/{fname}_adxvalue.csv".format(fname=c))

			retrieveadx = pd.read_csv("companies/{fname}/intraday trading/{fname}_adxvalue.csv".format(fname=c))
			retrievedAdxvalue = retrieveadx['0'].iloc[-1]
			retrievedAdxvalue = float(retrievedAdxvalue)

			adxForRangeBreakout = retrieveadx['0'].head(-10).tail(10).mean()
			adxForRangeBreakout = float(adxForRangeBreakout)

			retrieve_adx_list = retrieveadx['0'].tail(10).tolist()
			
			xForADX = retrieveadx['0'].tail(10).tolist()
			yForADX = range(len(xForADX))
			slopeADX, interceptADX, r_valueADX, p_valueADX, std_errADX = stats.linregress(xForADX,yForADX)

			#calculating ema values using ta-lib
			
			ema_value_5 = ta.EMA(np.array(close),5)
			ema_value_8 = ta.EMA(np.array(close),8)
			ema_value_13 = ta.EMA(np.array(close),13)
			

			#exporting ema values to csv file in a specified folder
			
			pd.DataFrame(ema_value_5).to_csv('companies/{fname}/intraday trading/{fname}_ema_value_5.csv'.format(fname = c))
			pd.DataFrame(ema_value_8).to_csv('companies/{fname}/intraday trading/{fname}_ema_value_8.csv'.format(fname = c))
			pd.DataFrame(ema_value_13).to_csv('companies/{fname}/intraday trading/{fname}_ema_value_13.csv'.format(fname = c))
			

			retrieveEma_5 = pd.read_csv('companies/{fname}/intraday trading/{fname}_ema_value_5.csv'.format(fname = c))
			retrieveEma_8 = pd.read_csv('companies/{fname}/intraday trading/{fname}_ema_value_8.csv'.format(fname = c))
			retrieveEma_13 = pd.read_csv('companies/{fname}/intraday trading/{fname}_ema_value_13.csv'.format(fname = c))	

			for i in range(1,6):
				retrieve_ema_value_5 = retrieveEma_5['0'].iloc[-i]
				emaFiveListForMode.append(retrieve_ema_value_5)
				#print(emaFiveListForMode)

		
				retrieve_ema_value_8 = retrieveEma_8['0'].iloc[-i]
				emaEightListForMode.append(retrieve_ema_value_8)


		
				retrieve_ema_value_13 = retrieveEma_13['0'].iloc[-i]
				emathirteenListForMode.append(retrieve_ema_value_13)



			mainEmaModeList = []


			for (a, b, c) in zip(emaFiveListForMode, emaEightListForMode, emathirteenListForMode):
				if a > b and a > c and b > c:	
					emaValue = "Upward Crossover"
				elif a < b and a < c and b < c:	
					emaValue = "Downward Crossover"
				else:
					emaValue = "Check yourself"
			
				mainEmaModeList.append(emaValue)


			val = 40 
			Volumeval = 5

			flag = 0
			flagVolume = 0
			flag = len(set(lastFiveValueList)) == len(lastFiveValueList) 
			flagVolume = len(set(intradayVolumelist)) == len(intradayVolumelist)
 
			if(flag): #this line of code checks whether there is the same closing price in the list which i want to remove. 
				if(flagVolume): #this line of code checks whether there is the same volume in the list which i want to remove. The assumption is it won't be unless the value of volume is 0.
					
					if slope<0: #mid-cross over strategy
						if slopeT>0:
							if statistics.mode(mainEmaModeList) == "Upward Crossover":
								if slopeRSI>0:
									if (CheckForLess(retrieve_rsi_list, val)):#If any of the last 10 rsi values is less than 40 to identify oversold conditions. 
										if(BBPercentileClose>middlebandlastvalue) and BBPercentileClose<6000:
											if intradayAvgVolume>850:
												if (CheckForLessVolume(intradayVolumelist, Volumeval)):
													slopetrendstrategy = (company,slopeRSI,angle,lastprice,statistics.mode(mainEmaModeList),retrievedAdxvalue)
													slopelist.append(slopetrendstrategy)
													slopelist.sort(key = sortSecond, reverse = False)
					
					if slopeRSI>0: #range breakout
						if slopeADX>0: 
							if slopeT>0:#is price increasing. This can be removed for swing breakout strategy.
								if(rsiForRangeBreakout>=40 and rsiForRangeBreakout<=60): #ignore recent ten values because 10 min for intraday data collection.
									if(adxForRangeBreakout<=25):
										if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)>0.5): #The bollinger band just opened up.
											if BBPercentileClose<6000:
												if intradayAvgVolume>850:
													if (CheckForLessVolume(intradayVolumelist, Volumeval)):
														if company not in [i[0] for i in slopelist]: 
															
															toappendinbollingersqueeze = (company,slopeRSI,BBPercentileClose)
															bollingerlist.append(toappendinbollingersqueeze)
															bollingerlist.sort(key = sortSecond, reverse = False)

					upVal = 68
					if slopeT>0:#is price increasing
						if slopeADX>0: 
							if statistics.mode(mainEmaModeList) == "Upward Crossover":
								if slopeRSI>0: #is rsi also increasing
									if (CheckForMore(retrieve_rsi_list, upVal)):
										if intradayAvgVolume>850:
											if BBPercentileClose<6000: 
												if (CheckForLessVolume(intradayVolumelist, Volumeval)):
													if company not in [i[0] for i in bollingerlist]:
														slopeuptrendstrategy = (company,slopeRSI,angle,lastprice,statistics.mode(mainEmaModeList),retrievedAdxvalue)
														slopeuplist.append(slopeuptrendstrategy)
														slopeuplist.sort(key = sortSecond, reverse = False)
			

					
					'''
					if(retrieve_rsi_value>=40 and retrieve_rsi_value<=60):
						if(retrievedAdxvalue<=25): 
							if(bblastfivevalue<middlebandvalue):
								if BBPercentileClose<6000: 
									if intradayAvgVolume>1000:
										if (CheckForLessVolume(intradayVolumelist, Volumeval)):
											if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)>0.5):
												if  (abs(BBPercentileClose-middlebandvalue)/((BBPercentileClose+middlebandvalue)/2)*100)<0.3: #current price should be lower than middle band for buying because i don't short a stock.
													BollingerSqueeze = (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)
													BollingerSqueeze = float(BollingerSqueeze)
													toappendonrangestrategy = (company,BollingerSqueeze,BBPercentileClose,retrieve_rsi_value,retrievedAdxvalue,statistics.mode(mainEmaModeList))
													rangestrategylist.append(toappendonrangestrategy)
													rangestrategylist.sort(key = sortSecond, reverse = True) #true because the greater the range the better the mean reversion oppurtunity.
					'''
	
			mainEmaModeList.clear()

		pd.set_option('display.max_rows', None)
		print('-------------------------------------------------------Oversold-Crossover STRATEGY-------------------------------------------------------')
		swingObj = pd.DataFrame(slopelist, columns = ['Company','RsiSlope','Angle','Price','EMA','ADX']) 
		swingObj.to_sql(con=database_connection, name='swingintradaytrend', if_exists='replace')
		print(swingObj)
			
		print('-------------------------------------------------------UpTrend STRATEGY-------------------------------------------------------')
		swingupObj = pd.DataFrame(slopeuplist, columns = ['Company','RsiSlope','Angle','Price','EMA','ADX']) 
		swingupObj.to_sql(con=database_connection, name='upswingintradaytrend', if_exists='replace')
		print(swingupObj)

		print('-------------------------------------------------------BBSQUEEZE STRATEGY-------------------------------------------------------')		
		IntradayBollingerSqueezeObj = pd.DataFrame(bollingerlist, columns = ['Company','RsiSlope','Close']) 
		IntradayBollingerSqueezeObj.to_sql(con=database_connection, name='intradaybbsqueeze', if_exists='replace') 
		print(IntradayBollingerSqueezeObj)
		
		'''
		print('-------------------------------------------------------RANGE TRADING(RSI AND ADX) MEAN REVERSION STRATEGY-------------------------------------------------------')
		RangeObj = pd.DataFrame(rangestrategylist, columns = ['Company','Squeeze','Price','avgrsi','avgadx','EMA']) 
		RangeObj.to_sql(con=database_connection, name='rangeintradaytrading', if_exists='replace')
		print(RangeObj)
		'''	

		time.sleep(600)


if __name__=='__main__':
    p1 = Process(target=ParsePrice)
    p1.start()
    p2 = Process(target=intraday)
    p2.start()

