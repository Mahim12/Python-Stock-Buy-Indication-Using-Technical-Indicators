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
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="hybridtactics"
)

mycursor = mydb.cursor()



#For sorting a list.
def sortSecond(val): 
    return val[1] 

# For calculating the closest value from a list compared to K. For percentile
def closest(list, K):      
    return list[min(range(len(list)), key = lambda i: abs(list[i]-K))] 
      

sloperange = 30 #HOW MANY DAYS SWING SLOPE DO YOU WANT TO CALCULATE?
percentiledays = 10 #how many days percentile, mean, median, max do you want to calculate?


#companylist = pd.read_csv('NIFTY50.csv')
companylist = pd.read_csv('mainCompanylist.csv')
#companylist = pd.read_csv('Companylist.csv')
companies = companylist['Symbol']


def swingtrading():
	slopelist = list()
	sloperangelist = list()
	companylistforbbsqueeze	= list()

	rangeBreakoutList = list()
	crossoverList = list()
	newsctlist = list()
	newmmlist = list()	

	#mycursor.execute("TRUNCATE TABLE `swingtrend`")
	database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('root', '', 'localhost', 'hybridtactics'))

	
	folder_path = (r'slope images')
	test = os.listdir(folder_path)

	for images in test:
		if images.endswith(".png"):
			os.remove(os.path.join(folder_path, images))
		

	for c in companies:
		currentpricepercentile = []

		company = '{fname}'.format(fname = c)

		df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = c))
		x = df['Close'].tail(sloperange).tolist()
		xlastfive = df['Close'].head(-1).tail(5).tolist()
		v = df['Volume'].tail(sloperange).tolist()

		open = df['Open']
		high = df['High']
		low = df['Low']
		currLow =  df['Low'].iloc[-1]

		close = df['Close']
		
		lastprice = df['Close'].iloc[-1]
		lastprice = float(lastprice)
		secondlastclose = df['Close'].iloc[-2]

		LastFivehigh = df['High'].tail(10).mean()
		LastFivelow = df['Low'].tail(10).mean()

		vol = (abs(LastFivehigh-LastFivelow)/((LastFivehigh+LastFivelow)/2)*100)
		canBuy = math.floor(2500/lastprice)
		mainNumber = lastprice*canBuy 
		score = vol/mainNumber 

		bblastfivevalue = df['Close'].head(-1).tail(5).mean()
		


		y = range(len(x))
		ylastfive = range(len(xlastfive))

		best_fit_line = np.poly1d(np.polyfit(y, x, 1))(y)

		#slope = (y[-1] - y[0]) / (x[-1] - x[0])
		angle = np.rad2deg(np.arctan2(y[-1] - y[0], x[-1] - x[0]))
		angle = float(angle)


		slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
		slope = float(slope)
		slopeV, interceptV, r_valueV, p_valueV, std_errV = stats.linregress(v,y)


		slopelastfive, interceptlastfive, r_valuelastfive, p_valuelastfive, std_errlastfive = stats.linregress(xlastfive,ylastfive)

		
		#--------------------------------------------PERCENTILE,MEDIAN,MEAN,MAX FOR SWING CALCULATIONS START----------------------------------
		percentileclose = df['Close'].head(-1)

		median = percentileclose.tail(percentiledays).median()
		mean = percentileclose.tail(percentiledays).mean()
		max =  percentileclose.tail(percentiledays).max()
			
		percentileclose = percentileclose.tail(percentiledays).tolist()

		for i in range(1,101):
				
			currentpricepercentile.append(np.percentile(percentileclose, i))

			indexofcurrentpricepercentile = currentpricepercentile.index(closest(currentpricepercentile, lastprice))
			currentpricepercentileindex = indexofcurrentpricepercentile+1
			currentpricepercentileindex = int(currentpricepercentileindex)
			
		
		#--------------------------------------------PERCENTILE,MEDIAN,MEAN,MAX FOR SWING CALCULATIONS ENDS----------------------------------


		#--------------------------------------------MEAN VOLUME CALCULATIONS STARTS----------------------------------
		meanVolume = df['Volume'].tail(percentiledays).mean()
		#--------------------------------------------MEAN VOLUME CALCULATIONS ENDS----------------------------------
		
		


		#calculating rsi values using ta-lib
		rsi_value = np.array(ta.RSI(close,14))

		#exporting rsi values to csv file in a specified folder
		pd.DataFrame(rsi_value).to_csv('newcompanylist/{fname}/swing trading/{fname}_rsi_value.csv'.format(fname = c))

		retrieveRSI = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_rsi_value.csv'.format(fname = c))
		retrieve_rsi_value = retrieveRSI['0'].iloc[-1]
		retrieve_rsi_value = float(retrieve_rsi_value)

		rsiForRangeBreakout = retrieveRSI['0'].head(-10).tail(10).mean()
		rsiForRangeBreakout = float(rsiForRangeBreakout)
			
			
		xForRSI = retrieveRSI['0'].tail(5).tolist()
		yForRSI = range(len(xForRSI))
		slopeRSI, intercept, r_value, p_value, std_err = stats.linregress(xForRSI,yForRSI)
			
		
		#calculating ADX values using ta-lib
		adx_value = np.array(ta.ADX(high,low,close,14)) 

		pd.DataFrame(adx_value).to_csv("newcompanylist/{fname}/swing trading/{fname}_adxvalue.csv".format(fname=c))

		retrieveadx = pd.read_csv("newcompanylist/{fname}/swing trading/{fname}_adxvalue.csv".format(fname=c))
		retrievedAdxvalue = retrieveadx['0'].iloc[-1]
		retrievedAdxvalue = float(retrievedAdxvalue)


		xForADX = retrieveadx['0'].tail(5).tolist()
		yForADX = range(len(xForADX))
		slopeADX, interceptADX, r_valueADX, p_valueADX, std_errADX = stats.linregress(xForADX,yForADX)

		adxForRangeBreakout = retrieveadx['0'].head(-10).tail(10).mean()
		adxForRangeBreakout = float(adxForRangeBreakout)



		#calculating ema values using ta-lib
			
		ema_value_5 = ta.EMA(np.array(close),5)
		ema_value_8 = ta.EMA(np.array(close),8)
		ema_value_13 = ta.EMA(np.array(close),13)
			

		#exporting ema values to csv file in a specified folder
			
		pd.DataFrame(ema_value_5).to_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_5.csv'.format(fname = c))
		pd.DataFrame(ema_value_8).to_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_8.csv'.format(fname = c))
		pd.DataFrame(ema_value_13).to_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_13.csv'.format(fname = c))
			
		
		retrieveEma_5 = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_5.csv'.format(fname = c))
		retrieve_ema_value_5 = retrieveEma_5['0'].iloc[-1]

		retrieveEma_8 = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_8.csv'.format(fname = c))
		retrieve_ema_value_8 = retrieveEma_8['0'].iloc[-1]
	
		retrieveEma_13 = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_13.csv'.format(fname = c))
		retrieve_ema_value_13 = retrieveEma_13['0'].iloc[-1]

		if retrieve_ema_value_5 > retrieve_ema_value_8 and retrieve_ema_value_5 > retrieve_ema_value_13 and retrieve_ema_value_8 > retrieve_ema_value_13 :	
			emaValue = "Upward Crossover"
		elif retrieve_ema_value_5 < retrieve_ema_value_8 and retrieve_ema_value_5 < retrieve_ema_value_13 and retrieve_ema_value_8 < retrieve_ema_value_13 :	
			emaValue = "Downward Crossover"
		else:
			emaValue = "Check yourself"
		


		

		#calculating bollinger band values using ta-lib

		swingupper, swingmiddle, swinglower = np.array(ta.BBANDS(close, 20, 2, 2, 0))

		pd.DataFrame(swingupper).to_csv('newcompanylist/{fname}/swing trading/{fname}_upperband.csv'.format(fname = c))
		pd.DataFrame(swingmiddle).to_csv('newcompanylist/{fname}/swing trading/{fname}_middleband.csv'.format(fname = c))
		pd.DataFrame(swinglower).to_csv('newcompanylist/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = c))


		upperband = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_upperband.csv'.format(fname = c))
		upperbandvalue = upperband['0'].head(-1).tail(5)
		upperbandvalue = upperbandvalue.mean()

		currupperbandvalue = upperband['0'].iloc[-1]

		middleband = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_middleband.csv'.format(fname = c))
		middlebandvalue = middleband['0'].head(-1).tail(5)
		secondlastmidbollingervalue = middleband['0'].iloc[-2]
		middlebandvalue = middlebandvalue.mean()

		currmiddlebandvalue = middleband['0'].iloc[-1]
			

		lowerband = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = c))
		lowerbandvalue = lowerband['0'].head(-1).tail(5)
		lowerbandvalue = lowerbandvalue.mean()

		currlowerbandvalue = lowerband['0'].iloc[-1]


		if slope>0 and slopeV>0 and lastprice<1000 and meanVolume>1000000:
			

			slopetrendstrategy = (company,angle,slope,currentpricepercentileindex,lastprice,emaValue,retrieve_rsi_value,retrievedAdxvalue)
			slopelist.append(slopetrendstrategy)
			slopelist.sort(key = sortSecond, reverse = False)
			
			


			plt.figure(figsize=(8,6))
			plt.plot(x)
			plt.plot(best_fit_line, '--', color='r')
			plt.title(company+" Last Price: "+str(lastprice))
			#plt.show()
			plt.savefig('slope images/{fname}.png'.format(fname = c), bbox_inches='tight')
			
			mydb.commit()

		

		if slopeRSI>0: #range breakout
			if slopeADX>0: 
				if(rsiForRangeBreakout>=40 and rsiForRangeBreakout<=60): #ignore recent ten values because 10 min for intraday data collection.
					if(adxForRangeBreakout<=25):
						if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)>0.5): #The bollinger band just opened up.
							toappendinrangebreakout = (company,lastprice)
							rangeBreakoutList.append(toappendinrangebreakout)
							rangeBreakoutList.sort(key = sortSecond, reverse = False)

		
		
		if lastprice>currmiddlebandvalue:
			if middlebandvalue>bblastfivevalue :
				if((abs(currupperbandvalue-currlowerbandvalue)/((currupperbandvalue+currlowerbandvalue)/2)*100)>10):	
					if slopeRSI>0:
						toappendincrossover = (company,lastprice)
						crossoverList.append(toappendincrossover)
						crossoverList.sort(key = sortSecond, reverse = False)	



		if slopeRSI<0:
			if retrieve_rsi_value<=35:
				if((abs(lastprice-currlowerbandvalue)/((lastprice+currlowerbandvalue)/2)*100)<1):
					toappend = (company,lastprice)
					newsctlist.append(toappend)
					newsctlist.sort(key = sortSecond, reverse = False)

		
		if slope>0:
			if lastprice>currmiddlebandvalue and lastprice<2500:
				if((abs(lastprice-currupperbandvalue)/((lastprice+currupperbandvalue)/2)*100)>3) and currupperbandvalue>lastprice:
					if currLow>currmiddlebandvalue:
						if slopelastfive<0:
							if((abs(secondlastclose-secondlastmidbollingervalue)/((secondlastclose+secondlastmidbollingervalue)/2)*100)<3):
								toappend = (company,score,lastprice)
								newmmlist.append(toappend)
								newmmlist.sort(key = sortSecond, reverse = True)

				
				
			


	
	pd.set_option('display.max_rows', None)
	
	
	print('-------------------------------------------------------RANGE BREAKOUT STRATEGY-------------------------------------------------------')
	swingObj = pd.DataFrame(rangeBreakoutList, columns = ['Company','Price']) 
	swingObj.to_csv('strategies/swing trading/trend trading/rangebreakouttrading.csv', index=False) 
	print(swingObj)

	print('-------------------------------------------------------CROSSOVER STRATEGY-------------------------------------------------------')
	swingObj = pd.DataFrame(crossoverList, columns = ['Company','Price']) 
	swingObj.to_csv('strategies/swing trading/trend trading/swingcrossovertrading.csv', index=False) 
	print(swingObj)

	print('-------------------------------------------------------SCHAFF BUY STRATEGY-------------------------------------------------------')
	swingObj = pd.DataFrame(newsctlist, columns = ['Company','Price']) 
	swingObj.to_csv('strategies/schaffBuy/schaffbuy.csv', index=False) 
	print(swingObj)

	print('-------------------------------------------------------MIDBOLLINGER TOUCH STRATEGY-------------------------------------------------------')
	swingObj = pd.DataFrame(newmmlist, columns = ['Company','Score','Price']) 
	swingObj.to_csv('strategies/Midtouch/midtouch.csv', index=False) 
	print(swingObj)

			
	#print('-------------------------------------------------------SLOPE TREND TRADING STRATEGY-------------------------------------------------------')
	swingObj = pd.DataFrame(slopelist, columns = ['Company','Angle','Slope','CPP','Price','EMA Value','RSI','ADX']) 
	swingObj.to_sql(con=database_connection, name='swingtrend', if_exists='replace')
	swingObj.to_csv('strategies/swing trading/trend trading/swingtrading.csv', index=False) 
	#print(swingObj)










