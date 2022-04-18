from scipy import stats
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime
import yfinance as yf
import mysql.connector
import time
import talib as ta
import numpy as np
import math
from scipy.stats import pearsonr
import pandas_datareader as web
import os
from pandas.io import sql
import sqlalchemy
import sys
import bs4
import requests
from bs4 import BeautifulSoup
import csv
import yfinance as yf
import statistics 
import itertools
import winsound

#For sorting a list.
def sortSecond(val): 
    return val[1] 

def calculateGeneralSlopeTrend(days, company, Parameter): #Parameter is the Close, Open, High, Low, Volume here
	df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname=company))
	x = df[Parameter].tail(days).tolist()
	y = range(len(x))
	best_fit_line = np.poly1d(np.polyfit(y, x, 1))(y)
	angle = np.rad2deg(np.arctan2(y[-1] - y[0], x[-1] - x[0]))
	angle = float(angle)
	slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
	slope = float(slope)

	return slope,angle,best_fit_line


def bollingerBandsCalculations(LastNDaysForCalc, company, Parameter, ilocValue): # statParameter is the mean, median, mode
	df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname=company))
	value = df[Parameter]

	swingupper, swingmiddle, swinglower = np.array(
            ta.BBANDS(value, 20, 2, 2, 0))

	pd.DataFrame(swingupper).to_csv('newcompanylist/{fname}/swing trading/{fname}_upperband.csv'.format(fname=company))
	pd.DataFrame(swingmiddle).to_csv('newcompanylist/{fname}/swing trading/{fname}_middleband.csv'.format(fname=company))
	pd.DataFrame(swinglower).to_csv('newcompanylist/{fname}/swing trading/{fname}_lowerband.csv'.format(fname=company))

	upperband = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_upperband.csv'.format(fname=company))
	upperbandvalue = upperband['0'].tail(LastNDaysForCalc)
	upperbandvalue = upperbandvalue.mean()

	upperbandlastvalue = upperband['0'].iloc[-ilocValue]

	middleband = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_middleband.csv'.format(fname=company))
	middlebandvalue = middleband['0'].tail(LastNDaysForCalc)
	middlebandvalue = middlebandvalue.mean()

	middlebandlastvalue = middleband['0'].iloc[-ilocValue]
	
	lowerband = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_lowerband.csv'.format(fname=company))
	lowerbandvalue = lowerband['0'].tail(LastNDaysForCalc)
	lowerbandvalue = lowerbandvalue.mean()

	lowerbandlastvalue = lowerband['0'].iloc[-ilocValue]

	return upperbandvalue,middlebandvalue,middlebandlastvalue,lowerbandvalue,upperbandlastvalue,lowerbandlastvalue


def rsiCalculations(days, company, daysforslope, Parameter, ilocValue):
	df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname=company))
	value = df[Parameter]

        # calculating rsi values using ta-lib
	rsi_value = np.array(ta.RSI(value, days))
	pd.DataFrame(rsi_value).to_csv('newcompanylist/{fname}/swing trading/{fname}_rsi_value.csv'.format(fname=company))

	retrieveRSI = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_rsi_value.csv'.format(fname=company))
	retrieve_rsi_value = retrieveRSI['0'].iloc[-ilocValue]
	retrieve_rsi_value = float(retrieve_rsi_value)

	xForRSI = retrieveRSI['0'].tail(daysforslope).tolist()
	yForRSI = range(len(xForRSI))
	best_fit_line = np.poly1d(np.polyfit(yForRSI, xForRSI, 1))(yForRSI)
	angle = np.rad2deg(np.arctan2(yForRSI[-1] - yForRSI[0], xForRSI[-1] - xForRSI[0]))
	angle = float(angle)
	slopeRSI, intercept, r_value, p_value, std_err = stats.linregress(xForRSI, yForRSI)

	return retrieve_rsi_value,slopeRSI,angle,best_fit_line


