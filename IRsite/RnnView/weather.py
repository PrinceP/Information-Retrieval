import pycurl
import StringIO
import json

from html import XHTML
h = XHTML()
data = {}

def callCurl():
	response = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, 'http://api.openweathermap.org/data/2.5/weather?q=mumbai&appid=cab609a8f21e818634dfa99354765c45')
	c.setopt(c.WRITEFUNCTION, response.write)
	c.setopt(c.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	c.setopt(c.POSTFIELDS, '@request.json')
	c.perform()
	c.close()
	temp = response.getvalue()
	response.close()
	return temp



def calculateTemp():
	temp = callCurl()
	# print temp
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



