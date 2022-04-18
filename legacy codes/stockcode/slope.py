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
companies = companylist['Symbol']

intradayallowedlist = pd.read_csv('intradayallowed.csv')
intradayallowed = intradayallowedlist['Allowed'].tolist()



#--------------------------------------------EVERY COMPANY SWING DATA GATHERING STARTS----------------------------------

def extractSwingData():
	start = time.time()
	print(start)
	list = []
	total_calls_a_day= 1
	while total_calls_a_day<2:	
		total_calls_a_day+=1
	
		start = datetime.datetime(2010, 1, 1)
		end = datetime.datetime.today()

		niftyprice = web.DataReader('^NSEI', 'yahoo', start, end) 
		niftyprice.to_csv('companies/nifty.csv')


		dowJonesprice = web.DataReader('^DJI', 'yahoo', start, end) 
		dowJonesprice.to_csv('companies/dowjones.csv')


		for x in companies:
			company = '{fname}'.format(fname = x)
	 
			companyname = web.DataReader('{fname}'.format(fname = x), 'yahoo', start, end)
 
			companyname.to_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))
			print(company)

	end = time.time()
	elapsed = done - start
	print(elapsed)

		
#--------------------------------------------EVERY COMPANY SWING DATA GATHERING ENDS----------------------------------




