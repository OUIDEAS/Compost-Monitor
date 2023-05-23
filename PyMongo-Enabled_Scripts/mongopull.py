import pymongo
import pandas

client = pymongo.MongoClient("mongodb://100.110.90.28/")
db = client['CompostMonitor']
collection = db['Overall']

docs= collection.find({'Container_No': '2'}).sort("_id", pymongo.DESCENDING).limit(500)
docs_DF = pandas.DataFrame(docs)

print(docs_DF)