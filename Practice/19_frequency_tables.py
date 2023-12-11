import numpy as np
import pandas as pd


#1. get raw data
data = pd.read_csv("Titanic-Dataset.csv")
print(data)

char_cabin = data["Cabin"].astype(str)
new_cabin = np.array([cabin[0] for cabin in char_cabin])
print(new_cabin)

data["Cabin"] = pd.Categorical(new_cabin)
print(data)


#2. one-way tables
tab_survided = pd.crosstab(index=data["Survived"],
                     columns="count")
print(tab_survided)
#print(type(tab_survided))

tab_pclass = pd.crosstab(index=data["Pclass"],
                         columns="count")
print(tab_pclass)

tab_cabin = pd.crosstab(index=data["Cabin"],
                        columns="count")
print(tab_cabin)

tab_sex = pd.crosstab(index=data["Sex"],
                      columns="count")
print(tab_sex)

tab_sex = data.Sex.value_counts()
print(tab_sex)

tab_sex = data.groupby("Sex")["Pclass"].count().reset_index()
tab_sex.columns = ["Sex", "Total"]
print(tab_sex)
#print(tab_sex.sum())
#print(tab_sex.shape())


#3. two-way tables
data_survived_by_sex = pd.crosstab(index=data["Survived"],
                                   columns=data["Sex"])
data_survived_by_sex.index = ["died", "survived"]
print(data_survived_by_sex)

data_survived_by_class = pd.crosstab(index=data["Survived"],
                                     columns=data["Pclass"],
                                     margins=True)
data_survived_by_class.index = ["died", "survived", "people_total"]
data_survived_by_class.columns = ["class1", "class2", "class3", "class_total"]
print(data_survived_by_class)

data_percentage_survival = (data_survived_by_class/data_survived_by_class.loc["people_total", "class_total"]) * 100
data_percentage_survival = data_percentage_survival.round(2)
data_percentage_survival.index = ["died %", "survived %", "people_total %"]
data_percentage_survival.columns = ["class1 %", "class2 %", "class3 %", "class_total %"]
print(data_percentage_survival)


#4. hugher dimensional tables
data_survival_by_sex_class = pd.crosstab(index=data["Survived"],
                                         columns=[data["Pclass"], data["Sex"]],
                                         margins=True)
print(data_survival_by_sex_class)

data_percentage_survival = data_survival_by_sex_class/data_survival_by_sex_class.loc["All"]
data_percentage_survival = data_percentage_survival * 100
print(data_percentage_survival)