def swingtrading():
	slopelist = list()
	sloperangelist = list()

	gaplowlist = list()
	gapuplist = list()


	companylistforbbsqueeze	= list()

	#mycursor.execute("TRUNCATE TABLE `swingtrend`")
	database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('root', '', 'localhost', 'hybridtactics'))

	
	nifty = pd.read_csv('companies/nifty.csv')
	niftyClose = nifty['Close'].tail(sloperange)


	for c in companies:
		currentpricepercentile = []

		company = '{fname}'.format(fname = c)

		df = pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = c))

		
		closeForCorr = df['Close'].tail(sloperange)
		Companycorr, _ = pearsonr(niftyClose, closeForCorr)

		x = df['Close'].tail(sloperange).tolist()
		v = df['Volume'].tail(sloperange).tolist()

		open = df['Open']
		high = df['High']
		low = df['Low']
		close = df['Close']
		
		lastprice = df['Close'].iloc[-1]
		lastprice = float(lastprice)

		
		xForRange = df['Close'].tail(10).tolist()
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



		# GAP TRADING STRATEGY BEGINS

		gapOpen = df['Open'].iloc[-1]
		gapHigh = df['High']
		gapLow = df['Low']
		gapClose = df['Close'].iloc[-2]

		openForRange = df['Open'].tail(10).mean()
		highForRange = df['High'].tail(10).mean()
		lowForRange = df['Low'].tail(10).mean()

		high2OpenRange = (abs(highForRange-openForRange)/((highForRange+openForRange)/2)*100)
		open2LowRange = (abs(lowForRange-openForRange)/((lowForRange+openForRange)/2)*100)

		cash = 6000
		canBuy = math.floor(cash/lastprice)
	
		if company in intradayallowed:
			if((abs(gapOpen-gapClose)/((gapOpen+gapClose)/2)*100)>1):
				if(gapClose<gapOpen):
					gap = (abs(gapOpen-gapClose)/((gapOpen+gapClose)/2)*100)
					
					appUp = (company,gap,"Opened Higher",high2OpenRange,open2LowRange,slope,Companycorr,canBuy)
					gapuplist.append(appUp)
					gapuplist.sort(key = sortSecond, reverse = True)
			
	
			if((abs(gapOpen-gapClose)/((gapOpen+gapClose)/2)*100)>1):
				if(gapOpen<gapClose):
					gap = (abs(gapOpen-gapClose)/((gapOpen+gapClose)/2)*100)
					
					app = (company,gap,"Opened Lower",high2OpenRange,open2LowRange,slope,Companycorr,canBuy)
					gaplowlist.append(app)
					gaplowlist.sort(key = sortSecond, reverse = True)

		# GAP TRADING STRATEGY ENDS
				


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
		pd.DataFrame(rsi_value).to_csv('companies/{fname}/swing trading/{fname}_rsi_value.csv'.format(fname = c))

		retrieveRSI = pd.read_csv('companies/{fname}/swing trading/{fname}_rsi_value.csv'.format(fname = c))
		retrieve_rsi_value = retrieveRSI['0'].iloc[-1]
		retrieve_rsi_value = float(retrieve_rsi_value)
			
		
		#calculating ADX values using ta-lib
		adx_value = np.array(ta.ADX(high,low,close,14)) 

		pd.DataFrame(adx_value).to_csv("companies/{fname}/swing trading/{fname}_adxvalue.csv".format(fname=c))

		retrieveadx = pd.read_csv("companies/{fname}/swing trading/{fname}_adxvalue.csv".format(fname=c))
		retrievedAdxvalue = retrieveadx['0'].iloc[-1]
		retrievedAdxvalue = float(retrievedAdxvalue)

		#calculating ema values using ta-lib
			
		ema_value_5 = ta.EMA(np.array(close),5)
		ema_value_8 = ta.EMA(np.array(close),8)
		ema_value_13 = ta.EMA(np.array(close),13)
			

		#exporting ema values to csv file in a specified folder
			
		pd.DataFrame(ema_value_5).to_csv('companies/{fname}/swing trading/{fname}_ema_value_5.csv'.format(fname = c))
		pd.DataFrame(ema_value_8).to_csv('companies/{fname}/swing trading/{fname}_ema_value_8.csv'.format(fname = c))
		pd.DataFrame(ema_value_13).to_csv('companies/{fname}/swing trading/{fname}_ema_value_13.csv'.format(fname = c))
			
		
		retrieveEma_5 = pd.read_csv('companies/{fname}/swing trading/{fname}_ema_value_5.csv'.format(fname = c))
		retrieve_ema_value_5 = retrieveEma_5['0'].iloc[-1]

		retrieveEma_8 = pd.read_csv('companies/{fname}/swing trading/{fname}_ema_value_8.csv'.format(fname = c))
		retrieve_ema_value_8 = retrieveEma_8['0'].iloc[-1]
	
		retrieveEma_13 = pd.read_csv('companies/{fname}/swing trading/{fname}_ema_value_13.csv'.format(fname = c))
		retrieve_ema_value_13 = retrieveEma_13['0'].iloc[-1]

		if retrieve_ema_value_5 > retrieve_ema_value_8 and retrieve_ema_value_5 > retrieve_ema_value_13 and retrieve_ema_value_8 > retrieve_ema_value_13 :	
			emaValue = "Upward Crossover"
		elif retrieve_ema_value_5 < retrieve_ema_value_8 and retrieve_ema_value_5 < retrieve_ema_value_13 and retrieve_ema_value_8 < retrieve_ema_value_13 :	
			emaValue = "Downward Crossover"
		else:
			emaValue = "Check yourself"
		

		if slope>0 and slopeV>0 and lastprice<1000 and meanVolume>1000000:
			

			slopetrendstrategy = (company,slope,angle,currentpricepercentileindex,lastprice,emaValue,retrieve_rsi_value,retrievedAdxvalue)
			slopelist.append(slopetrendstrategy)
			slopelist.sort(key = sortSecond, reverse = False)
			
			


			plt.figure(figsize=(8,6))
			plt.plot(x)
			plt.plot(best_fit_line, '--', color='r')
			plt.title(company+" Last Price: "+str(lastprice))
			# plt.show()
			plt.savefig('slope images/{fname}.png'.format(fname = c), bbox_inches='tight')


			mydb.commit()
			

		if slopeT==0 and lastprice<1000 and meanVolume>1000000:
			sloperangestrategy = (company,slope,angle,currentpricepercentileindex,lastprice,emaValue,retrieve_rsi_value,retrievedAdxvalue)
			sloperangelist.append(sloperangestrategy)
			
			


	
	pd.set_option('display.max_rows', None)
	print('-------------------------------------------------------SLOPE TREND TRADING STRATEGY-------------------------------------------------------')
	swingObj = pd.DataFrame(slopelist, columns = ['Company','Slope','Angle','CPP','Price','EMA Value','RSI','ADX']) 
	swingObj.to_sql(con=database_connection, name='swingtrend', if_exists='replace')
	print(swingObj)

	print('-------------------------------------------------------SLOPE(0) RANGE TRADING STRATEGY-------------------------------------------------------')
	SlopeRangegObj = pd.DataFrame(sloperangelist, columns = ['Company','Slope','Angle','CPP','Price','EMA Value','RSI','ADX']) 
	SlopeRangegObj.to_sql(con=database_connection, name='sloperangestrategy', if_exists='replace')
	print(SlopeRangegObj)

	print('-------------------------------------------------------Gap Trading Strategy-------------------------------------------------------')
	lowObj = pd.DataFrame(gaplowlist, columns = ['Company','Gap','Remarks','HighOpenRange','LowOpenRange','Slope','Correlation','Qty']) 
	print(lowObj)		

	print('--------------------------------------------------------------------------------------------------------------')
	upObj = pd.DataFrame(gapuplist, columns = ['Company','Gap','Remarks','HighOpenRange','LowOpenRange','Slope','Correlation','Qty']) 
	print(upObj)		



