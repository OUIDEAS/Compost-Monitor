import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['CompostMonitor']
collection = db['Overall']

index_keys = [('Date_Time', -1), ('BME_Humidity', 1), ('CO2_Con', 1), ('O2_Con', 1), ('TVOC_Con', 1), ('Methane_Con', 1), ('Container_No', 1), ('BME_Pressure', 1), ('BME_Temp', 1)]

collection.create_index(index_keys)