import pymongo
import pandas
from pandasgui import show


client = pymongo.MongoClient("mongodb://100.110.90.28/")
db = client['CompostMonitor']
collection = db['Overall']

docs= collection.find().limit(10)
# field_names = set()
# for document in docs:
#     field_names.update(document.keys())
docs_DF = pandas.DataFrame(docs)
# show(docs_DF)


print(docs_DF) 
# print(docs_DF.Date_Time[1])
# print(field_names)

# query1 = {'drivingModes': {'$exists': 'True'}}
# query2 = {'modes': {'$exists': 'True'}}