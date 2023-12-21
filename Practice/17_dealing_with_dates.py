import numpy as np
import pandas as pd


#1. get raw date
file_name = "dates_lesson_16.csv"
data = pd.read_csv(file_name)
#print(data.head())
#print(data.isnull().sum())
#print(data.info())


#2. clean & format data
#covert one column into datetime format
cols = data.columns
data["month_day_year"] = pd.to_datetime(data["month_day_year"])
print(data.head())

#conver whole dataframe into datetime format
data = pd.read_csv(file_name,
                   parse_dates=[0, 1, 2, 3])
print(data.head())
print(data.info())

for col in data:
    print("data type -> ", type(data[col][1]))

odd_date = "12:30:15 2015-29-11"
print("date -> ", pd.to_datetime(odd_date,
                     format="%H:%M:%S %Y-%d-%m"))

#get all rows from column month_day_year
column_1 = data["month_day_year"]
print(column_1)

#get all rows from columns 1,2
column_1 = data.iloc[:,0:2]
print(column_1)

#data_df = pd.DataFrame({'year': column_1.dt.year})
column_1["year"] = column_1["month_day_year"].dt.year
column_1["month"] = column_1["month_day_year"].dt.month
column_1["day"] = column_1["month_day_year"].dt.day
column_1["day_of_week"] = column_1["month_day_year"].dt.day_of_week
column_1["quarter"] = column_1["month_day_year"].dt.quarter
print(column_1)


