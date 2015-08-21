#%%
import urllib2
import xml.etree.ElementTree as ET
import zipfile
import requests
import StringIO
import pandas as pd

def getZIP(zipFileName):
    r = requests.get(zipFileName).content
    s = StringIO.StringIO(r)
    zf = zipfile.ZipFile(s, 'r') # Read in a list of zipped files
    return zf

def get_node_price(node, yearStart, monthStart, dayStart, yearEnd, monthEnd, dayEnd):
    startdatetime = time_into_datetime(yearStart, monthStart, dayStart, hour=7)
    enddatetime = time_into_datetime(yearEnd, monthEnd, dayEnd, hour=7)
    resultFormat = 'resultformat=6'
    queryname = 'PRC_INTVL_LMP'
    test =  'http://oasis.caiso.com/oasisapi/SingleZip?'+resultFormat+'&queryname='+queryname+'&startdatetime='+startdatetime+'&enddatetime='+enddatetime+'market_run_id=RTM&version=1&'+'node='+node
    zf = getZIP(test)
    request = zf.open(zf.namelist()[0])
    lmp = pd.read_csv(request)
    #lmp.columns=['startDateTime', 'type', 'price']
    return lmp
    
def time_into_datetime(year, month, day, hour=7):
    year = str(year)
    month=str(month)
    day=str(day)
    hour=str(hour)
    if int(hour)<10:
        hour='0'+hour
    if int(day)<10:
        day='0'+day
    if int(month)<10:
        month='0'+month
    datetime = year+month+day+'T'+hour+':00-0000'
    return str(datetime)
    

#%%
for year in [2012, 2013, 2014]:
    node1 = 'VACA-DIX_1_N015'
    daysPerMonth = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    for month in range(1,13):
        df_month = pd.DataFrame()
        for day in range(1, 3):
            print str(day)+'/'+str(month)+'/'+str(year)
            df_day = get_node_price(node1, 2015, month, day, 2015, month, day+1)
            df_month = pd.concat([df_month, df_day])
        df_month.to_csv('VACA_'+str(year)+'_'+str(month)+'.csv')
        print 'Completed '+str(month)