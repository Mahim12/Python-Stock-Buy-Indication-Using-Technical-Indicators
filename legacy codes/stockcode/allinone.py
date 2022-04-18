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



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="companies"
)

mycursor = mydb.cursor()

# For calculating the closest value from a list compared to K. For percentile
def closest(list, K):      
    return list[min(range(len(list)), key = lambda i: abs(list[i]-K))] 
      

#For sorting a list.
def sortSecond(val): 
    return val[1] 



#Calcuting variance
def var(X):
    S = 0.0
    SS = 0.0
    for x in X:
        S += x
        SS += x*x
    xbar = S/float(len(X))
    return (SS - len(X) * xbar * xbar) / (len(X) -1.0)



#Calcuting co-variance
def cov(X,Y):
    n = len(X)
    xbar = sum(X) / n
    ybar = sum(Y) / n
    return sum([(x-xbar)*(y-ybar) for x,y in zip(X,Y)])/(n-1)



#Calcuting trend
def beta(x,y):
    return cov(x,y)/var(x)


start = datetime.datetime(2017, 9, 1)
end = datetime.datetime.today()



# companylist = pd.read_csv('500companies.csv')
# companylist = pd.read_csv('mainCompanylist.csv')

companylist = pd.read_csv('mainCompanylist.csv')
companies = companylist['Symbol']





#--------------------------------------------BOLLINGER BAND SQUEEZE CALCULATIONS STARTS----------------------------------
def bbsqueeze():
	bollingerlist = []		
	for x in companies:
			currentpricepercentile = []
			company = '{fname}'.format(fname = x)

			technical_indicators = pd.read_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_intraday.csv'.format(fname = x))
			swing = pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))


			swingclose = swing['Close']

			open = technical_indicators['Open']
			high = technical_indicators['High']
			low = technical_indicators['Low']
			close = technical_indicators['Close']
			
			volume = technical_indicators['Volume']
			BBPercentileClose = technical_indicators['Close'].iloc[-1]
			

			#--------------------------------------------PERCENTILE CALCULATIONS START----------------------------------
			percentileclose = swing['Close'].head(-1)
			median = percentileclose.tail(10).median()
			mean = percentileclose.tail(10).mean()
			max =  percentileclose.tail(10).max()
			percentileclose = percentileclose.tail(10).tolist()

			for i in range(1,101):
			
				currentpricepercentile.append(np.percentile(percentileclose, i))

			indexofcurrentpricepercentile = currentpricepercentile.index(closest(currentpricepercentile, BBPercentileClose))
			currentpricepercentileindex = indexofcurrentpricepercentile+1
			#--------------------------------------------PERCENTILE CALCULATIONS ENDS----------------------------------
	
			#--------------------------------------------TOTAL QUANTITY THAT I CAN BUY CALCULATIONS START----------------------------------
			cash = 13000
			price = BBPercentileClose

			canBuy = math.floor(cash/price)
			#--------------------------------------------TOTAL QUANTITY THAT I CAN BUY CALCULATIONS ENDS----------------------------------



			#--------------------------------------------TA-LIB CALCULATIONS START----------------------------------
			#calculating ema values using ta-lib
			
			
			upper, middle, lower = np.array(ta.BBANDS(close, 20, 2, 2, 0))

			swingupper, swingmiddle, swinglower = np.array(ta.BBANDS(close, 20, 2, 2, 0))

			pd.DataFrame(swingupper).to_csv('companies/{fname}/swing trading/{fname}_upperband.csv'.format(fname = x))
			pd.DataFrame(swingmiddle).to_csv('companies/{fname}/swing trading/{fname}_middleband.csv'.format(fname = x))
			pd.DataFrame(swinglower).to_csv('companies/{fname}/swing trading/{fname}_lowerband.csv'.format(fname = x))


			pd.DataFrame(upper).to_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_upperband.csv'.format(fname = x))
			pd.DataFrame(middle).to_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_middleband.csv'.format(fname = x))
			pd.DataFrame(lower).to_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_lowerband.csv'.format(fname = x))


			upperband = pd.read_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_upperband.csv'.format(fname = x))
			upperbandvalue = upperband['0'].tail(5)
			upperbandvalue = upperbandvalue.mean()

			middleband = pd.read_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_middleband.csv'.format(fname = x))
			middlebandvalue = middleband['0'].tail(5)
			middlebandvalue = middlebandvalue.mean()

			lowerband = pd.read_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_lowerband.csv'.format(fname = x))
			lowerbandvalue = lowerband['0'].tail(5)
			lowerbandvalue = lowerbandvalue.mean()
			#--------------------------------------------TA-LIB CALCULATIONS ENDS----------------------------------



			if canBuy>0:
				if((abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)<0.5 and (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)>0.000010):
					BollingerSqueeze = (abs(upperbandvalue-lowerbandvalue)/((upperbandvalue+lowerbandvalue)/2)*100)
					
					mainscore = currentpricepercentileindex*BollingerSqueeze
					

					toappendinbollingersqueeze = (company,mainscore,BollingerSqueeze,currentpricepercentileindex,median,mean,max,BBPercentileClose,canBuy)
					bollingerlist.append(toappendinbollingersqueeze)
					bollingerlist.sort(key = sortSecond, reverse = False)
				
	BollingerObj = pd.DataFrame(bollingerlist, columns = ['Company','Main Score','BollingerSqueeze','Percentile(CPP)','Median','Mean','Max','Close','Capacity']) 
	
	print(BollingerObj)