def adxCalculations(days, company, daysforslope, ilocValue):
	df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname=company))
	open = df['Open']
	high = df['High']
	low = df['Low']  
	close = df['Close']
	adx_value = np.array(ta.ADX(high, low, close, 14))

	pd.DataFrame(adx_value).to_csv("newcompanylist/{fname}/swing trading/{fname}_adxvalue.csv".format(fname=company))

	retrieveadx = pd.read_csv("newcompanylist/{fname}/swing trading/{fname}_adxvalue.csv".format(fname=company))
	retrievedAdxvalue = retrieveadx['0'].iloc[-ilocValue]
	retrievedAdxvalue = float(retrievedAdxvalue)

	xForADX = retrieveadx['0'].tail(daysforslope).tolist()
	yForADX = range(len(xForADX))
	best_fit_line = np.poly1d(np.polyfit(yForADX, xForADX, 1))(yForADX)
	angle = np.rad2deg(np.arctan2(yForADX[-1] - yForADX[0], xForADX[-1] - xForADX[0]))
	angle = float(angle)
	slopeADX, interceptADX, r_valueADX, p_valueADX, std_errADX = stats.linregress(xForADX, yForADX)

	adxForRangeBreakout = retrieveadx['0'].head(-10).tail(10).mean()
	adxForRangeBreakout = float(adxForRangeBreakout)

	return retrievedAdxvalue,slopeADX,angle,best_fit_line


def emaCalculations(company, Parameter):

	emaOneListForMode = []
	emaThreeListForMode = []
	emaFiveListForMode = []
	emaEightListForMode = []
	emathirteenListForMode = []

	df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname=company))
	value = df[Parameter]

	#calculating ema values using ta-lib

	ema_value_3 = np.array(ta.EMA(value,3)) 
	ema_value_5 = np.array(ta.EMA(value,5))
	ema_value_8 = np.array(ta.EMA(value,8))
	ema_value_13 = np.array(ta.EMA(value,13))
			
	#exporting ema values to csv file in a specified folder

	pd.DataFrame(ema_value_3).to_csv('newcompanylist/{fname}/intraday trading/{fname}_ema_value_3.csv'.format(fname=company))	
	pd.DataFrame(ema_value_5).to_csv('newcompanylist/{fname}/intraday trading/{fname}_ema_value_5.csv'.format(fname=company))
	pd.DataFrame(ema_value_8).to_csv('newcompanylist/{fname}/intraday trading/{fname}_ema_value_8.csv'.format(fname=company))
	pd.DataFrame(ema_value_13).to_csv('newcompanylist/{fname}/intraday trading/{fname}_ema_value_13.csv'.format(fname=company))
			

	retrieveEma_3 = pd.read_csv('newcompanylist/{fname}/intraday trading/{fname}_ema_value_3.csv'.format(fname=company))
	retrieveEma_5 = pd.read_csv('newcompanylist/{fname}/intraday trading/{fname}_ema_value_5.csv'.format(fname=company))
	retrieveEma_8 = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_8.csv'.format(fname=company))
	retrieveEma_13 = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_13.csv'.format(fname=company))

	for i in range(1,6):

		retrieve_ema_value_3 = retrieveEma_3['0'].iloc[-i]
		emaThreeListForMode.append(retrieve_ema_value_3)

		retrieve_ema_value_5 = retrieveEma_5['0'].iloc[-i]
		emaFiveListForMode.append(retrieve_ema_value_5)
		
		retrieve_ema_value_8 = retrieveEma_8['0'].iloc[-i]
		emaEightListForMode.append(retrieve_ema_value_8)

		retrieve_ema_value_13 = retrieveEma_13['0'].iloc[-i]
		emathirteenListForMode.append(retrieve_ema_value_13)

	EmaModeListForAdxRsiMeanReversion = []
	EmaModeListForbollingermidlistMeanReversion = []

	for (a, b, c) in zip(emaFiveListForMode, emaEightListForMode, emathirteenListForMode):
		if a > b and a > c and b > c:	
			emaValue = "Upward Crossover"
		elif a < b and a < c and b < c:	
			emaValue = "Downward Crossover"
		else:
			emaValue = "Check yourself"
			
		EmaModeListForAdxRsiMeanReversion.append(emaValue)

	for (a, b) in zip(emaThreeListForMode, emaFiveListForMode):
		if a > b:	
			emaValue = "Upward Crossover"
		elif a < b:	
			emaValue = "Downward Crossover"
		else:
			emaValue = "Check yourself"
			
		EmaModeListForbollingermidlistMeanReversion.append(emaValue)


	return EmaModeListForAdxRsiMeanReversion,EmaModeListForbollingermidlistMeanReversion,ema_value_3,ema_value_5,ema_value_8,ema_value_13


