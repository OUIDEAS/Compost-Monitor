COMPOST MONITOR README

Below are instructions and explanations for relevant scripts in this repo.

Tabs in flow descriptions indicate nesting level like in Python.

Folders:
-Arduino_Code
-Python_Code
    -Other_Scripts
    -Reporting_Scripts
    -Sensor_Scripts
    -System_Monitoring_Scripts

Arduino_Code: Contains code written in the Arduino IDE.

Python_Code: Contains code written in Python.
    
    -Other_Scripts: All scripts not used for reporting data, monitoring sensor activity, or reading/logging sensor data.

    -Reporting_Scripts: All scripts used to pull data from the DB and generate tables, charts, plots, etc.

    -Sensor_Scripts: All scripts used to read and log data from compost monitor sensors.

    -System_Monitoring_Scripts: All scripts used to examine the operation of sensor scripts.

Sensor_Scripts: 

    -EZO_CO2_mongoupload.py: 

        --Reads byte data from Atlas Scientific EZO-CO2 sensors as it is transmitted, decodes it, adds supporting information (e.g. timestamps) and 
            uploads it to a MongoDB collection.
        
        --Arguments:
        '-c', '--comport'           : USB port where the desired sensor is connected (e.g. /dev/ttyUSB{number} on Linux or COM{number} on Windows).
        '-f', '--filename'          : Filepath where output files should be created and stored.
        '-n', '--containernumber'   : Composting bin number.
        '-cn', '--collection'       : Name of MongoDB collection to which data should be saved.
        '-e', '--experimentnumber'  : Experiment number used to identify data from multiple experiments/tests.

        --General flow:

            -Imports
            -Pre-defining counters, filepaths, serial port connections, MongoDB address, and initializing multiprocessing.
            -Function upload_to_database
                -Argument is a dictionary of data
            -While True loop:
                -Read 1 byte from EZO-CO2
                -With log file open:
                    -write previous byte to log file
                -Append previous byte to array
                -If last byte is Carriage Return (aka CR, \r):
                    -Convert byte array into string, add to data list
                    -Add timestamp and other supporting information
                    -Convert list to dictionary with MongoDB column names
                    -Print status message
                    -Execute upload_to_database with multiprocessing
            -If enough time has passed:
                -Reset timer
                -Reset other required variables
                -Start new log file

    
    -EZO_O2_mongoupload.py:

        --Reads byte data from Atlas Scientific EZO-O2 sensors as it is transmitted, decodes it, adds supporting information (e.g. timestamps) and 
            uploads it to a MongoDB collection.
        
        --Arguments:
        '-c', '--comport'           : USB port where the desired sensor is connected (e.g. /dev/ttyUSB{number} on Linux or COM{number} on Windows).
        '-f', '--filename'          : Filepath where output files should be created and stored.
        '-n', '--containernumber'   : Composting bin number.
        '-cn', '--collection'       : Name of MongoDB collection to which data should be saved.
        '-e', '--experimentnumber'  : Experiment number used to identify data from multiple experiments/tests.

        --General flow:

            -Imports
            -Pre-defining counters, filepaths, serial port connections, MongoDB address, and initializing multiprocessing.
            -Function upload_to_database
                -Argument is a dictionary of data
            -While True loop:
                -Read 1 byte from EZO-O2
                -With log file open:
                    -write previous byte to log file
                -Append previous byte to array
                -If last byte is Carriage Return (aka CR, \r):
                    -Convert byte array into string, add to data list
                    -Add timestamp and other supporting information
                    -Convert list to dictionary with MongoDB column names
                    -Print status message
                    -Execute upload_to_database with multiprocessing
            -If enough time has passed:
                -Reset timer
                -Reset other required variables
                -Start new log file

    -methane_mongoupload.py:

        --Reads byte data from Cubic SJH-5 sensors as it is transmitted, decodes it, adds supporting information (e.g. timestamps) and uploads it 
            to a MongoDB collection.

        --Arguments:
        '-c', '--comport'           : USB port where the desired sensor is connected (e.g. /dev/ttyUSB{number} on Linux or COM{number} on Windows).
        '-f', '--filename'          : Filepath where output files should be created and stored.
        '-n', '--containernumber'   : Composting bin number.
        '-cn', '--collection'       : Name of MongoDB collection to which data should be saved.
        '-e', '--experimentnumber'  : Experiment number used to identify data from multiple experiments/tests.

        --General flow:

            -Imports
            -Pre-defining counters, filepaths, serial port connections, MongoDB address, and initializing multiprocessing.
            -Function upload_to_database
                -Argument is a dictionary of data
            -Try statement:
                -While True loop:
                    -with log file open:
                        -with CSV file open:
                            -initialize CSV writer
                            -if new CSV file, write header line
                            -Start reading_sent timer
                            -Send read_command to Cubic SJH-5 sensor
                            -While there is data in the input buffer:
                                -Read 1 byte from Cubic SJH-5
                                -Append byte to byte array
                                -increase length counter
                                -write the byte to log file
                                
                                -If packetstart is TRUE and packetsize counter is -1: (This only enters on the second byte in the sensor's 
                                                                                        response)
                                    -Convert newest byte to integer
                                    -Set packetsize to this integer
                                
                                -If packetstart is TRUE and packetsize counter is >1: (This counts the number of bytes read. Used to help 
                                                                                        determine if the response has been fully read yet)
                                    -Add 1 to packetcount
                                    
                                -If newest byte looks like the status byte:
                                    -Check whether it is the real status byte or another byte with the same value
                                    -If it is the status byte, set length counter to 0
                                    -If it is not the status byte, set packetstart flag to TRUE
                                
                                -If packetcount is 1 greater than packetsize:         (This means that the newest byte is the first byte of the
                                                                                        sensor's next message)
                                    -Turn byte array into a byte string
                                    -Unpack the byte string (Big-endian)
                                    -Reset the serial port input buffer
                                    -Start the data list with the timestamp
                                    -Append unpacked data to data list
                                    -Append container number and experiment number
                                    -Write data to the CSV file
                                    -Convert data list to a dictionary
                                    -Print status message
                                    -Execute upload_to_database with multiprocessing
                                    -Reset word/packet counters
                                    -Increase loop counter by 1
                        -While read timer has not elapsed:
                            -Sleep 100ms
            -Except statement:
                -Display error message
                -Write error timestamp in log file
            
            -If 500 lines have been written to the .CSV file:
                -Reset loop counter
                -Reset precursor values
                -Start new log and .csv files



    
    -RedBoard_mongoupload.py

        --Reads byte data from RedBoard Qwiic development boards as it is transmitted, decodes it, adds supporting information (e.g. timestamps) and 
            uploads it to a MongoDB collection.

        --Arguments:
        '-c', '--comport'           : USB port where the desired sensor is connected (e.g. /dev/ttyUSB{number} on Linux or COM{number} on Windows).
        '-f', '--filename'          : Filepath where output files should be created and stored.
        '-n', '--containernumber'   : Composting bin number.
        '-cn', '--collection'       : Name of MongoDB collection to which data should be saved.
        '-e', '--experimentnumber'  : Experiment number used to identify data from multiple experiments/tests.

        --General flow:

            -Imports
            -Pre-defining counters, filepaths, serial port connections, MongoDB address, and initializing multiprocessing.
            -Function upload_to_database
                -Argument is a dictionary of data
            -While True loop:
                -Read 1 byte from RedBoard
                -With log file open:
                    -write previous byte to log file
                -Append previous byte to array
                -If last byte is Carriage Return (aka CR, \r):
                    -Convert byte array into string, add to data list
                    -Add timestamp and other supporting information
                    -Convert list to dictionary with MongoDB column names
                    -Print status message
                    -Execute upload_to_database with multiprocessing
            -If enough time has passed:
                -Reset timer
                -Reset other required variables
                -Start new log file

-Reporting_Scripts:

    -plotting.py

        --Queries a MongoDB collection for data from each sensor type for each container. Arguments allow the code to return all of the documents 
            or a smaller quantity. Arguments allow the code to pull data for all sensors or just individual sensors.

        --Arguments:
        '-s', '--sensor'
        '-n', '--number', default = 'All'
        '-c', '--containernumber', default = 'All'
        '-t', '--saveSheet', default = 0

        --General flow:

            -Imports
            -Set variables for MongoDB
            -Initialize argument parser and set Arguments
            -Function emptycells
                -Takes a DataFrame and removes empty cells
            -Function deleteExtras
                -Takes a DataFrame and removes rows that have data but no timestamp or a timestamp but no data
            -Function pull_data
                -Takes sensor type and container number as arguments
                -Set number of documents to pull based on --number argument
                -Query MongoDB
                -Match case (sensor type)
                    -Ensures proper formatting for dataframes and converts data fields to list format
                    -Calls functions emptycells and deleteExtras as needed
            -Function plots
                -Arguments are: data_set, plot title, axis titles, and file path
                -Checks formatting of data
                -Creates a scatter plot with data from pull_data
            -if __name__ == '__main__':
                -With multiprocessing Manager object as manager:
                    -Pre-defines managed lists for each sensor variable and its associated timestamps
                    -Creates 28 processes (7 sensor types for 4 bins) which execute pull_data and waits for them to all finish
                    -if sensor:
                        -Add data from managed list to data_sets list
                        -Execute plots function
    
    -plotting_to_csv.py

        --Similar to plotting.py, but is intended to export data to .csv format to be read into a program later

        --Arguments:
        None (currently)




Connecting Sensors for Compost Monitor:
---------------------------------------
1. In terminal, use ‘cd /sys/class/tty’ and ‘ls’
2. Take note of the ports listed
3. After each restart or any time the RedBoard is not recognized in sys/class/tty, unplug USB-A cable for the RedBoard. While holding down RESET on the RedBoard, plug the USB cable back in. 
4. Use ‘ls’ again. The RedBoard QWIIC shows up in /sys/class/tty as ‘ttyUSBX’, where X is an integer. It will default to the lowest integer that is unused (if ttyUSB0 and ttyUSB2 are already listed, the latest device to connect will be listed as ‘ttyUSB1’). 
