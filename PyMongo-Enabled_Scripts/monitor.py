import pymongo
import pandas
import datetime
from pandasgui import show


client = pymongo.MongoClient("mongodb://100.110.90.28/")
db = client['CompostMonitor']
collection = db['Overall']

C2_TVOC = collection.find({
                       'Container_No': '2', 
                       'TVOC_Con': {'$exists': 'True'}
                       }).sort("Date_Time", pymongo.DESCENDING).limit(1)
# C2_TVOC = pandas.DataFrame(C2_TVOC)
C2_BME = collection.find({
                       'Container_No': '2', 
                       'BME_Humidity': {'$exists': 'True'}
                       }).sort("Date_Time", pymongo.DESCENDING).limit(1)
# C2_BME = pandas.DataFrame(C2_BME)
C2_O2 = collection.find({
                       'Container_No': '2', 
                       'O2_Con': {'$exists': 'True'}
                       }).sort("Date_Time", pymongo.DESCENDING).limit(1)
# C2_O2 = pandas.DataFrame(C2_O2)
C2_meth = collection.find({
                       'Container_No': '2', 
                       'Methane_Con': {'$exists': 'True'}
                       }).sort("Date_Time", pymongo.DESCENDING).limit(1)
# C2_meth = pandas.DataFrame(C2_meth)
C2_CO2 = collection.find({
                       'Container_No': '2', 
                       'CO2_Con': {'$exists': 'True'}
                       }).sort("Date_Time", pymongo.DESCENDING).limit(1)
C2_CO2 = pandas.DataFrame(C2_CO2)



class monitor_output:
    def __init__(self, data):
        self.pandas_df = pandas.DataFrame(data)
        self.lastdate = self.pandas_df.Date_Time[0]
        self.lastdate.to_pydatetime()
        self.timedelta = datetime.datetime.now() - self.lastdate
        if (self.timedelta.total_seconds() >= 5.0):
            self.marker = False
        else:
            self.marker = True
        


C2_TVOC_marker = monitor_output(C2_TVOC)
print(C2_TVOC_marker.marker)



# datetime 

# pandas_df = pandas.DataFrame(C2_TVOC)
# lastdate = pandas_df.Date_Time[1]
# if (datetime.datetime.now - lastdate <= 15):
#     marker = True
# else:
#     marker = False



# def get_datetime(input):
#     input = pandas.DataFrame(input)
    # return(input.Date_Time[1])

# print(C2_BME.Date_Time[1])
# # print()