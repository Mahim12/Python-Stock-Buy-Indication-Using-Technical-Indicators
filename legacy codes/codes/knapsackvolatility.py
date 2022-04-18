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
import knapsack
import pprint


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="hybridtactics"
)

mycursor = mydb.cursor()

# Python3 code for Dynamic Programming 
# based solution for 0-1 Knapsack problem 
  
# Prints the items which are put in a  
# knapsack of capacity W 
def knapSack(W, wt, val, n):
    itemlist = list()
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('root', '', 'localhost', 'hybridtactics'))
    K = [[0 for w in range(W + 1)] 
            for i in range(n + 1)] 
              
    # Build table K[][] in bottom 
    # up manner 
    for i in range(n + 1): 
        for w in range(W + 1): 
            if i == 0 or w == 0: 
                K[i][w] = 0
            elif wt[i - 1] <= w: 
                K[i][w] = max(val[i - 1]  
                  + K[i - 1][w - wt[i - 1]], 
                               K[i - 1][w]) 
            else: 
                K[i][w] = K[i - 1][w] 
  
    # stores the result of Knapsack 
    res = K[n][W] 
    print(res) 
      
    w = W 
    for i in range(n, 0, -1): 
        if res <= 0: 
            break
        # either the result comes from the 
        # top (K[i-1][w]) or from (val[i-1] 
        # + K[i-1] [w-wt[i-1]]) as in Knapsack 
        # table. If it comes from the latter 
        # one/ it means the item is included. 
        if res == K[i - 1][w]: 
            continue
        else: 
            # This item is included. 
            print(wt[i - 1]) 
            on = (wt[i - 1])
            itemlist.append(on)
            swingObj = pd.DataFrame(itemlist, columns = ['Price']) 
            swingObj.to_sql(con=database_connection, name='items', if_exists='replace')  
           
            # Since this weight is included 
            # its value is deducted 
            res = res - val[i - 1] 
            w = w - wt[i - 1] 
           
  
  



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





def swingtrading():
	val = list()
	wt = list()
	main = list()
	intraday_list = list()
	companylist = list()
	knapsacklist = list()
	for c in companies:
		
		company = '{fname}'.format(fname = c)

		df = pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = c))
		
		open = df['Open'].tail(percentiledays).mean()
		high = df['High'].tail(percentiledays).mean()
		low = df['Low'].tail(percentiledays).mean()
		yesterdayClose = df['Close'].head(-1).tail(percentiledays).mean()

		yesterdayClose2Low = (abs(yesterdayClose-low)/((yesterdayClose+low)/2)*100)
		yesterdayClose2Open = (abs(yesterdayClose-open)/((yesterdayClose+open)/2)*100)
		open2High = (abs(high-open)/((high+open)/2)*100)
		high2Low = (abs(high-low)/((high+low)/2)*100)



		#perimeter = yesterdayClose2Low+yesterdayClose2Open+open2High+high2Low
		perimeter = high2Low
		perimeter = int(perimeter) 
		latestClose = df ['Close'].iloc[-1]
		mainClose = df ['Close'].iloc[-1]
		latestClose = int(latestClose) 

		vallist = (perimeter)
		val.append(vallist)

		wtlist = (latestClose)
		wt.append(wtlist)

		mainlist = (company,latestClose,mainClose)
		main.append(mainlist)


	  
	# Driver program to test above function 
	W = 3000
	n = len(val)
	#print(knapSack(W, wt, val, n)) 

		
	mycursor.execute("SELECT Price FROM `items`")
	table_rows = mycursor.fetchall()
		

	for [z] in table_rows:	
		intraday_list.append(z)

	for c in companies:
		df = pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = c))

		latestClose = df ['Close'].iloc[-1]
		latestClose = int(latestClose) 
		company = '{fname}'.format(fname = c)

		for x in intraday_list: 
			if x == latestClose:
				companylist.append(company)
				companylist = list(dict.fromkeys(companylist)) #remove duplicate values from the list.

	
	for c in companylist:
		df = pd.read_csv('companies/{fname}/swing trading/{fname}.csv'.format(fname = c))
		latestClose = df ['Close'].iloc[-1]
		company = '{fname}'.format(fname = c)

		n = (company,latestClose)
		knapsacklist.append(n)
			
	knapObj = pd.DataFrame(knapsacklist, columns = ['Company','Price']) 
		
	print(knapObj)	


if __name__ == '__main__':
	swingtrading()
	
	
	