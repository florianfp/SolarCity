def clean_data(data):
    data = data[['INTERVALSTARTTIME_GMT', 'XML_DATA_ITEM', 'MW']]
    data.columns = ['StartTime', 'Type', 'Price']
    data = data[data['Type']=='LMP_PRC']
    data = data.groupby(by='StartTime', as_index=False).sum()
    data['StartDateTime'] = map(lambda x: x[0:len(x)-6], data['StartTime'])
    data['StartDateTime'] = map(lambda x: time.strptime(x, '%Y-%m-%dT%H:%M:%S'), data['StartDateTime'])
    data['StartDateTime'] = map(lambda x: dt.datetime(x.tm_year, x.tm_mon, x.tm_mday, x.tm_hour, x.tm_min), data['StartDateTime'])
    data['StartDateTime'] = map(lambda x: x-dt.timedelta(hours=7), data['StartDateTime'])
    data['StartTime'] = map(lambda x: x.time(),data['StartDateTime'])
    data['StartDate'] = map(lambda x: x.date(), data['StartDateTime'])
    #data['Cost'] = map(lambda x: time_to_pge_price(x, x.time()), data['StartDateTime'])
    return data
    
def new_strategy(data, threshold, startDemandLogic, endDemandLogic, capacity, energy_to_charge):
    subset = data[data['Price']>threshold]
    strat1 = subset[subset['StartTime']<startDemandLogic]
    strat2 = subset[subset['StartTime']>endDemandLogic]
    strat = pd.concat([strat1, strat2])
    count_events = strat.count()[0]
    revenues = round(capacity*round((float(5)/60)*strat['Price'].sum()))
    energy = round((float(5)/60)*energy_to_charge*count_events)
    cost = round(energy * threshold)
    profit = round(revenues-cost)
    result = pd.DataFrame([[count_events,profit, revenues, cost, energy]])
    result.columns = ['numberEvents', 'profit', 'revenues', 'cost', 'energy']
    return result, strat, subset
    
def explore_strategy(data, start_time_threshold, end_time_threshold, capacity, weekend=False):
    #exploring various strategies
    results = pd.DataFrame()
    for threshold in range (0,500,10):
        tempResult, strat, subset = strategy(data, threshold, start_time_threshold, end_time_threshold, capacity)
        tempResult['threshold'] = threshold
        results = pd.concat([results, tempResult])
   
    plt.plot(results['threshold'], results['revenues']/1000)
    plt.xlabel('Threshold value ($)')
    plt.ylabel('Revenues ($k)')
    plt.show()
    
    plt.plot(results['threshold'], results['revenues']/1000)
    plt.xlabel('Threshold value ($)')
    plt.ylabel('Revenues ($k)')
    plt.xlim(0,100)