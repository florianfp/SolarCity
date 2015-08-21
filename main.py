#%%
import pandas as pd
import datetime as dt
import time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime as dt
sns.set_style("darkgrid")

#%%Parameters
energy_capacity = pd.read_excel('Battery_degradation.xlsx', sheetname='Retention')
energy_capacity = energy_capacity/10 #fron 10kWh Tesla battery to 1MWh 
energy_to_charge = pd.read_excel('Battery_degradation.xlsx', sheetname='Energy_required')
energy_to_charge = energy_to_charge/10
capacity = energy_capacity
threshold = 159
start_time_threshold = dt.time(hour=0)
end_time_threshold = dt.time(hour=23, minute=59)
cycle = 50
node_id=1

#%%Strategy1+
threshold = 159 #to account for battery degradation add +50
#cycle = 50 #to account for battery degradation
startDemandLogic = dt.time(hour=3)
endDemandLogic = dt.time(hour=6)
node_id=1

results=pd.DataFrame()
strats=pd.DataFrame()
for year, year_index in [[2012,1],[2013,2],[2014,3]]:
    raw = pd.DataFrame()
    for month in range(1,13):
        temp = pd.read_excel('VACA_'+str(year)+'_'+str(month)+'.xlsx')
        raw = pd.concat([raw, temp])
    data = clean_data(raw)
    result, strat, subset = new_strategy(data, threshold, startDemandLogic, endDemandLogic, capacity[year_index][cycle], energy_to_charge[year_index][cycle])
    result['Year']=year
    result['Node']=node_id
    results = pd.concat([results, result])  
    strats = pd.concat([strats, strat])
#results.to_excel('Node1_results_with_degradation.xlsx')
#strats.to_excel('Node1_strats_with_degradation.xlsx')

#%%
strats=pd.DataFrame()
battery_energy = 2
year = 2014
node_id=1
raw = pd.DataFrame()
for month in range(1,13):
    temp = pd.read_excel('Node1_'+str(year)+'_'+str(month)+'.xlsx')
    raw = pd.concat([raw, temp])
data = clean_data(raw)
result, strat, subset = new_strategy(data, threshold, startDemandLogic, endDemandLogic, capacity)
result['Year']=year
result['Node']=node_id
results = pd.concat([results, result])  
strats = pd.concat([strats, strat])
    
#%%
#let's determine how important congestion pricing is
stratTotal = pd.merge(strat, congestion, on=['StartDateTime', 'StartTime', 'StartDate'], suffixes=('_total', '_congestion'))
stratTotal.to_excel('stratTotal.xlsx')
stratTotal['Price_congestion'].sum() / stratTotal['Price_total'].sum()


#%%
event_per_day = pd.DataFrame()
for threshold in range(0,100,5):
    new_row = pd.DataFrame([[threshold, (strat.groupby(by='StartDate')['StartDate'].count()>threshold).count()]])
    event_per_day = pd.concat([event_per_day, new_row])
event_per_day.columns = ['Threshold','Number_of_days']

#looking at the days where a lot of events happen
(strat.groupby(by='StartDate')['StartDate'].count()>10).sum()
day1 = strat[strat['StartDate']==dt.date(2014,3,15)]
day1.to_excel('2014-03-15.xlsx')

day2 = strat[strat['StartDate']==dt.date(2014,5,9)]
day2.to_excel('2014-05-09.xlsx')

day3 = strat[strat['StartDate']==dt.date(2014,5,10)]
day3.to_excel('2014-05-10.xlsx')


#%%Strategy 2
threshold = 150
start_time_threshold = dt.time(hour=7)
end_time_threshold = dt.time(hour=10)

result, strat, subset = strategy(data, threshold, start_time_threshold, end_time_threshold, capacity)
#explore_strategy(data, start_time_threshold, end_time_threshold, capacity, weekend=False)

#%%Strategy 3
threshold = 150
start_time_threshold = dt.time(hour=9)
end_time_threshold = dt.time(hour=10)

result, strat, subset = strategy(data, threshold, start_time_threshold, end_time_threshold, capacity)
#explore_strategy(data, start_time_threshold, end_time_threshold, capacity, weekend=False)


#%%
quantile_99 = data['MW'].quantile(q=0.99)
plt.hist(data[data['MW']>150]['MW'].values, bins=100)
plt.xlabel('Prices')
plt.ylabel('Number of occurences in 2014')