#--------------------------------------------BOLLINGER BAND SQUEEZE CALCULATIONS STARTS----------------------------------
def bbswingsqueeze():
	bollingerlist = []	

	database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('root', '', 'localhost', 'hybridtactics'))
	
	for x in companies:
			currentpricepercentile = []
			company = '{fname}'.format(fname = x)

			technical_indicators =  pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))
			
			open = technical_indicators['Open']
			high = technical_indicators['High']
			low = technical_indicators['Low']
			close = technical_indicators['Close']
			volume = technical_indicators['Volume']
			BBPercentileClose = technical_indicators['Close'].iloc[-1]
			BBPercentileClose = float(BBPercentileClose)

			#--------------------------------------------PERCENTILE CALCULATIONS START----------------------------------
			percentileclose = technical_indicators['Close'].head(-1)
			median = percentileclose.tail(10).median()
			median = float(median)
			mean = percentileclose.tail(10).mean()
			mean = float(mean)
			max =  percentileclose.tail(10).max()
			max = float(max)
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
			#calculating ema values using ta-lib

			swingupper, swingmiddle, swinglower = np.array(ta.BBANDS(close, 20, 2, 2, 0))

			pd.DataFrame(swingupper).to_csv('companies/{fname}/swing trading/{fname}_upperband.csv'.format(fname = x))
			pd.DataFrame(swingmiddle).to_csv('companies/{fname}/swing trading/{fname}_middleband.csv'.format(fname = x))
			pd.DataFrame(swinglower).to_csv('companies/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = x))


			upperband = pd.read_csv('companies/{fname}/swing trading/{fname}_upperband.csv'.format(fname = x))
			upperbandvalue = upperband['0'].tail(5)
			upperbandvalue = upperbandvalue.mean()

			middleband = pd.read_csv('companies/{fname}/swing trading/{fname}_middleband.csv'.format(fname = x))
			middlebandvalue = middleband['0'].tail(5)
			middlebandvalue = middlebandvalue.mean()

			lowerband = pd.read_csv('companies/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = x))
			lowerbandvalue = lowerband['0'].tail(5)
			lowerbandvalue = lowerbandvalue.mean()
			#--------------------------------------------TA-LIB CALCULATIONS ENDS----------------------------------



			if canBuy>0:
				if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)<0.5 and (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)>0.000010):
					BollingerSqueeze = (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)
					
					mainscore = currentpricepercentileindex*BollingerSqueeze

					BollingerSqueeze = float(BollingerSqueeze)
					mainscore = float(mainscore)
					

					toappendinbollingersqueeze = (company,mainscore,BollingerSqueeze,currentpricepercentileindex,median,mean,max,BBPercentileClose)
					bollingerlist.append(toappendinbollingersqueeze)
					bollingerlist.sort(key = sortSecond, reverse = False)
					
	print('-------------------------------------------------------BBSQUEEZE STRATEGY-------------------------------------------------------')
				
	BollingerObj = pd.DataFrame(bollingerlist, columns = ['Company','Main Score','BollingerSqueeze','Percentile(CPP)','Median','Mean','Max','Close']) 
	BollingerObj.to_sql(con=database_connection, name='swingsqueeze', if_exists='replace')
	print(BollingerObj)
#--------------------------------------------BOLLINGER BAND SQUEEZE CALCULATIONS ENDS----------------------------------