def HA(company,ilocValue):
	df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname=company))

	df_HA = df
	df_HA['Close']=(df['Open']+ df['High']+ df['Low']+df['Close'])/4

	for i in range(0, len(df)):
		if i == 0:
			df_HA['Open'][i]= ( (df['Open'][i] + df['Close'][i] )/ 2)
		else:
			df_HA['Open'][i] = ( (df['Open'][i-1] + df['Close'][i-1] )/ 2)

	df_HA['High']=df[['Open','Close','High']].max(axis=1)
	df_HA['Low']=df[['Open','Close','Low']].min(axis=1)

	newdf = pd.DataFrame({'Date':df['Date'], 'Open': df_HA['Open'],'High': df_HA['High'],'Low': df_HA['Low'],'Close': df_HA['Close']})

	pd.set_option('display.max_rows', None)
	newdf = pd.DataFrame(newdf,columns=['Date','Open','High','Low','Close'])
	newdf.to_csv('newcompanylist/{fname}/swing trading/{fname}_heikenashi.csv'.format(fname=company), index=False) 

	retreiveHeikenAshiClose = df_HA['Close'].iloc[-ilocValue]
	retreiveHeikenAshiOpen = df_HA['Open'].iloc[-ilocValue]

	return retreiveHeikenAshiClose,retreiveHeikenAshiOpen 
	#return df_HA



def lastNValues(daysforaverage, company, Parameter, ilocValue):
	df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname=company))
	lastvalue = df[Parameter].iloc[-ilocValue]
	lastvolume = df[Parameter].iloc[-ilocValue]

	avgOfLastNdays = df[Parameter].tail(daysforaverage).mean() #to calculate mean of the last n number of days
	return lastvalue,avgOfLastNdays,lastvolume 

def absolutePercentDiffBetweenTwoNumbers(x,y):
	ans = ((abs(x-y))/((x+y)/2)*100)
	return ans

def percentIncreaseOrDecrease(originalNum,newNum):
	diff = newNum - originalNum
	percentdiff = (diff/originalNum)*100
	return percentdiff 
	

def allValues(company, daysforlist):
	df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname=company))

	open = df['Open']
	high = df['High']
	low = df['Low']
	close = df['Close']

	openList = df['Open'].tail(daysforlist).tolist()
	highList = df['High'].tail(daysforlist).tolist()
	lowList = df['Low'].tail(daysforlist).tolist()
	closeList = df['Close'].tail(daysforlist).tolist()
	
	return open,high,low,close,openList,highList,lowList,closeList


def removeImages(folder):
	folder_path = ((folder))
	test = os.listdir(folder_path)

	for images in test:
		if images.endswith(".png"):
			os.remove(os.path.join(folder_path, images))



def ParsePrice():
	my_list = []
		
	company = 'https://www.moneycontrol.com/stocks/marketstats/nseloser/index.php'
	r=requests.get(company)
	soup=bs4.BeautifulSoup(r.text,"lxml")
	for price in soup.find_all('span', attrs={'class':'gld13'}):
		head, sep, tail = price.text.partition('Add')
		my_list.append(head)
		
			
	firstextraction = [v for i, v in enumerate(my_list) if i % 2 != 0] #removes all the odd indexed strings from the list because there were two values of same company being extracted.
	print("First is", firstextraction)
			




companylist = pd.read_csv('mainCompanylist.csv')
companies = companylist['Symbol']

def collectData():
	list = []
	total_calls_a_day= 1
	while total_calls_a_day<2:	
		total_calls_a_day+=1
	
		start = datetime.datetime(2010, 1, 1)
		end = datetime.datetime.today()

		niftyprice = web.DataReader('^NSEI', 'yahoo', start, end) 
		niftyprice.to_csv('newcompanylist/nifty.csv')

		dowJonesprice = web.DataReader('^DJI', 'yahoo', start, end) 
		dowJonesprice.to_csv('newcompanylist/dowjones.csv')


		niftyIntrday = yf.download(tickers='^NSEI',period="1d",interval="1m")
		niftyIntrday.to_csv('newcompanylist/NSEI_intraday.csv')

		for x in companies:
			company = '{fname}'.format(fname = x)
			companyname = web.DataReader('{fname}'.format(fname = x), 'yahoo', start, end)
			companyname.to_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = x))

			print(company)



