import pymongo
import pandas

# from pandasgui import show


client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client['CompostMonitor']
collection = db['Overall']
indexes = collection.list_indexes()

for index in indexes:
    print(index)

print(collection.count_documents({}))

docs= collection.find()
print(docs)
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