#--------------------------------------------BB-MID-CROSSOVER CALCULATIONS STARTS----------------------------------
def bbmidcrossover():
	bollingermidlist = []

	mycursor.execute("TRUNCATE TABLE `bollingermidcrossover`")
		
	for x in companies:
			currentpricepercentile = []
			company = '{fname}'.format(fname = x)

			technical_indicators =  pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))
			
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
			#calculating ema values using ta-lib

			swingupper, swingmiddle, swinglower = np.array(ta.BBANDS(close, 20, 2, 2, 0))

			pd.DataFrame(swingupper).to_csv('companies/{fname}/swing trading/{fname}_upperband.csv'.format(fname = x))
			pd.DataFrame(swingmiddle).to_csv('companies/{fname}/swing trading/{fname}_middleband.csv'.format(fname = x))
			pd.DataFrame(swinglower).to_csv('companies/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = x))


			upperband = pd.read_csv('companies/{fname}/swing trading/{fname}_upperband.csv'.format(fname = x))
			upperbandvalue = upperband['0'].tail(5)
			upperbandvalue = upperbandvalue.mean()

			middleband = pd.read_csv('companies/{fname}/swing trading/{fname}_middleband.csv'.format(fname = x))
			middlebandlastvalue = middleband['0'].iloc[-1]
			middlebandvalue = middleband['0'].tail(5)
			middlebandvalue = middlebandvalue.mean()
			

			lowerband = pd.read_csv('companies/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = x))
			lowerbandvalue = lowerband['0'].tail(5)
			lowerbandvalue = lowerbandvalue.mean()
			#--------------------------------------------TA-LIB CALCULATIONS ENDS----------------------------------


			
			if canBuy>0:
				if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)>10) and meanVolume>1000000:
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
	print('-------------------------------------------------------BOLINGER-MID-CROSSOVER STRATEGY-------------------------------------------------------')
				
	Bollinger2Obj = pd.DataFrame(bollingermidlist, columns = ['Company','Mean Reversion Squeeze','Percentile(CPP)','Close']) 
	
	print(Bollinger2Obj)
	
#--------------------------------------------BB-MID-CROSSOVER CALCULATIONS ENDS----------------------------------








