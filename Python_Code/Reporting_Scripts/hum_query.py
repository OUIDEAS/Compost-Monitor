import json
from pymongo import MongoClient
from datetime import datetime

def query_humidity():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client['CompostMonitor']
    collection = db['Overall']  # Replace with your actual collection name

    # Prepare a dictionary to store humidity data with timestamps
    humidity_data = {
        'Container_1': [],
        'Container_2': [],
        'Container_3': [],
        'Container_4': []
    }

    # Query for all documents in the collection for containers 1, 2, 3, and 4
    for container_id in ['1', '2', '3', '4']:
        results = collection.find({'Container_No': container_id, 'BME_Humidity': { '$exists': True }}, {'Date_Time': 1, 'BME_Humidity': 1})
        print(f"Results for Container {container_id}:")
        for data in results:
            print(data)  # Print the document for debugging
            timestamp = data.get('Date_Time')
            humidity_value = data.get('BME_Humidity')

            if timestamp is not None and humidity_value is not None:
                # Ensure humidity_value is converted to float
                humidity_data[f'Container_{container_id}'].append({
                    'timestamp': timestamp.isoformat(),  # Convert datetime to ISO format string
                    'humidity': float(humidity_value)  # Convert to float
                })
            else:
                print(f"Missing data for Container {container_id} - Timestamp: {timestamp}, Humidity: {humidity_value}")

    # Calculate relative humidity for containers 1, 2, and 4 based on container 3
    relative_humidity = {
        'Container_1_Relative_Humidity': [],
        'Container_2_Relative_Humidity': [],
        'Container_4_Relative_Humidity': []
    }

    # Create a dictionary to easily access container 3's humidity values by timestamp
    container_3_humidity_dict = {entry['timestamp']: entry['humidity'] for entry in humidity_data['Container_3']}

    # Calculate relative humidity for each entry in containers 1, 2, and 4
    for entry in humidity_data['Container_1']:
        timestamp = entry['timestamp']
        if timestamp in container_3_humidity_dict:
            relative_humidity['Container_1_Relative_Humidity'].append({
                'timestamp': timestamp,
                'relative_humidity': entry['humidity'] - container_3_humidity_dict[timestamp]
            })

    for entry in humidity_data['Container_2']:
        timestamp = entry['timestamp']
        if timestamp in container_3_humidity_dict:
            relative_humidity['Container_2_Relative_Humidity'].append({
                'timestamp': timestamp,
                'relative_humidity': entry['humidity'] - container_3_humidity_dict[timestamp]
            })

    for entry in humidity_data['Container_4']:
        timestamp = entry['timestamp']
        if timestamp in container_3_humidity_dict:
            relative_humidity['Container_4_Relative_Humidity'].append({
                'timestamp': timestamp,
                'relative_humidity': entry['humidity'] - container_3_humidity_dict[timestamp]
            })

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