def gapTrading():
	gaplowlist = list()
	gapuplist = list()

	database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('root', '', 'localhost', 'hybridtactics'))

	for c in companies:
		
		company = '{fname}'.format(fname = c)

		df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = c))
	
		gapOpen = df['Open'].iloc[-1]
		gapHigh = df['High']
		gapLow = df['Low']
		gapClose = df['Close'].iloc[-2]
	
		if gapOpen<5000:
			if company in intradayallowed:
				if((abs(gapOpen-gapClose)/((gapOpen+gapClose)/2)*100)>1):
					if(gapClose<gapOpen):
						gap = (abs(gapOpen-gapClose)/((gapOpen+gapClose)/2)*100)
					
						appUp = (company,gap,"Opened Higher")
						gapuplist.append(appUp)
						gapuplist.sort(key = sortSecond, reverse = False)
			
	
				if((abs(gapOpen-gapClose)/((gapOpen+gapClose)/2)*100)>1):
					if(gapOpen<gapClose):
						gap = (abs(gapOpen-gapClose)/((gapOpen+gapClose)/2)*100)
					
						app = (company,gap,"Opened Lower")
						gaplowlist.append(app)
						gaplowlist.sort(key = sortSecond, reverse = True)

	
	

	pd.set_option('display.max_rows', None)
	print('-------------------------------------------------------Gap Trading Strategy-------------------------------------------------------')
	lowObj = pd.DataFrame(gaplowlist, columns = ['Company','Gap','Remarks']) 
	lowObj.to_sql(con=database_connection, name='downgaptrading', if_exists='replace')
	print(lowObj)		

	print('--------------------------------------------------------------------------------------------------------------')
	upObj = pd.DataFrame(gapuplist, columns = ['Company','Gap','Remarks']) 
	upObj.to_sql(con=database_connection, name='upgaptrading', if_exists='replace')
	print(upObj)	


def meanReversion():
	removeImages('mean reversion/bbmidcrossover')
	removeImages('mean reversion/adxrsi')

	for c in companies:

		if calculateGeneralSlopeTrend(7, c, 'Close')[0]>0:# Mid cross over strategy. 	
			#[0], [3] are the return values. 0 is the upperbandvalue return from the bollingerBandsCalculations function.
			if lastNValues(5, c, 'Close', 1)[0]>bollingerBandsCalculations(5, c, 'Close',1)[2]:
				if lastNValues(5, c, 'Close', 1)[1]<bollingerBandsCalculations(5, c, 'Close',1)[1]:
					if absolutePercentDiffBetweenTwoNumbers(bollingerBandsCalculations(5, c, 'Close',1)[0],bollingerBandsCalculations(5, c, 'Close',1)[3])>10:
						if statistics.mode(emaCalculations(c, 'Close')[1]) == "Upward Crossover" or statistics.mode(emaCalculations(c,'Close')[1]) == "Check yourself":
							if absolutePercentDiffBetweenTwoNumbers(lastNValues(5, c, 'Close', 1)[0], lastNValues(5, c, 'Close', 2)[0])<6:
								if absolutePercentDiffBetweenTwoNumbers(lastNValues(5, c, 'Close', 1)[0], bollingerBandsCalculations(5, c, 'Close',1)[3])>0.25:
									print("mid list",c)
									plt.figure(figsize=(20, 6))
									plt.plot(allValues(c, 7)[7])
									#plt.plot(bollingerBandsCalculations(5, c, 'Close')[0])
									#plt.plot(bollingerBandsCalculations(5, c, 'Close')[1])
									#plt.plot(bollingerBandsCalculations(5, c, 'Close')[3])
									plt.plot(calculateGeneralSlopeTrend(7, c, 'Close')[2], '--', color='r')
									plt.title(c)
									#plt.show()
									plt.savefig('mean reversion/bbmidcrossover/{fname}.png'.format(fname=c), bbox_inches='tight')

		if calculateGeneralSlopeTrend(30, c, 'Close')[0]>0 and calculateGeneralSlopeTrend(4, c, 'Close')[0]>0:
			if rsiCalculations(14, c, 7, 'Close',1)[0] >= 40 and rsiCalculations(14, c, 7, 'Close',1)[0] <= 60:
				if lastNValues(5, c, 'Close', 1)[1]<bollingerBandsCalculations(5, c, 'Close',1)[1]:
					if adxCalculations(14, c, 7, 1)[0] <= 25:
						if statistics.mode(emaCalculations(c, 'Close')[0]) == "Upward Crossover" or statistics.mode(emaCalculations(c,'Close')[0]) == "Check yourself":
							print("adx",c)
							plt.figure(figsize=(20, 6))
							plt.plot(allValues(c, 7)[7])
							#plt.plot(bollingerBandsCalculations(5, c, 'Close')[0])
							#plt.plot(bollingerBandsCalculations(5, c, 'Close')[1])
							#plt.plot(bollingerBandsCalculations(5, c, 'Close')[3])
							plt.plot(calculateGeneralSlopeTrend(7, c, 'Close')[2], '--', color='r')
							plt.title(c)
							#plt.show()
							plt.savefig('mean reversion/adxrsi/{fname}.png'.format(fname=c), bbox_inches='tight')


