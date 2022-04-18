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
import yfinance as yf
import mysql.connector
import time
import talib as ta
import numpy as np
import math
from scipy.stats import pearsonr
import pandas_datareader as web
import os
import datetime
from pandas.io import sql
import sqlalchemy

import swingtrading
import multiprocess


#For sorting a list.
def sortSecond(val): 
    return val[1] 

#companylist = pd.read_csv('NIFTY50.csv')
companylist = pd.read_csv('mainCompanylist.csv')
companies = companylist['Symbol']


intradayallowedlist = pd.read_csv('intradayallowed.csv')
intradayallowed = intradayallowedlist['Allowed'].tolist()

def data():
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


		niftyIntrday = yf.download(tickers='^NSEI',period="1d",interval="1m")
		niftyIntrday.to_csv('companies/NSEI_intraday.csv')

		for x in companies:
			company = '{fname}'.format(fname = x)
			companyname = web.DataReader('{fname}'.format(fname = x), 'yahoo', start, end)
			companyname.to_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = x))

			print(company)
		




def gaptrade():
	gaplowlist = list()
	gapuplist = list()

	database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('root', '', 'localhost', 'hybridtactics'))

	for c in companies:
		
		company = '{fname}'.format(fname = c)

		df = pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = c))
	
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



if __name__ == '__main__':
	#data()
	#gaptrade()
	#swingtrading.swingtrading()
	#swingtrading.meanreversion()
	#swingtrading.bbswingsqueeze()
	p1 = Process(target=multiprocess.ParsePrice)
	p1.start()
	p2 = Process(target=multiprocess.intraday)
	p2.start()
	
	
	
	