import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
host = "localhost",
user="root",
passwd="",
database="companies"
)

mycursor = mydb.cursor()

# company = pd.read_csv("NIFTY50.csv")

company = pd.read_csv('mainCompanylist.csv')
# company = pd.read_csv("500companies.csv")
companieslist = company['Symbol'] # column heading 

counter = 0
for x in companieslist:
	counter +=1
	
	mycursor.execute("TRUNCATE TABLE  `"+ '{fname}_percentstrategy'.format(fname = x) + "`")
	mycursor.execute("TRUNCATE TABLE  `"+ '{fname}_totalper'.format(fname = x) + "`")
	# mycursor.execute("CREATE TABLE IF NOT EXISTS `"+ '{fname}_intraday_yfinance_module_technical_value'.format(fname = x) + "` (ticker VARCHAR(255), emacrossover VARCHAR(255), adxvalue VARCHAR(255), rsivalue VARCHAR(255) )")

	# mycursor.execute("CREATE TABLE IF NOT EXISTS `"+ '{fname}_totalper'.format(fname = x) + "` (ticker VARCHAR(255),  totalpercent FLOAT )")
	# mycursor.execute("CREATE TABLE IF NOT EXISTS `"+ '{fname}_percentstrategy'.format(fname = x) + "` (ticker VARCHAR(255),  percentchange FLOAT )")

	mydb.commit()
	
	print(counter, mycursor.rowcount, "record inserted")