#--------------------------------------------MEAN REVERSION CALCULATIONS STARTS----------------------------------
def meanreversion():
	bollingerlist = []
	rangestrategylist = []		

	mycursor.execute("TRUNCATE TABLE `rtrade`")
	mycursor.execute("TRUNCATE TABLE `bollingerrange`")	

	for x in companies:
			currentpricepercentile = []
			company = '{fname}'.format(fname = x)

			technical_indicators =  pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))
			
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

			pd.DataFrame(swingupper).to_csv('companies/{fname}/swing trading/{fname}_upperband.csv'.format(fname = x))
			pd.DataFrame(swingmiddle).to_csv('companies/{fname}/swing trading/{fname}_middleband.csv'.format(fname = x))
			pd.DataFrame(swinglower).to_csv('companies/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = x))


			upperband = pd.read_csv('companies/{fname}/swing trading/{fname}_upperband.csv'.format(fname = x))
			upperbandvalue = upperband['0'].tail(5)
			upperbandvalue = upperbandvalue.mean()

			middleband = pd.read_csv('companies/{fname}/swing trading/{fname}_middleband.csv'.format(fname = x))
			middlebandlastvalue = middleband['0'].iloc[-1]
			middlebandvalue = middleband['0'].tail(5)
			middlebandvalue = middlebandvalue.mean()
			

			lowerband = pd.read_csv('companies/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = x))
			lowerbandvalue = lowerband['0'].tail(5)
			lowerbandvalue = lowerbandvalue.mean()



			#calculating rsi values using ta-lib
			rsi_value = np.array(ta.RSI(close,14))

			#exporting rsi values to csv file in a specified folder
			pd.DataFrame(rsi_value).to_csv('companies/{fname}/swing trading/{fname}_rsi_value.csv'.format(fname = x))

			retrieveRSI = pd.read_csv('companies/{fname}/swing trading/{fname}_rsi_value.csv'.format(fname = x))
			retrieve_rsi_value = retrieveRSI['0'].tail(10).mean()
			retrieve_rsi_value = float(retrieve_rsi_value)
		

			#calculating ADX values using ta-lib
			adx_value = np.array(ta.ADX(high,low,close,14)) 

			pd.DataFrame(adx_value).to_csv("companies/{fname}/swing trading/{fname}_adxvalue.csv".format(fname=x))

			retrieveadx = pd.read_csv("companies/{fname}/swing trading/{fname}_adxvalue.csv".format(fname=x))
			retrievedAdxvalue = retrieveadx['0'].tail(10).mean()
			retrievedAdxvalue = float(retrievedAdxvalue)
			
			#calculating ema values using ta-lib
			
			ema_value_5 = ta.EMA(np.array(close),5)
			ema_value_8 = ta.EMA(np.array(close),8)
			ema_value_13 = ta.EMA(np.array(close),13)
			

			#exporting ema values to csv file in a specified folder
			
			pd.DataFrame(ema_value_5).to_csv('companies/{fname}/swing trading/{fname}_ema_value_5.csv'.format(fname = x))
			pd.DataFrame(ema_value_8).to_csv('companies/{fname}/swing trading/{fname}_ema_value_8.csv'.format(fname = x))
			pd.DataFrame(ema_value_13).to_csv('companies/{fname}/swing trading/{fname}_ema_value_13.csv'.format(fname = x))
			
		
			retrieveEma_5 = pd.read_csv('companies/{fname}/swing trading/{fname}_ema_value_5.csv'.format(fname = x))
			retrieve_ema_value_5 = retrieveEma_5['0'].iloc[-1]

			retrieveEma_8 = pd.read_csv('companies/{fname}/swing trading/{fname}_ema_value_8.csv'.format(fname = x))
			retrieve_ema_value_8 = retrieveEma_8['0'].iloc[-1]
	
			retrieveEma_13 = pd.read_csv('companies/{fname}/swing trading/{fname}_ema_value_13.csv'.format(fname = x))
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
					toappendonrangestrategy = (company,currentpricepercentileindex,BBPercentileClose,retrieve_rsi_value,retrievedAdxvalue,emaValue)
					rangestrategylist.append(toappendonrangestrategy)
					rangestrategylist.sort(key = sortSecond, reverse = False)

					
					sql = "INSERT INTO `rtrade` (company,cpp,price,rsi,adx,ema)  VALUES (%s, %s, %s, %s, %s, %s)"
					val = (company,currentpricepercentileindex,BBPercentileClose,retrieve_rsi_value,retrievedAdxvalue,emaValue)
					mycursor.execute(sql, val)

		


			
			if canBuy>0:
				if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)<=45) and meanVolume>1000000:
					if(BBPercentileClose>middlebandlastvalue):
						if(bblastfivevalue<middlebandvalue):
							if(currentpricepercentileindex>90):
								BollingerSqueeze = (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)
								BollingerSqueeze = float(BollingerSqueeze)
					
								toappendinbollingersqueeze = (company,BollingerSqueeze,currentpricepercentileindex,BBPercentileClose)
								bollingerlist.append(toappendinbollingersqueeze)
								bollingerlist.sort(key = sortSecond, reverse = True)

								sql = "INSERT INTO `bollingerrange` (company,bollingersquueze,cpp,price)  VALUES (%s, %s, %s, %s)"
								val = (company,BollingerSqueeze,currentpricepercentileindex,BBPercentileClose)
								mycursor.execute(sql, val)

	pd.set_option('display.max_rows', None)			
	BollingerObj = pd.DataFrame(bollingerlist, columns = ['Company','Bollinger Range Squeeze','Percentile(CPP)','Price']) 
	print('-------------------------------------------------------BOLLINGER RANGE STRATEGY-------------------------------------------------------')
	
	print(BollingerObj)


	RangeObj = pd.DataFrame(rangestrategylist, columns = ['Company','Percentile(CPP)','Price','Average RSI','Average ADX','EMA Value']) 
	print('-------------------------------------------------------RANGE TRADING(RSI AND ADX) MEAN REVERSION STRATEGY-------------------------------------------------------')
	
	print(RangeObj)
#--------------------------------------------MEAN REVERSION CALCULATIONS ENDS----------------------------------


