import pycurl
import StringIO
import json
import socket

from html import XHTML
h = XHTML()
data = {}


#Below code checks internet connection validity
REMOTE_SERVER = "www.google.com"
def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False
print is_connected()

def callCurl(city):
	city = city.split()
	if len(city) > 1:
		city = city[1]
	else:
		city = city[0]
		
	if is_connected():
		response = StringIO.StringIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=cab609a8f21e818634dfa99354765c45')
		c.setopt(c.WRITEFUNCTION, response.write)
		c.setopt(c.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
		c.setopt(c.POSTFIELDS, '@request.json')
		c.perform()
		c.close()
		temp = response.getvalue()
		response.close()
	else:
		temp = '{"coord":{"lon":77.22,"lat":28.67},"weather":[{"id":761,"main":"Dust","description":"dust","icon":"50d"}],"base":"stations","main":{"temp":314.15,"pressure":1004,"humidity":8,"temp_min":314.15,"temp_max":314.15},"visibility":3500,"wind":{"speed":4.1,"deg":320,"gust":9.3},"clouds":{"all":0},"dt":1462089600,"sys":{"type":1,"id":7809,"message":0.0111,"country":"IN","sunrise":1462061393,"sunset":1462109208},"id":1273294,"name":"Delhi","cod":200}'
	return temp




def calculateTemp(city):
	temp = callCurl(city)
	json1_data = json.loads(temp)


	for key in json1_data:
		lst = {}
		if isinstance(json1_data[key],dict):
			for k,v in json1_data[key].items():
				data[k] = v
		else:
			if (key != "weather"):
				data[key] = json1_data[key]
			
			

	# print data
	# cab609a8f21e818634dfa99354765c45
	country=""
	temp = ""
	humidity = ""
	city = ""
	date = ""


	if "country" in data:
		country = data["country"]
	if "temp" in data:
		temp = data["temp"]
	if "name" in data:
		city = data["name"]
	if "humidity" in data:
		humity = data["humidity"]	
	if "dt" in data:
		date = data['dt']

	#tempreture is in kelvin, convert into celcius
	# c = k-273.15
	celTemp = str(temp - 273.15) + "c"

	return {'temp':celTemp, "humidity":humity}