def trendTrading():
	for c in companies:
		if HA(c,1)[0]>HA(c,1)[1]: #heiken ashi close today> open today
			if HA(c,1)[0]>HA(c,2)[0]: #heiken ashi close today> close yest
				if HA(c,2)[0]<HA(c,2)[1]: #heiken ashi close yest< open yest
				#if calculateGeneralSlopeTrend(15, c, 'Close')[0]<0:
					print("trend", c)



def midTouchTrendStrategy():#This is a part of the trend trading strategy.
	for c in companies:

		if calculateGeneralSlopeTrend(5, c, 'Close')[0]<0:
			if absolutePercentDiffBetweenTwoNumbers(bollingerBandsCalculations(5, c, 'Close',2)[2],HA(c,1)[0])<3: #percent diff between second last value and mid band value < 3.
				if HA(c,1)[0]>bollingerBandsCalculations(5, c, 'Close',1)[2]: #today's close value>mid bb band value.			
					if (absolutePercentDiffBetweenTwoNumbers(bollingerBandsCalculations(5, c, 'Close',1)[4],HA(c,1)[0])>3) and (bollingerBandsCalculations(5, c, 'Close',1)[4]>HA(c,1)[0]): #percent diff between today's close and upper band value>3 and upper band value> today's close.
						if HA(c,1)[0]>HA(c,1)[1]: #heiken ashi close today> open today
							if HA(c,1)[0]>HA(c,2)[0]: #heiken ashi close today> close yest
								if HA(c,2)[0]<HA(c,2)[1]: #heiken ashi close yest< open yest								
									print("midTouchStrategy",c)

	
                

def lowestPointStrategy():
	ParsePrice()
	list = []
	for c in companies:

		#score  = percentIncreaseOrDecrease(lastNValues(5, c, 'Close', 2)[0],lastNValues(5, c, 'Close', 1)[0])
		#if score<0:
		#if calculateGeneralSlopeTrend(14, c, 'Close')[0]>=0:
		#append = (c,score,lastNValues(5, c, 'Close', 1)[0])
		#list.append(append)
		#list.sort(key = sortSecond, reverse = False)



		momentumscore = percentIncreaseOrDecrease(lastNValues(5, c, 'Close', 2)[0],lastNValues(5, c, 'Close', 1)[0])*lastNValues(5, c, 'Volume', 1)[2]
		if momentumscore<0:
			if calculateGeneralSlopeTrend(14, c, 'Close')[0]>=0:
				if lastNValues(5, c, 'Open', 1)[0]>lastNValues(5, c, 'Close', 1)[0]:
					append = (c,momentumscore ,lastNValues(5, c, 'Close', 1)[0])
					list.append(append)
					list.sort(key = sortSecond, reverse = False)


		#This strategy is very risky. Rsi and bollinger band based lowest point strategy.
		#if calculateGeneralSlopeTrend(14, c, 'Close')[0]>=0:
		#if rsiCalculations(14, c, 4, 'Close',1)[1]<0:
		#if rsiCalculations(14, c, 4, 'Close',1)[0]<=35:
		#if (absolutePercentDiffBetweenTwoNumbers(bollingerBandsCalculations(5, c, 'Close',1)[5],lastNValues(5, c, 'Close', 1)[0])<1):
		#print("lowest point Strategy",c)

	pd.set_option('display.max_rows', None)
	print('-------------------------------------------------------Current Top gainer Strategy-------------------------------------------------------')
	lowObj = pd.DataFrame(list, columns = ['Company','Score','Curr Price']) 
	print(lowObj)	


if __name__ == '__main__':
	collectData()
	gapTrading()
	meanReversion()
	midTouchTrendStrategy()
	trendTrading()
	lowestPointStrategy()

