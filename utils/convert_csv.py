import os
import datetime
import csv, sqlite3

con = sqlite3.connect('../config/app.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS metrics (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, channel, country, os, impressions, clicks, installs, spend, revenue);") # use your column names here

with open('../dataset.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(datetime.datetime.strptime(i['date'], '%m/%d/%Y').strftime('%m-%d-%Y'), i['channel'], i['country'], i['os'], i['impressions'], i['clicks'], i['installs'], i['spend'], i['revenue']) for i in dr]

cur.executemany("INSERT INTO metrics (date, channel, country, os, impressions, clicks, installs, spend, revenue) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)", to_db)
con.commit()
con.close()