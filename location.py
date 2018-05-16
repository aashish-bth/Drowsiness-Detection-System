from math import radians, cos, sin, asin, sqrt
import geocoder
import json
import requests

"""Driver details"""
user_latitude = 22.5697
user_longitude = 88.3697
city = "Kolkata"
print("\nUser/Driver details:")
print ("latitude = " + str(user_latitude) + "\nlongitude = " + str(user_longitude) + "\ncity = " + city)

"""Emergency contact person details"""
#visit https://stackoverflow.com/questions/24906833/get-your-location-through-python/49778452#49778452 to known about, how to get your own access_key
freegeoip = "http://api.ipstack.com/check?access_key=Your_ACCESS_KEY"
geo_r = requests.get(freegeoip)
geo_j = json.loads(geo_r.text)
ip = geo_j['ip']
location = geo_j['city']
lat_ecp = geo_j['latitude']
lon_ecp = geo_j['longitude']
print("\nEmergency contact person details:")
print("Your location = " + location)


"""Calculate the distance between two points"""
try:
	lon_ecp, lat_ecp, user_longitude, user_latitude = map(radians, [lon_ecp, lat_ecp, user_longitude, user_latitude])

	# haversine formula 
	dlon = user_longitude - lon_ecp 
	dlat = user_latitude - lat_ecp 
	a = sin(dlat/2)**2 + cos(lat_ecp) * cos(user_latitude) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	km = 6367 * c

	km = ('%.0f'%km)

	msg_distance = 'Driver is about '+str(km)+' km away from you';
	print(msg_distance)
except:
	print('\nUnable to calculate distance.')
	msg_distance = 'Unable to calculate distance.'

website = 'https://www.google.com/maps/'
co_ordinates = "?q="+str(user_latitude)+","+str(user_longitude)
