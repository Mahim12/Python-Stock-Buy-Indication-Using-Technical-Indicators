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


def Diff(firstextraction, passedon):
    return (list(list(set(firstextraction)-set(passedon)) + list(set(passedon)-set(firstextraction))))


	
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
			print("First is", firstextraction)
			list_difference = [item for item in firstextraction if item not in passedon]
			print("Difference is", Diff(firstextraction, passedon))

			moneyControlObj = pd.DataFrame(Diff(firstextraction, passedon), columns = ['Company']) 
			moneyControlObj.to_sql(con=database_connection, name='moneycontrol', if_exists='replace')
			
			passedon = firstextraction
	
			time.sleep(120)


		firstextraction.clear() 
		passedon.clear()	
		time.sleep(480)
			

if __name__ == '__main__':
	ParsePrice()
	 


