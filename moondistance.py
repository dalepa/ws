import socket
from skyfield.api import load, Topos
from datetime import datetime, timezone

def calculate_moon_gps_distance(latitude, longitude, elevation_meters):
    # Load the necessary data from Skyfield's data files
    data = load('de421.bsp')
    earth, moon = data['earth'], data['moon']

    # Create a Topos object for the GPS location
    gps_location = Topos(latitude_degrees=latitude, longitude_degrees=longitude, elevation_m=elevation_meters)

    # Get the current time in UTC
    current_time = datetime.now(timezone.utc)

    # Convert the datetime object to Skyfield's UTC timescale
    ts = load.timescale()
    current_time_utc = ts.utc(current_time)

    # Compute the positions of the Moon and the GPS location at the given time
    moon_position = (moon - earth).at(current_time_utc)
    gps_position = gps_location.at(current_time_utc)

    # Calculate the distance between the Moon and the GPS location
    distance_km = (moon_position - gps_position).distance().km

    return distance_km



# GPS location coordinates (latitude, longitude, elevation in degrees and meters)
gps_latitude = 28.6372
gps_longitude = -96.459
gps_elevation_meters = 1  # Elevation above sea level in meters

# Calculate the distance using the function
distance_to_moon_km = calculate_moon_gps_distance(28.6372, -96.459, gps_elevation_meters)






# InfluxDB server information
influxdb_host = 'bi.pancamo.com'
influxdb_port = 8089

# Temperature data
measurement = 'wu.KTXOLIVI.moon.distance.km'

# Construct the InfluxDB line protocol format
influxdb_data = f'{measurement} value={distance_to_moon_km}'

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send data to InfluxDB server using UDP
client_socket.sendto(influxdb_data.encode(), (influxdb_host, influxdb_port))

# Close the socket
client_socket.close()

print("Data sent to InfluxDB using UDP: ", influxdb_data)

