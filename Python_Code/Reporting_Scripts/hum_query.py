import json
from pymongo import MongoClient
from datetime import datetime

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
                humidity_data[container].append({
                    'Date_Time': data.get('Date_Time'),
                    'BME_Humidity': data.get('BME_Humidity'),
                    'Container_No': data.get('Container_No')
                })
                # print(container)
    print(humidity_data)
    # rel_hum1 = humidity_data[]

    for container, data in humidity_data.items():
        print(f"{container}: {data}")
        # if timestamp is not None and humidity_value is not None:
        #     # Ensure humidity_value is converted to float
        #     humidity_data[f'Container_{container_id}'].append({
        #         'timestamp': timestamp.isoformat(),  # Convert datetime to ISO format string
        #         'humidity': float(humidity_value)  # Convert to float
        #     })
        # else:
        #     print(f"Missing data for Container {container_id} - Timestamp: {timestamp}, Humidity: {humidity_value}")

    # Calculate relative humidity for containers 1, 2, and 4 based on container 3
    relative_humidity = {
        'Container_1_Relative_Humidity': [],
        'Container_2_Relative_Humidity': [],
        'Container_4_Relative_Humidity': []
    }

    # Create a dictionary to map container 3's humidity values to their timestamps
    container_3_humidity_dict = {entry['Date_Time']: entry['BME_Humidity'] for entry in humidity_data['Container_3']}

    # For each container's humidity data, calculate the relative humidity
    for container in ['Container_1', 'Container_2', 'Container_4']:
        for entry in humidity_data[container]:
            timestamp = entry['Date_Time']
            if timestamp in container_3_humidity_dict:
                relative_humidity[f'{container}_Relative_Humidity'].append({
                    'Date_Time': timestamp,
                    'relative_humidity': entry['BME_Humidity'] - container_3_humidity_dict[timestamp]
                })
            else:
                print(f"No matching timestamp in Container 3 for {container} - Timestamp: {timestamp}")

    # Export the results to a JSON file
    output_data = {
        'Container_Humidity': humidity_data,
        'Relative_Humidity': relative_humidity
    }

    with open('relative_humidity_data.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

    print("Relative humidity data exported to relative_humidity_data.json")

if __name__ == '__main__':
    query_humidity()