def intraday():

	total_calls_a_day= 1
	while total_calls_a_day<75:	
		total_calls_a_day+=1

		slopelist = list()
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
		
			# GET INTRADAY DATA
			data = yf.download(tickers=c,period="1d",interval="1m")
			data.to_csv('companies/{fname}/intraday trading/{fname}_intraday.csv'.format(fname = c))
			company = '{fname}'.format(fname = c)

			technical_indicators_intraday = pd.read_csv('companies/{fname}/intraday trading/{fname}_intraday.csv'.format(fname = c))

			open = technical_indicators_intraday['Open']
			high = technical_indicators_intraday['High']
			low = technical_indicators_intraday['Low']
			close = technical_indicators_intraday['Close']

			
			bblastfivevalue = technical_indicators_intraday['Close'].tail(5).mean()
			BBPercentileClose = technical_indicators_intraday['Close'].iloc[-1]
			BBPercentileClose = float(BBPercentileClose)

		
			x = technical_indicators_intraday['Close'].tail(10).tolist()
			v = technical_indicators_intraday['Volume'].tail(10).tolist()

		
		
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
			middlebandvalue = middleband['0'].tail(5)
			middlebandvalue = middlebandvalue.mean()
			

			lowerband = pd.read_csv('companies/{fname}/intraday trading/{fname}_lowerband.csv'.format(fname = c))
			lowerbandvalue = lowerband['0'].tail(5)
			lowerbandvalue = lowerbandvalue.mean()


			#calculating rsi values using ta-lib
			rsi_value = np.array(ta.RSI(close,14))

			#exporting rsi values to csv file in a specified folder
			pd.DataFrame(rsi_value).to_csv('companies/{fname}/intraday trading/{fname}_rsi_value.csv'.format(fname = c))

			retrieveRSI = pd.read_csv('companies/{fname}/intraday trading/{fname}_rsi_value.csv'.format(fname = c))
			retrieve_rsi_value = retrieveRSI['0'].iloc[-1]
			retrieve_rsi_value = float(retrieve_rsi_value)
			
		
			#calculating ADX values using ta-lib
			adx_value = np.array(ta.ADX(high,low,close,14)) 

			pd.DataFrame(adx_value).to_csv("companies/{fname}/intraday trading/{fname}_adxvalue.csv".format(fname=c))

			retrieveadx = pd.read_csv("companies/{fname}/intraday trading/{fname}_adxvalue.csv".format(fname=c))
			retrievedAdxvalue = retrieveadx['0'].iloc[-1]
			retrievedAdxvalue = float(retrievedAdxvalue)

			#calculating ema values using ta-lib
			
			ema_value_5 = ta.EMA(np.array(close),5)
			ema_value_8 = ta.EMA(np.array(close),8)
			ema_value_13 = ta.EMA(np.array(close),13)
			

			#exporting ema values to csv file in a specified folder
			
			pd.DataFrame(ema_value_5).to_csv('companies/{fname}/intraday trading/{fname}_ema_value_5.csv'.format(fname = c))
			pd.DataFrame(ema_value_8).to_csv('companies/{fname}/intraday trading/{fname}_ema_value_8.csv'.format(fname = c))
			pd.DataFrame(ema_value_13).to_csv('companies/{fname}/intraday trading/{fname}_ema_value_13.csv'.format(fname = c))
			
		
			retrieveEma_5 = pd.read_csv('companies/{fname}/intraday trading/{fname}_ema_value_5.csv'.format(fname = c))
			retrieve_ema_value_5 = retrieveEma_5['0'].iloc[-1]

			retrieveEma_8 = pd.read_csv('companies/{fname}/intraday trading/{fname}_ema_value_8.csv'.format(fname = c))
			retrieve_ema_value_8 = retrieveEma_8['0'].iloc[-1]
	
			retrieveEma_13 = pd.read_csv('companies/{fname}/intraday trading/{fname}_ema_value_13.csv'.format(fname = c))
			retrieve_ema_value_13 = retrieveEma_13['0'].iloc[-1]

			if retrieve_ema_value_5 > retrieve_ema_value_8 and retrieve_ema_value_5 > retrieve_ema_value_13 and retrieve_ema_value_8 > retrieve_ema_value_13 :	
				emaValue = "Upward Crossover"
			elif retrieve_ema_value_5 < retrieve_ema_value_8 and retrieve_ema_value_5 < retrieve_ema_value_13 and retrieve_ema_value_8 < retrieve_ema_value_13 :	
				emaValue = "Downward Crossover"
			else:
				emaValue = "Check yourself"
		

			if slope<0:
				slopetrendstrategy = (company,slope,angle,lastprice,emaValue,retrieve_rsi_value,retrievedAdxvalue)
				slopelist.append(slopetrendstrategy)
				slopelist.sort(key = sortSecond, reverse = False)
			

			if slopeT==0:
				sloperangestrategy = (company,slope,angle,lastprice,emaValue,retrieve_rsi_value,retrievedAdxvalue)
				sloperangelist.append(sloperangestrategy)


			if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)<0.5 and (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)>0.000010):
				BollingerSqueeze = (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)
				BollingerSqueeze = float(BollingerSqueeze)
				
				toappendinbollingersqueeze = (company,BollingerSqueeze,BBPercentileClose)
				bollingerlist.append(toappendinbollingersqueeze)
				bollingerlist.sort(key = sortSecond, reverse = False)


			if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)>10):
					if(BBPercentileClose>middlebandlastvalue):
						if(bblastfivevalue<middlebandvalue):
							
							BollingerSqueeze = (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)
							BollingerSqueeze = float(BollingerSqueeze)

							toappendinbollingersqueeze = (company,BollingerSqueeze,BBPercentileClose)
							bollingermidlist.append(toappendinbollingersqueeze)
							bollingermidlist.sort(key = sortSecond, reverse = True)

			if(retrieve_rsi_value>=40 and retrieve_rsi_value<=60):
				if(retrievedAdxvalue<=25):
					toappendonrangestrategy = (company,BBPercentileClose,retrieve_rsi_value,retrievedAdxvalue,emaValue)
					rangestrategylist.append(toappendonrangestrategy)
					rangestrategylist.sort(key = sortSecond, reverse = False)
			

			if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)<=45):
					if(BBPercentileClose>middlebandlastvalue):
						if(bblastfivevalue<middlebandvalue):
							
							BollingerSqueeze = (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)
							BollingerSqueeze = float(BollingerSqueeze)
					
							toappendinbollingersqueeze = (company,BollingerSqueeze,BBPercentileClose)
							bollingerIntradaylist.append(toappendinbollingersqueeze)
							bollingerIntradaylist.sort(key = sortSecond, reverse = True)

					
	
		pd.set_option('display.max_rows', None)
		print('-------------------------------------------------------SLOPE TREND TRADING STRATEGY-------------------------------------------------------')
		swingObj = pd.DataFrame(slopelist, columns = ['Company','Slope','Angle','Price','EMA Value','RSI','ADX']) 
		print(swingObj)

		print('-------------------------------------------------------SLOPE(0) RANGE TRADING STRATEGY-------------------------------------------------------')
		SlopeRangegObj = pd.DataFrame(sloperangelist, columns = ['Company','Slope','Angle','Price','EMA Value','RSI','ADX']) 
		print(SlopeRangegObj)

		print('-------------------------------------------------------BBSQUEEZE STRATEGY-------------------------------------------------------')		
		IntradayBollingerSqueezeObj = pd.DataFrame(bollingerlist, columns = ['Company','BollingerSqueeze','Close']) 
		print(IntradayBollingerSqueezeObj)

		print('-------------------------------------------------------BOLINGER-MID-CROSSOVER STRATEGY-------------------------------------------------------')		
		Bollinger2Obj = pd.DataFrame(bollingermidlist, columns = ['Company','Mean Reversion Squeeze','Close']) 
		print(Bollinger2Obj)
		
		print('-------------------------------------------------------RANGE TRADING(RSI AND ADX) MEAN REVERSION STRATEGY-------------------------------------------------------')
		RangeObj = pd.DataFrame(rangestrategylist, columns = ['Company','Price','Average RSI','Average ADX','EMA Value']) 
		print(RangeObj)

		print('-------------------------------------------------------BOLLINGER RANGE STRATEGY-------------------------------------------------------')
		BollingerIntradayObj = pd.DataFrame(bollingerIntradaylist, columns = ['Company','Bollinger Range Squeeze','Price']) 
		print(BollingerIntradayObj)
	

		time.sleep(600)


if __name__ == '__main__':
	extractSwingData()
	meanreversion()
	bbmidcrossover()
	swingtrading()
	bbswingsqueeze()
	#intraday()
	
	
	
		

		








