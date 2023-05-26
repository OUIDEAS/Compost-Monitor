import pymongo
import pandas
from pandasgui import show


client = pymongo.MongoClient("mongodb://100.110.90.28/")
db = client['CompostMonitor']
collection = db['Overall']

docs= collection.find({
                       'Container_No': '2', 
                       'CO2_Con': {'$exists': 'True'}
                       }).sort("Date_Time", pymongo.DESCENDING).limit(500)
docs_DF = pandas.DataFrame(docs)
# show(docs_DF)


print(docs_DF) 
print(docs_DF.Date_Time[1])