def meanreversion():
	bollingerlist = []
	rangestrategylist = []		
	swingListforCompare = []
	bollingermidlist = []

	mycursor.execute("TRUNCATE TABLE `rtrade`")
	mycursor.execute("TRUNCATE TABLE `bollingerrange`")
	mycursor.execute("TRUNCATE TABLE `bollingermidcrossover`")	

	for x in companies:
			currentpricepercentile = []
			company = '{fname}'.format(fname = x)

			technical_indicators =  pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = x))
			
			open = technical_indicators['Open']
			high = technical_indicators['High']
			low = technical_indicators['Low']
			close = technical_indicators['Close']
			volume = technical_indicators['Volume']
			meanVolume = technical_indicators['Volume'].tail(5).mean()
				
			bblastfivevalue = technical_indicators['Close'].tail(5).mean()
			BBPercentileClose = technical_indicators['Close'].iloc[-1]
			BBPercentileClose = float(BBPercentileClose)

			#--------------------------------------------PERCENTILE CALCULATIONS START----------------------------------
			percentileclose = technical_indicators['Close'].head(-1)
			median = percentileclose.tail(10).median()
			mean = percentileclose.tail(10).mean()
			max =  percentileclose.tail(10).max()
			percentileclose = percentileclose.tail(10).tolist()

			for i in range(1,101):
			
				currentpricepercentile.append(np.percentile(percentileclose, i))

			indexofcurrentpricepercentile = currentpricepercentile.index(closest(currentpricepercentile, BBPercentileClose))
			currentpricepercentileindex = indexofcurrentpricepercentile+1
			currentpricepercentileindex = int(currentpricepercentileindex)
			#--------------------------------------------PERCENTILE CALCULATIONS ENDS----------------------------------
	
			#--------------------------------------------TOTAL QUANTITY THAT I CAN BUY CALCULATIONS START----------------------------------
			
			
			cash = 13000
			price = BBPercentileClose

			canBuy = math.floor(cash/price)
			#--------------------------------------------TOTAL QUANTITY THAT I CAN BUY CALCULATIONS ENDS----------------------------------



			#--------------------------------------------TA-LIB CALCULATIONS START----------------------------------
			#calculating bollinger band values using ta-lib

			swingupper, swingmiddle, swinglower = np.array(ta.BBANDS(close, 20, 2, 2, 0))

			pd.DataFrame(swingupper).to_csv('newcompanylist/{fname}/swing trading/{fname}_upperband.csv'.format(fname = x))
			pd.DataFrame(swingmiddle).to_csv('newcompanylist/{fname}/swing trading/{fname}_middleband.csv'.format(fname = x))
			pd.DataFrame(swinglower).to_csv('newcompanylist/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = x))


			upperband = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_upperband.csv'.format(fname = x))
			upperbandvalue = upperband['0'].tail(5)
			upperbandvalue = upperbandvalue.mean()

			middleband = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_middleband.csv'.format(fname = x))
			middlebandlastvalue = middleband['0'].iloc[-1]
			middlebandvalue = middleband['0'].tail(5)
			middlebandvalue = middlebandvalue.mean()
			

			lowerband = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = x))
			lowerbandvalue = lowerband['0'].tail(5)
			lowerbandvalue = lowerbandvalue.mean()



			#calculating rsi values using ta-lib
			rsi_value = np.array(ta.RSI(close,14))

			#exporting rsi values to csv file in a specified folder
			pd.DataFrame(rsi_value).to_csv('newcompanylist/{fname}/swing trading/{fname}_rsi_value.csv'.format(fname = x))

			retrieveRSI = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_rsi_value.csv'.format(fname = x))
			retrieve_rsi_value = retrieveRSI['0'].tail(10).mean()
			retrieve_rsi_value = float(retrieve_rsi_value)
		

			#calculating ADX values using ta-lib
			adx_value = np.array(ta.ADX(high,low,close,14)) 

			pd.DataFrame(adx_value).to_csv("newcompanylist/{fname}/swing trading/{fname}_adxvalue.csv".format(fname=x))

			retrieveadx = pd.read_csv("newcompanylist/{fname}/swing trading/{fname}_adxvalue.csv".format(fname=x))
			retrievedAdxvalue = retrieveadx['0'].tail(10).mean()
			retrievedAdxvalue = float(retrievedAdxvalue)
			
			#calculating ema values using ta-lib
			
			ema_value_5 = ta.EMA(np.array(close),5)
			ema_value_8 = ta.EMA(np.array(close),8)
			ema_value_13 = ta.EMA(np.array(close),13)
			

			#exporting ema values to csv file in a specified folder
			
			pd.DataFrame(ema_value_5).to_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_5.csv'.format(fname = x))
			pd.DataFrame(ema_value_8).to_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_8.csv'.format(fname = x))
			pd.DataFrame(ema_value_13).to_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_13.csv'.format(fname = x))
			
		
			retrieveEma_5 = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_5.csv'.format(fname = x))
			retrieve_ema_value_5 = retrieveEma_5['0'].iloc[-1]

			retrieveEma_8 = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_8.csv'.format(fname = x))
			retrieve_ema_value_8 = retrieveEma_8['0'].iloc[-1]
	
			retrieveEma_13 = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}_ema_value_13.csv'.format(fname = x))
			retrieve_ema_value_13 = retrieveEma_13['0'].iloc[-1]

			if retrieve_ema_value_5 > retrieve_ema_value_8 and retrieve_ema_value_5 > retrieve_ema_value_13 and retrieve_ema_value_8 > retrieve_ema_value_13 :	
				emaValue = "Upward Crossover"
			elif retrieve_ema_value_5 < retrieve_ema_value_8 and retrieve_ema_value_5 < retrieve_ema_value_13 and retrieve_ema_value_8 < retrieve_ema_value_13 :	
				emaValue = "Downward Crossover"
			else:
				emaValue = "Check yourself"

			#--------------------------------------------TA-LIB CALCULATIONS ENDS----------------------------------

			if(retrieve_rsi_value>=40 and retrieve_rsi_value<=60):
				if(retrievedAdxvalue<=25):
					if(bblastfivevalue<middlebandvalue):
						if BBPercentileClose<10000:	
							toappendonrangestrategy = (company,currentpricepercentileindex,BBPercentileClose,retrieve_rsi_value,retrievedAdxvalue,emaValue)
							rangestrategylist.append(toappendonrangestrategy)
							rangestrategylist.sort(key = sortSecond, reverse = False)

								
							sql = "INSERT INTO `rtrade` (company,cpp,price,rsi,adx,ema)  VALUES (%s, %s, %s, %s, %s, %s)"
							val = (company,currentpricepercentileindex,BBPercentileClose,retrieve_rsi_value,retrievedAdxvalue,emaValue)
							mycursor.execute(sql, val)

								


			if canBuy>0:
				if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)>10) or ((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)<=45) and meanVolume>1000000:
					if(BBPercentileClose>middlebandlastvalue):
						if(bblastfivevalue<middlebandvalue):
							
							BollingerSqueeze = (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)
							BollingerSqueeze = float(BollingerSqueeze)
							
							sql = "INSERT INTO `bollingermidcrossover` (company,bollingersquueze,cpp,price)  VALUES (%s, %s, %s, %s)"
							val = (company,BollingerSqueeze,currentpricepercentileindex,BBPercentileClose)
							mycursor.execute(sql, val)
							
							toappendinbollingersqueeze = (company,BollingerSqueeze,currentpricepercentileindex,BBPercentileClose)
							bollingermidlist.append(toappendinbollingersqueeze)
							bollingermidlist.sort(key = sortSecond, reverse = True)
	
			

	pd.set_option('display.max_rows', None)	

	print('-------------------------------------------------------BOLINGER-MID-CROSSOVER STRATEGY-------------------------------------------------------')			
	Bollinger2Obj = pd.DataFrame(bollingermidlist, columns = ['Company','Mean Reversion Squeeze','Percentile(CPP)','Close']) 
	Bollinger2Obj.to_csv('strategies/swing trading/mean reversion/bbmidcrossover.csv', index=False) 
	print(Bollinger2Obj)
		

	RangeObj = pd.DataFrame(rangestrategylist, columns = ['Company','Percentile(CPP)','Price','Average RSI','Average ADX','EMA Value']) 
	RangeObj.to_csv('strategies/swing trading/mean reversion/adxrsirange.csv', index=False) 
	print('-------------------------------------------------------RANGE TRADING(RSI AND ADX) MEAN REVERSION STRATEGY-------------------------------------------------------')	
	print(RangeObj)


if __name__ == '__main__':
	meanreversion()
	swingtrading()
	
	
	
	
		

		








