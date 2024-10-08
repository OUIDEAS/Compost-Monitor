import json
from pymongo import MongoClient
from datetime import datetime
import numpy as np
import time

def query_humidity():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client['CompostMonitor']
    collection = db['Jun28Experiment']  # Replace with your actual collection name

    # Prepare a dictionary to store humidity data with timestamps
    humidity_data = {
        'Container_1': [],
        'Container_2': [],
        'Container_3': [],
        'Container_4': []
    }

    results = list(collection.find({}, {"BME_Humidity": 1, "Date_Time": 1, "Container_No": 1, "_id": 0}))
    # Query for all documents in the collection for containers 1, 2, 3, and 4
    # for container_id in ['1', '2', '3', '4']:
        

    # print(f"Results for Container {container_id}:")
    for data in results:
        # print(data.get('Container_No'))
        if data.get('Container_No') != 'Ambient' and data.get('Container_No') != None:
            container = f"Container_{data['Container_No']}"
        # print(data)  # Print the document for debugging
        # timestamp = data.get('Date_Time')
        # humidity_value = data.get('BME_Humidity')
            if container in humidity_data:
                
                if data.get('BME_Humidity')!=None:
                    # print(data.get('BME_Humidity'), container)
                    humidity_data[container].append({
                        'Date_Time': data.get('Date_Time').isoformat() if isinstance(data.get('Date_Time'), datetime) else data.get('Date_Time'),
                        'BME_Humidity': data.get('BME_Humidity'),
                        'Container_No': data.get('Container_No')
                    })
                # print(container)
    # print(humidity_data)
    # rel_hum1 = humidity_data[]

    # for container, data in humidity_data.items():
    #     print(f"{container}: {data}")
        # if timestamp is not None and humidity_value is not None:
        #     # Ensure humidity_value is converted to float
        #     humidity_data[f'Container_{container_id}'].append({
        #         'timestamp': timestamp.isoformat(),  # Convert datetime to ISO format string
        #         'humidity': float(humidity_value)  # Convert to float
        #     })
        # else:
        #     print(f"Missing data for Container {container_id} - Timestamp: {timestamp}, Humidity: {humidity_value}")

    # Calculate relative humidity for containers 1, 2, and 4 based on container 3

    # relative_humidity = {
    #     'Container_1_Relative_Humidity': [],
    #     'Container_2_Relative_Humidity': [],
    #     'Container_3_Relative_Humidity': [],
    #     'Container_4_Relative_Humidity': []
    # }

    # # Create a dictionary to map container 3's humidity values to their timestamps
    
    # print(humidity_data['Container_1'][100])
    # # For each container's humidity data, calculate the relative humidity
    # for container in ['Container_1', 'Container_2', 'Container_3', 'Container_4']:
    #     # print(container, len(humidity_data['Container_3']))
    #     # print(humidity_data.keys())
    #     if len(humidity_data[container]) < len(humidity_data['Container_3']):
    #         cont = container
    #     else:
    #         cont = 'Container_3'
    #     for i in range(0, len(humidity_data[cont]), 10):
    #         # print(int(i))
    #         # for entry in humidity_data[container]:
    #         # print(entry, i)
    #         timestamp = humidity_data[container][int(i)]['Date_Time']
    #         # print(entry['BME_Humidity'])
    #         # print(humidity_data['Container_3'][i]['BME_Humidity'])
    #         # print(container, i)
    #         # if timestamp in humidity_data['Container_3']:
    #         relative_humidity[f'{container}_Relative_Humidity'].append({
    #             'Date_Time': timestamp,
    #             'relative_humidity': float(humidity_data[container][int(i)]['BME_Humidity']) - float(humidity_data['Container_3'][int(i)]['BME_Humidity']),
    #             'Container_No': container
    #         })
    condensed_relative_humidity = []

    # Calculate relative humidity for containers 1, 2, and 4 based on container 3
    for container in ['Container_1', 'Container_2', 'Container_4']:
        if len(humidity_data[container]) < len(humidity_data['Container_3']):
            cont = container
        else:
            cont = 'Container_3'
        for i in range(len(humidity_data[cont])):
            timestamp = humidity_data[container][i]['Date_Time']
            relative_humidity_value = float(humidity_data[container][i]['BME_Humidity']) - float(humidity_data['Container_3'][i]['BME_Humidity'])
            condensed_relative_humidity.append({
                'Date_Time': timestamp,
                'Relative_Humidity': relative_humidity_value,
                'Container_No': container
            })
            # time.sleep(1)
            # print(relative_humidity['Container_1_Relative_Humidity'], i)
                # print('OKAY')
    
                # else:
                #     print(f"No matching timestamp in Container 3 for {container} - Timestamp: {timestamp}")
    # print(relative_humidity)
    # Export the results to a JSON file
    output_data = {
        'BME_Humditiy': humidity_data,
        'Relative_Humidity': condensed_relative_humidity,
    }

    for container in humidity_data:
        for entry in humidity_data[container]:
            entry['Date_Time'] = entry['Date_Time'].isoformat() if isinstance(entry['Date_Time'], datetime) else entry['Date_Time']

    with open('relative_humidity_data.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

    print("Relative humidity data exported to relative_humidity_data.json")

if __name__ == '__main__':
    query_humidity()
