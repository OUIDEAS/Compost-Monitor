# response = b'0;37.75;95287.97;23.45'
# parsed_data = response.decode('utf-8').strip().split(';')
# status = parsed_data[0]
# ch4_concentration = float(parsed_data[1])
# reference_value = float(parsed_data[2])
# temperature_humidity = float(parsed_data[3])

# print(f"Status: {status}")
# print(f"CH4 Concentration: {ch4_concentration} ppm")
# print(f"Reference Value: {reference_value}")
# print(f"Temperature/Humidity: {temperature_humidity}")
def parse_sensor_response(response):
    # Decode the response and remove trailing spaces
    parsed_data = response.decode('utf-8').strip().split(';')

    # Extract DF1, DF2, and sensor status (ST1, ST2)
    df1 = float(parsed_data[1]) # DF1 - part of the gas concentration
    df2 = float(parsed_data[2]) # DF2 - part of the gas concentration
    st1 = float(parsed_data[3])  # Sensor working status
    # st2 = parsed_data[4]  # Additional status (may be reserved)

    # Calculate CH4 concentration
    ch4_concentration = (df1 * 256 + df2) / 100

    # Parse ST1 bits to understand the sensor status
    # status = {
    #     'Measurement Over Limit': (st1 & 0x80) > 0,  # BIT7
    #     'Reference Over Limit': (st1 & 0x40) > 0,   # BIT6
    #     'High Humidity': (st1 & 0x20) > 0,           # BIT5
    #     'No Calibration': (st1 & 0x10) > 0,          # BIT4
    #     'Out of Range': (st1 & 0x02) > 0,            # BIT1
    #     'Malfunction': (st1 & 0x01) > 0,             # BIT0
    #     'Warming Up': (st1 & 0x08) > 0               # BIT3
    # }

    # Return parsed data
    return {
        'CH4 Concentration': ch4_concentration,
        # 'Sensor Status': status,
        # 'ST2': st2  # Additional status byte (reserved or used for other flags)
    }

# Example usage with the response you received
# response = b'0;37.71;95308.80;23.47 '
response = b'0;25.78;94915.13;23.88'
sensor_data = parse_sensor_response(response)

print(f"CH4 Concentration: {sensor_data['CH4 Concentration']} ppm")
print("Sensor Status:")
# for key, value in sensor_data['Sensor Status'].items():
#     print(f"  {key}: {'Yes' if value else 'No'}")
# print(f"ST2: {sensor_data['ST2']}")
