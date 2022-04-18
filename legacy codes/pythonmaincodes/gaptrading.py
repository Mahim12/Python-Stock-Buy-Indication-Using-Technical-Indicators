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


companylist = pd.read_csv('mainCompanylist.csv')
companies = companylist['Symbol']


intradayallowedlist = pd.read_csv('intradayallowed.csv')
intradayallowed = intradayallowedlist['Allowed'].tolist()

		
'''
def data():
	list = []
	res = {}
	mainChunk = []
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
			mainChunk.append(x)
			

		n = 10 #Break the mainChunk list into 10 smaller chunks of list
		final = [mainChunk[i * n:(i + 1) * n] for i in range((len(mainChunk) + n - 1) // n )]  
		#print (final) 

		for x in range(0,9):
			res[x] = [i[x] for i in final] 
			


		for (comp0,comp1,comp2,comp3,comp4,comp5,comp6,comp7,comp8) in zip(res[0],res[1],res[2],res[3],res[4],res[5],res[6],res[7],res[8]):
			company0 = '{fname}'.format(fname = comp0)
			companyname0 = web.DataReader('{fname}'.format(fname = comp0), 'yahoo', start, end)
			companyname0.to_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = comp0))

			company1 = '{fname}'.format(fname = comp1)
			companyname1 = web.DataReader('{fname}'.format(fname = comp1), 'yahoo', start, end)
			companyname1.to_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = comp1))

			company2 = '{fname}'.format(fname = comp2)
			companyname2 = web.DataReader('{fname}'.format(fname = comp2), 'yahoo', start, end)
			companyname2.to_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = comp2))

			company3 = '{fname}'.format(fname = comp3)
			companyname3 = web.DataReader('{fname}'.format(fname = comp3), 'yahoo', start, end)
			companyname3.to_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = comp3))

			company4 = '{fname}'.format(fname = comp4)
			companyname4 = web.DataReader('{fname}'.format(fname = comp4), 'yahoo', start, end)
			companyname4.to_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = comp4))

			company5 = '{fname}'.format(fname = comp5)
			companyname5 = web.DataReader('{fname}'.format(fname = comp5), 'yahoo', start, end)
			companyname5.to_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = comp5))

			company6 = '{fname}'.format(fname = comp6)
			companyname6 = web.DataReader('{fname}'.format(fname = comp6), 'yahoo', start, end)
			companyname6.to_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = comp6))

			company7 = '{fname}'.format(fname = comp7)
			companyname7 = web.DataReader('{fname}'.format(fname = comp7), 'yahoo', start, end)
			companyname7.to_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = comp7))

			company8 = '{fname}'.format(fname = comp8)
			companyname8 = web.DataReader('{fname}'.format(fname = comp8), 'yahoo', start, end)
			companyname8.to_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = comp8))


			print(company0)
			print(company1)
			print(company2)
			print(company3)
			print(company4)
			print(company5)
			print(company6)
			print(company7)
			print(company8)			






'''
def data():
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


def gaptrade():
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



if __name__ == '__main__':
	data()
	gaptrade()
	#swingtrading.meanreversion()
	#swingtrading.swingtrading()
	#p1 = Process(target=multiprocess.ParsePrice)
	#p1.start()
	#p2 = Process(target=multiprocess.intraday)
	#p2.start()
	
	
	
	