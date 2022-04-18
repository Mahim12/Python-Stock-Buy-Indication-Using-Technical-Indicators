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


#For sorting a list.
def sortSecond(val): 
    return val[1] 


#companylist = pd.read_csv('strategies\Midtouch\midtouch.csv')
#companies = companylist['Company']

companylist = pd.read_csv('mainCompanylist.csv')
companies = companylist['Symbol']

list = list()

for c in companies:
		
	company = '{fname}'.format(fname = c)

	df = pd.read_csv('newcompanylist/{fname}/swing trading/{fname}.csv'.format(fname = c))

	prevLow = df['Low'].iloc[-2]
	currLow = df['Low'].iloc[-1]	

	prevHigh = df['High'].iloc[-2]
	currHigh = df['High'].iloc[-1]

	prevClose = df['Close'].iloc[-2]
	currClose = df['Close'].iloc[-1]

	x = df['Close'].tail(3).tolist()
	y = range(len(x))
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	slope = float(slope)
		
	#score = currClose - prevClose 
	vol = ((currClose-prevClose)/((currClose+prevClose)/2)*100)
	canBuy = math.floor(2500/currClose)
	mainNumber = currClose*canBuy 
	score = vol/mainNumber
	 

	highScore = currHigh - prevHigh
	LowScore = currLow - prevLow

	if score<0:
		if slope<0:
			if currClose<2500:
				app = (company,score,currClose)
				list.append(app)
				list.sort(key = sortSecond, reverse = True)

	
	

pd.set_option('display.max_rows', None)
print('-------------------------------------------------------Current Top gainer Strategy-------------------------------------------------------')
lowObj = pd.DataFrame(list, columns = ['Company','Score','Price']) 
print(lowObj)		


