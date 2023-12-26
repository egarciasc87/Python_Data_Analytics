#%matplotlib inline

import numpy as np
import pandas as pd
import scipy.stats as sc_stats
import matplotlib.pyplot as plt
import math


#statement: Card usage has been improved 
#   from last year usage which was 50
def test_hypothesis_1(data):
    #null hypothesis: average = 50
    #alternative hypothesis: average > 50
    df = pd.DataFrame(data)

    expected_mean = 50
    confidence_level = 0.95
    significance_level = (1 - confidence_level)   
    sample_average = df.Latest_mon_usage.mean()
    print(df.columns)

    print("\nStatistics for 'Latest_mon_usage'")
    print("mean: ", sample_average)
    print("std: ", df.Latest_mon_usage.std())
    print("expected mean: ", expected_mean)
    print("significance level: ", significance_level)

    stats_, p_value = sc_stats.ttest_1samp(a=df.Latest_mon_usage,
                                           popmean=50)
    print("p-value: ", p_value)

    if sample_average > expected_mean and p_value < significance_level:
        print("\nReject null hypothesis")
    else:
        print("\nFail to reject null hypothesis")


#statement: The last campaign was successful 
#   in terms of credit card.
def test_hypothesis_2(data):
    #null hypothesis: pre_avg = post_avg
    #alternative_hypothesis: pre_avg < post_avg
    df = pd.DataFrame(data)
    print(df.columns)

    confidence_level = 0.95
    significance_level = (1-confidence_level)
    pre_usage_avg = df.pre_usage.mean()
    post_usage_1month_avg = df.Post_usage_1month.mean()
    post_usage_2month_avg = df.post_usage_2ndmonth.mean()

    print("\nStatistics for 'pre_usage' and 'post_usage'")
    print("pre_usage_avg: ", pre_usage_avg)
    print("post_usage_1month_avg: ", post_usage_1month_avg)
    print("post_usage_2month_avg: ", post_usage_2month_avg)

    stats_, p_value = sc_stats.ttest_rel(a=df.pre_usage,
                                         b=df.Post_usage_1month)
    
    print("p-value: ", p_value)
    
    if pre_usage_avg < post_usage_1month_avg and p_value < significance_level:
        print("\nReject null hypothesis")
    else:
        print("\nFail to reject null hypothesis")


#statement: Is there any differce in credit card spend
#   usage between males and females?
def test_hypothesis_3(data):
    #null hypothesis: male_avg = female_avg
    #alternative_hypothesis: male_avg != female_avg
    df = pd.DataFrame(data)
    print(df.columns)

    male_spend = df.Post_usage_1month[df.sex == 0]
    female_spend = df.Post_usage_1month[df.sex == 1]
    print(male_spend)
    print(female_spend)

    p_value = 0
    confidence_level = 0.95
    significance_level = (1-confidence_level)
    male_avg = male_spend.mean()
    male_std = male_spend.std()
    female_avg = female_spend.mean()
    female_std = female_spend.std()

    print("\nStatistics for male and female spend")
    print("male avg: ", male_avg)
    print("female avg: ", female_avg)
    print("significance level: ", significance_level)

    stats_, p_value = sc_stats.ttest_ind(a=male_spend,
                                         b=female_spend,
                                         equal_var=False)    
    print("p-value (t-test): ", p_value)

    if p_value < significance_level:
        print("Reject null hypothesis using t-test")
    else:
        print("Fail to reject null hypothesis using t-test")

    stats_, p_value = sc_stats.f_oneway(male_spend,
                                        female_spend)
    print("\np-value (ANOVA): ", p_value)

    if p_value < significance_level:
        print("Reject null hypothesis using ANOVA")
    else:
        print("Fail to reject null hypothesis using ANOVA")


#statement: Is there any difference in credit card 
#   spend between segments?
def test_hypothesis_4(data):
    #null hypothesis: seg1_avg = seg2_avg
    #alternative hypothesis: seg1_avg != seg2_avg
    df = pd.DataFrame(data)
    print(df.columns)

    print(df["segment"].value_counts())
    print(df["segment"].describe())

    df_seg1 = df.Latest_mon_usage[df.segment == 1]
    df_seg2 = df.Latest_mon_usage[df.segment == 2]
    df_seg3 = df.Latest_mon_usage[df.segment == 3]
    total_avg = df.Latest_mon_usage.mean()
    seg1_avg = df_seg1.mean()
    seg2_avg = df_seg2.mean()
    seg3_avg = df_seg3.mean()

    confidence_level = 0.95
    significance_level = (1-confidence_level)
    p_value = 0

    ststs_, p_value = sc_stats.f_oneway(df_seg1,
                                        df_seg2,
                                        df_seg3)
    print("\nStatistics for segments analysis")
    print("significance level: ", significance_level)
    print("total avg: ", total_avg)
    print("segment 1 avg: ", seg1_avg)
    print("segment 2 avg: ", seg2_avg)
    print("segment 3 avg: ", seg3_avg)
    print("p-value: ", p_value)

    if (p_value < significance_level):
        print("\nReject null hypothesis")
    else:
        print("\nFail to reject null hypothesis")


#statement: Is there any relationship between region and segment?
def test_hypothesis_5(data):
    #null hypothesis: there is no relationship
    #alternative hypothesis: there is a relationshipo
    df = pd.DataFrame(data)
    print(df.columns)

    confidence_level = 0.95
    significance_level = (1-confidence_level)
    p_value = 0

    df = pd.crosstab(df.segment,
                     df.region,
                     margins=True)
    print(df)
    
    stats_, p_value, df, expected_freq = sc_stats.chi2_contingency(
        observed=df)
    print("\nStatistics for segment vs region")
    print("significance level: ", significance_level)
    print("p-value: ", p_value)
    print("degree of freedom: ", df)
    print("expected frequency: ", expected_freq)


#1. get data and perform exploratory analysis
data = pd.read_csv("cust_seg.csv")
print(data)
print(data.describe())
#print(data.columns)
#print(data.describe())
#print(data.isnull().sum())
#print(data.info())

#test_hypothesis_1(data)
#test_hypothesis_2(data)
#test_hypothesis_3(data)
#test_hypothesis_4(data)
test_hypothesis_5(data)



