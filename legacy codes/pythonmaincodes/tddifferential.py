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

def minimum(a, b): 
      
    if a <= b: 
        return a 
    else: 
        return b 


def maximum(a, b): 
      
    if a <= b: 
        return b 
    else: 
        return a 




BuyCloseList = list()
SellCloseList = list()
intraday_list = []



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="hybridtactics"
)

mycursor = mydb.cursor()



companylist = pd.read_csv('mainCompanylist.csv')
companies = companylist['Symbol']




for c in companies:
	company = '{fname}'.format(fname = c)
	df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = c))
	fullClose = df['Close']
	
	currLow = df['Low'].iloc[-1]
	prevLow = df['Low'].iloc[-2]
	priorLow = df['Low'].iloc[-3]

	trueLow = minimum(currLow,prevLow)
	prevTrueLow =  minimum(prevLow,priorLow)

	currHigh = df['Low'].iloc[-1]
	prevHigh = df['Low'].iloc[-2]
	priorHigh = df['Low'].iloc[-3]

	trueHigh = maximum(currHigh,prevHigh)
	prevTrueHigh =  minimum(prevHigh,priorHigh)
	
	currClose = df['Close'].iloc[-1]
	prevClose = df['Close'].iloc[-2]
	priorClose = df['Close'].iloc[-3]
	
	buyPressure = currClose-trueLow 
	prevbuyPressure = prevClose-prevTrueLow 

	sellPressure = currClose-trueHigh 
	prevsellPressure = prevClose-prevTrueHigh 

	if buyPressure>prevbuyPressure:
		if priorClose> prevClose and priorClose> currClose:
			toappend = (company,currClose,"Buy")
			BuyCloseList.append(toappend)
	elif sellPressure>prevsellPressure:
		if priorClose< prevClose and priorClose< currClose:
			toappend = (company,currClose,"Sell")
			BuyCloseList.append(toappend)
				

	'''
	plt.figure(figsize=(8,6))
	plt.plot(fullClose)
	plt.plot(BuyCloseList,marker=".",markersize=40, color='g')
	plt.plot(SellCloseList,marker=".",markersize=40, color='r')
	plt.title(company)
	plt.show()

	'''	


	
pd.set_option('display.max_rows', None)	

print('-------------------------------------------------------BOLINGER-MID-CROSSOVER STRATEGY-------------------------------------------------------')			
Bollinger2Obj = pd.DataFrame(BuyCloseList, columns = ['Company','Close','Do']) 
print(Bollinger2Obj)