#--------------------------------------------BOLLINGER BAND SQUEEZE CALCULATIONS ENDS----------------------------------






#--------------------------------------------EVERY COMPANY SWING TRADING CALCULATIONS STARTS----------------------------------

def swingtrading():
	list = []
	total_calls_a_day= 1
	while total_calls_a_day<2:	
		total_calls_a_day+=1
	
		start = datetime.datetime(2010, 1, 1)
		end = datetime.datetime.today()

		# companylist = pd.read_csv('mainCompanylist.csv') #
		companylist = pd.read_csv('mainCompanylist.csv')
		companies = companylist['Symbol']


		for x in companies:
			company = '{fname}'.format(fname = x)
	 
			companyname = web.DataReader('{fname}'.format(fname = x), 'yahoo', start, end)
 
			companyname.to_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))
		

		
#--------------------------------------------EVERY COMPANY SWING TRADING CALCULATIONS ENDS----------------------------------







#--------------------------------------------EVERY COMPANY INTRADAY TRADING CALCULATIONS STARTS----------------------------------

def intraday():
	total_calls_a_day= 1
	while total_calls_a_day<75:	
		total_calls_a_day+=1
	
	
		niftyprice = web.DataReader('^NSEI', 'yahoo', start, end) 
		niftyprice.to_csv('companies/nifty.csv')

		dowJonesprice = web.DataReader('^DJI', 'yahoo', start, end) 
		dowJonesprice.to_csv('companies/dowjones.csv')


		niftyIntrday = yf.download(tickers='^NSEI',period="1d",interval="1m")
		niftyIntrday.to_csv('companies/NSEI_intraday.csv')
		niftyIntrdayValue = pd.read_csv('companies/NSEI_intraday.csv')

		#--------------------------------------------SWING CORRELATIONS WITH NIFTY AND DOW CALCULATIONS STARTS----------------------------------
		correlationlist = []

		nifty = pd.read_csv('companies/nifty.csv')
		niftyClose = nifty['Close'].tail(10)
		
		dow = pd.read_csv('companies/dowjones.csv')
		dowClose = dow['Close'].tail(10)

		dowCloseToday = dow['Close'].iloc[-1]
		dowCloseYesterday = dow['Close'].iloc[-2]

		if (dowCloseToday>dowCloseYesterday):
			DowStatus = "Dow Jones is higher than yesterday"
		else:
			DowStatus = "Dow Jones is lower than yesterday"

		DowToNiftycorr, _ = pearsonr(dowClose, niftyClose)
		
		toappendInCorrelationlist = (DowStatus,DowToNiftycorr)
		correlationlist.append(toappendInCorrelationlist)
		correlationlist.sort(key = sortSecond, reverse = False)
		#--------------------------------------------SWING CORRELATIONS WITH NIFTY AND DOW CALCULATIONS ENDS----------------------------------


		cppstrategylist = []
		percentstrategylist = []
		Intradaycorrelationlist = []

		for x in companies:
			trendlist = []
			currentpricepercentile = []
			list = []
		
			company = '{fname}'.format(fname = x)
		
			# GET INTRADAY DATA
			data = yf.download(tickers=x,period="1d",interval="1m")
			data.to_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_intraday.csv'.format(fname = x))

		 	# GET SWING DATA
			companyname = web.DataReader('{fname}'.format(fname = x), 'yahoo', start, end)
			companyname.to_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))
		

			technical_indicators_intraday = pd.read_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_intraday.csv'.format(fname = x))
			swing = pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))

			open = technical_indicators_intraday['Open']
			high = technical_indicators_intraday['High']
			low = technical_indicators_intraday['Low']
			allclose = technical_indicators_intraday['Close']



			#--------------------------------------------INTRADAY CORRELATIONS CALCULATIONS STARTS----------------------------------
		
		
		

			niftyIntradayClose = niftyIntrdayValue['Close'].tail(15)
			allcloseIntradayCorrelation = technical_indicators_intraday['Close'].tail(15)
	
			CompanycloseforCorrelation = swing['Close'].tail(10)
		

			NiftyToCompanySwingcorr, _ = pearsonr(niftyClose, CompanycloseforCorrelation)
					

			NiftyToCompanyIntradaycorr, _ = pearsonr(niftyIntradayClose, allcloseIntradayCorrelation)
			

		

			#--------------------------------------------INTRADAY CORRELATIONS CALCULATIONS ENDS----------------------------------

	
		


			#--------------------------------------------PERCENT CHANGE FOR PERCENT CHANGE STRATEGY CALCULATIONS STARTS----------------------------------
			yesterdayclose = technical_indicators_intraday['Close'].head(-1)
			yesterdayclose = yesterdayclose.tail(1)
			yesterdayclose = float(yesterdayclose)


	
			close = technical_indicators_intraday['Close'].iloc[-1]
			
			todayclose = float(close)


		
			# percentchange is used in the database down below.
			percentchange = ((todayclose-yesterdayclose)/yesterdayclose)*100
			#--------------------------------------------PERCENT CHANGE FOR PERCENT CHANGE STRATEGY CALCULATIONS STARTS----------------------------------


		
		
		




			#--------------------------------------------CLOSE TO LAST 10 DAYS CALCULATIONS START(SORT OF LIKE PERCENTILE)----------------------------------
			meanclose = technical_indicators_intraday['Close'].head(-1)
			meanclose = meanclose.tail(10)
			meancloseMEAN = meanclose.tail(10).mean()		

			if((abs(meancloseMEAN-close)/((close+meancloseMEAN)/2)*100)<2):
				compareTendays = "close to last (10 days)"
			else:
				compareTendays = "Not close to last (10 days)"
			#--------------------------------------------CLOSE TO LAST 10 DAYS CALCULATIONS START(SORT OF LIKE PERCENTILE)----------------------------------


 
	
		

			#--------------------------------------------PERCENTILE,MEDIAN,MEAN,MAX FOR SWING CALCULATIONS START----------------------------------
			percentileclose = swing['Close'].head(-1)
			median = percentileclose.tail(10).median()
			

			mean = percentileclose.tail(10).mean()
			


			max =  percentileclose.tail(10).max()
			

			percentileclose = percentileclose.tail(10).tolist()

			for i in range(1,101):
				
				currentpricepercentile.append(np.percentile(percentileclose, i))

			indexofcurrentpricepercentile = currentpricepercentile.index(closest(currentpricepercentile, close))
			currentpricepercentileindex = indexofcurrentpricepercentile+1
			
		
			#--------------------------------------------PERCENTILE,MEDIAN,MEAN,MAX FOR SWING CALCULATIONS ENDS----------------------------------





			#--------------------------------------------52 WEEKS HIGH/LOW CALCULATIONS STARTS----------------------------------
	
			maxhigh = swing['Close'].head(-1)
			maxhigh = maxhigh.tail(365)
			maxhighclose = maxhigh.max()


			if((abs(maxhighclose-close)/((close+maxhighclose)/2)*100)>7):
				compareFiftyTwoWeeks = "Far from 52 week high"

			else:
				compareFiftyTwoWeeks = "Near to 52 week high"
			#--------------------------------------------52 WEEKS HIGH/LOW CALCULATIONS ENDS----------------------------------





			#--------------------------------------------MEAN VOLUME CALCULATIONS STARTS----------------------------------
			meanVolume = swing['Volume'].tail(10).mean()
			#--------------------------------------------MEAN VOLUME CALCULATIONS ENDS----------------------------------
		





			#--------------------------------------------TA-LIB CALCULATIONS START----------------------------------
			#calculating rsi values using ta-lib
			rsi_value = np.array(ta.RSI(allclose,14))

			#exporting rsi values to csv file in a specified folder
			pd.DataFrame(rsi_value).to_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_rsi_value.csv'.format(fname = x))

			retrieveRSI = pd.read_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_rsi_value.csv'.format(fname = x))
			retrieve_rsi_value = retrieveRSI['0'].iloc[-1]
			
		



			#calculating ADX values using ta-lib
			adx_value = np.array(ta.ADX(high,low,allclose,14)) 

			pd.DataFrame(adx_value).to_csv("companies/{fname}/intraday trading/percent change strategy/{fname}_adxvalue.csv".format(fname=x))

			retrieveadx = pd.read_csv("companies/{fname}/intraday trading/percent change strategy/{fname}_adxvalue.csv".format(fname=x))
			retrievedAdxvalue = retrieveadx['0'].iloc[-1] 


			#calculating to check ADX values if the last 5 adx values are increasing.
			isadxlistAscending = retrieveadx['0'].tail(5).tolist()

			if [(isadxlistAscending[k+1]-isadxlistAscending[k])>0 for k in range(len(isadxlistAscending)-1)].count(True) == len(isadxlistAscending)-1:
				adxValue = "Adx is increasing"
			else:
				adxValue = "Check Adx yourself"




	
			#calculating ema values using ta-lib
			
			ema_value_5 = ta.EMA(np.array(allclose),5)
			ema_value_8 = ta.EMA(np.array(allclose),8)
			ema_value_13 = ta.EMA(np.array(allclose),13)
			

			#exporting ema values to csv file in a specified folder
			
			pd.DataFrame(ema_value_5).to_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_ema_value_5.csv'.format(fname = x))
			pd.DataFrame(ema_value_8).to_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_ema_value_8.csv'.format(fname = x))
			pd.DataFrame(ema_value_13).to_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_ema_value_13.csv'.format(fname = x))
			
		
			retrieveEma_5 = pd.read_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_ema_value_5.csv'.format(fname = x))
			retrieve_ema_value_5 = retrieveEma_5['0'].iloc[-1]

			retrieveEma_8 = pd.read_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_ema_value_8.csv'.format(fname = x))
			retrieve_ema_value_8 = retrieveEma_8['0'].iloc[-1]
	
			retrieveEma_13 = pd.read_csv('companies/{fname}/intraday trading/percent change strategy/{fname}_ema_value_13.csv'.format(fname = x))
			retrieve_ema_value_13 = retrieveEma_13['0'].iloc[-1]

			if retrieve_ema_value_5 > retrieve_ema_value_8 and retrieve_ema_value_5 > retrieve_ema_value_13 and retrieve_ema_value_8 > retrieve_ema_value_13 :	
				emaValue = "Upward Crossover"
			elif retrieve_ema_value_5 < retrieve_ema_value_8 and retrieve_ema_value_5 < retrieve_ema_value_13 and retrieve_ema_value_8 < retrieve_ema_value_13 :	
				emaValue = "Downward Crossover"
			else:
				emaValue = "Check yourself"
			#--------------------------------------------TA-LIB CALCULATIONS END----------------------------------








			#--------------------------------------------TOTAL QUANTITY THAT I CAN BUY CALCULATIONS START----------------------------------
			cash = 13000
			price = close

			canBuy = math.floor(cash/price)
			
			#--------------------------------------------TOTAL QUANTITY THAT I CAN BUY CALCULATIONS ENDS----------------------------------







			#--------------------------------------------INSERT AND RETREIVE FROM DATABASE OF EVERY COMPANY CALCULATIONS STARTS----------------------------------
			sql = "INSERT INTO `"+ '{fname}_percentstrategy'.format(fname = x) + "` (ticker, percentchange) VALUES (%s, %s)"
			val = (company , percentchange)
			mycursor.execute(sql, val)

			mydb.commit()
			
			mycursor.execute("SELECT percentchange FROM `"+ '{fname}_percentstrategy'.format(fname = x) + "`")
			table_rows = mycursor.fetchall()
		
			total = 0
			for [z] in table_rows:
			
				list.append(z)
				trend = [b - a for a, b in zip(list[::1], list[1::1])]

			
			for ele in range(0, len(trend)): 
    				total = total + trend[ele]

			mycursor.execute("TRUNCATE TABLE `"+ '{fname}_totalper'.format(fname = x) + "`")
		
			sql = "INSERT INTO `"+ '{fname}_totalper'.format(fname = x) + "` (ticker, totalpercent) VALUES (%s, %s)"
			val = (company , total)
			mycursor.execute(sql, val)
		
			mycursor.execute("SELECT totalpercent FROM `"+ '{fname}_totalper'.format(fname = x) + "`")
			table_rows = mycursor.fetchall()
			#--------------------------------------------INSERT AND RETREIVE FROM DATABASE OF EVERY COMPANY CALCULATIONS ENDS----------------------------------




		
			#--------------------------------------------TEN MINUTE AND FULL DAY TREND CALCULATIONS START----------------------------------
			TenMinuteTrend = technical_indicators_intraday['Close'].tail(10)
			trendlist = TenMinuteTrend.tolist()

			y = trendlist
			x = range(1,len(y)+1)

			tenMinuteBetaValue = beta(x,y)
		
		

			FullDayTrend = technical_indicators_intraday['Close']
			trendlist = FullDayTrend.tolist()

			y = trendlist
			x = range(1,len(y)+1)
			FullDayBetaValue = beta(x,y)
			


			MainScore = canBuy*(tenMinuteBetaValue)
			

			#--------------------------------------------TEN MINUTE AND FULL DAY TREND CALCULATIONS ENDS----------------------------------





		

			#--------------------------------------------MINIMUM PRICE TO BE SOLD CALCULATIONS START----------------------------------

			brokerage = (close*canBuy)*(0.05/100)*(2)
			if (brokerage<20):
				brokerageAmount = brokerage
			else:
				brokerageAmount = 20

		
			MinPriceSold = close+10

			#--------------------------------------------MINIMUM PRICE TO BE SOLD CALCULATIONS END-----------------------------------



			

			
			for [a] in table_rows: # we can add a, meanVolume,compareTendays,FullDayBetaValue which i removed
	
				if canBuy>0:
					toappendIncppstrategylist = (company,currentpricepercentileindex,median,mean,max,canBuy,close,MinPriceSold,emaValue,adxValue,retrieve_rsi_value)
					cppstrategylist.append(toappendIncppstrategylist)
					cppstrategylist.sort(key = sortSecond, reverse = False)

					toappendInpercentstrategylist = (company,MainScore,currentpricepercentileindex,canBuy,close,MinPriceSold,FullDayBetaValue,emaValue,adxValue,retrieve_rsi_value)
					percentstrategylist.append(toappendInpercentstrategylist)
					percentstrategylist.sort(key = sortSecond, reverse = True)	

				
					toappendInIntradayCorrelationlist = (company,NiftyToCompanySwingcorr,NiftyToCompanyIntradaycorr)
					Intradaycorrelationlist.append(toappendInIntradayCorrelationlist)
					Intradaycorrelationlist.sort(key = sortSecond, reverse = True)

					
	
		
		pd.set_option('display.max_rows', None)
		print('----------------------------------------------------------------PERCENT CHANGE STRATEGY----------------------------------------------------------------')
		PercentChangeStrategy = pd.DataFrame(percentstrategylist, columns = ['Company','MainScore','Percentile(CPP)','Capacity','Close','MinPriceToSell','Trend FullDay','Ema Crossover','Adx','RSI']) 
		
		print(PercentChangeStrategy)

		print('-------------------------------------------------------INDEX CORRELATIONS-------------------------------------------------------')
		DowNiftyDataframe = pd.DataFrame(correlationlist, columns = ['Dow status','Dow-Nifty Correlation']) 
		print(DowNiftyDataframe)

		print('-------------------------------------------------------COMPANY CORRELATIONS-------------------------------------------------------')
		NiftyAndCompanyDataframe = pd.DataFrame(Intradaycorrelationlist, columns = ['Company','Swing Correlation','Intraday Correlation']) 
		
		print(NiftyAndCompanyDataframe)

		# CPP stands for current price percentile
		print('----------------------------------------------------------------------CPP STRATEGY-------------------------------------------------------------------------------------')
		CPPstrategy = pd.DataFrame(cppstrategylist, columns = ['Company','Percentile(CPP)','Median','Mean','Max','Capacity','Close','MinPriceToSell','Ema Crossover','Adx','RSI']) 
		
		print(CPPstrategy)


		print('-------------------------------------------------------BBSQUEEZE STRATEGY-------------------------------------------------------')
		bbsqueeze()

		time.sleep(600)

#--------------------------------------------EVERY COMPANY INTRADAY TRADING CALCULATIONS ENDS----------------------------------




if __name__ == '__main__':
	swingtrading()
	intraday()
		





	