import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


#1. get raw data
file_name = "22_billionaires_stats.csv"
data = pd.read_csv(file_name)
print(data.isnull().sum())
print(data.columns)
data = data.drop(columns=["population_country", "latitude_country", "longitude_country", "life_expectancy_country", "tax_revenue_country_country", "total_tax_rate_country", "gross_tertiary_education_enrollment", "gross_primary_education_enrollment_country"])
print(data[["finalWorth", "personName", "country", "industries", "category"]])


#2. analysis
print(data["selfMade"].value_counts())

