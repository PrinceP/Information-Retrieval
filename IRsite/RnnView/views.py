
import json
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect

from rnnmodel import returnModel,returnDictionary,returnDictionaryOriginal
import numpy
from weather import calculateTemp 
import os


from DynamicFlight import makeparameters
city_name = ['agartala', 'agra', 'ahmedabad', 'allahabad', 'amritsar', 'aurangabad', 'bagdogra', 'bangalore', 'bhavnagar', 'bhopal', 'bhubaneswar', 'bhuj', 'calcutta', 'chandigarh', 'chennai', 'cochin', 'coimbatore', 'daman', 'dehradun', 'dibrugarh', 'dimapur', 'diu', 'gauhati', 'goa', 'gwalior', 'hubli', 'hyderabad', 'imphal', 'indore', 'jaipur', 'jammu', 'jamnagar', 'jamshedpur', 'jodhpur', 'jorhat', 'kanpur', 'khajuraho', 'kozhikode', 'leh', 'lucknow', 'ludhiana', 'madurai', 'mangalore', 'mumbai', 'nagpur', 'nanded', 'nasik', 'patna', 'pondicherry', 'pune', 'porbandar', 'puttaparthi', 'rajkot', 'ranchi', 'shillong', 'silchar', 'srinagar', 'surat', 'tezpur', 'tiruchirapally', 'tirupati', 'trivandrum', 'udaipur', 'vadodara', 'varanasi', 'vijayawada', 'vishakhapatnam','delhi', 'new delhi', 'port blair', 'rae bareli']
city_codes = {'ahmedabad': 'AMD', 'hyderabad': 'HYD', 'pantnagar': 'PGH', 'agatti island': 'AGX', 'kanpur': 'KNU', 'osmanabad': 'OMN', 'gorakhpur': 'GOP', 'agartala': 'IXA', 'ramagundam': 'RMD', 'car nicobar': 'CBD', 'cooch behar': 'COH', 'thanjavur': 'TJV', 'daman': 'NMB', 'khowai': 'IXN', 'dhanbad': 'DBD', 'agra': 'AGR', 'rupsi': 'RUP', 'pondicherry': 'PNY', 'ranchi': 'IXR', 'mumbai': 'BOM', 'kailashahar': 'IXH', 'bagdogra': 'IXB', 'dehra dun': 'DED', 'chennai/madras': 'MAA', 'raipur': 'RPR', 'amritsar': 'ATQ', 'lilabari': 'IXI', 'kandla': 'IXY', 'muzaffarnagar': 'MZA', 'puttaparthi': 'PUT', 'jaisalmer': 'JSA', 'coimbatore': 'CJB', 'bangalore': 'BLR', 'pathankot': 'IXP', 'ludhiana': 'LUH', 'dibrugarh': 'DIB', 'tirupati': 'TIR', 'jammu': 'IXJ', 'bhatinda': 'BUP', 'delhi':'DEL','new delhi': 'DEL', 'jabalpur': 'JLR', 'daparizo': 'DAE', 'jagdalpur': 'JGB', 'shillong': 'SHL', 'pasighat': 'IXT', 'allahabad': 'IXD', 'tuticorin': 'TCR', 'ratnagiri': 'RTC', 'hissar': 'HSS', 'warangal': 'WGC', 'kota': 'KTU', 'bellary': 'BEP', 'dimapur': 'DMU', 'gaya': 'GAY', 'surat': 'STV', 'zero': 'ZER', 'gwalior': 'GWL', 'akola': 'AKD', 'belgaum': 'IXG', 'keshod': 'IXK', 'bikaner': 'BKB', 'jaipur': 'JAI', 'mohanbari': 'MOH', 'diu': 'DIU', 'indore': 'IDR', 'kolhapur': 'KLH', 'mangalore': 'IXE', 'darjeeling': 'DAI', 'madurai': 'IXM', 'dharamsala': 'DHM', 'hubli': 'HBX', 'sholapur': 'SSE', 'chandigarh': 'IXC', 'rajahmundry': 'RJA', 'thiruvananthapuram': 'TRV', 'kozhikode': 'CCJ', 'jamshedpur': 'IXW', 'deparizo': 'DEP', 'salem': 'SXV', 'neyveli': 'NVY', 'khajuraho': 'HJR', 'aizawl': 'AJL', 'rewa': 'REW', 'malda': 'LDA', 'rajkot': 'RAJ', 'vishakhapatnam': 'VTZ', 'jeypore': 'PYB', 'jamnagar': 'JGA', 'balurghat': 'RGH', 'goa': 'GOI', 'bilaspur': 'PAB', 'vadodara': 'BDQ', 'guna': 'GUX', 'patna': 'PAT', 'silchar': 'IXS', 'kolkata': 'CCU', 'udaipur': 'UDR', 'kamalpur': 'IXQ', 'bhopal': 'BHO', 'simla': 'SLV', 'tezpur': 'TEZ', 'rourkela': 'RRK', 'jodhpur': 'JDH', 'muzaffarpur': 'MZU', 'bhuntar': 'KUU', 'leh': 'IXL', 'varanasi': 'VNS', 'satna': 'TNI', 'cityname': 'airport-code', 'port blair': 'IXZ', 'jorhat': 'JRH', 'nasik': 'ISK', 'vijayawada': 'VGA', 'porbandar': 'PBD', 'tiruchirapally': 'TRZ', 'aurangabad': 'IXU', 'along': 'IXV', 'srinagar': 'SXR', 'gawahati': 'GAU', 'bhubaneswar': 'BBI', 'pune': 'PNQ', 'imphal': 'IMF', 'lucknow': 'LKO', 'cuddapah': 'CDP', 'bhavnagar': 'BHU', 'nagpur': 'NAG', 'rajouri': 'RJI', 'bhuj': 'BHJ', 'mysore': 'MYQ', 'nanded': 'NDC', 'bareli': 'BEK', 'tezu': 'TEI', 'kochi': 'COK'}
rnn = returnModel()
dicts_words = returnDictionary()
dicts = returnDictionaryOriginal()




def analysis(originalquery,finalquery):

	fromcity = None
	tocity = None
	par3 = "2016-05-06"
	par4 = None

	
	for i in range(0,len(finalquery) ):
		if finalquery[i] == 'B-fromloc.city_name':
			fromcity = originalquery[i]
			try:
				if finalquery[i+1] == 'I-fromloc.city_name':
					fromcity = fromcity + ' ' + originalquery[i+1]
			except IndexError:
				pass


		if finalquery[i] == 'B-toloc.city_name':
			tocity = originalquery[i]

			try:
				if finalquery[i+1] == 'I-toloc.city_name':
					tocity = tocity + ' ' + originalquery[i+1]
			except IndexError:
				pass
			try:
				tocity = tocity + ' ' + originalquery[i+1]
			except IndexError:
				pass
	print fromcity,tocity

	flight_data  =  makeparameters(fromcity,tocity,par3,par4)
	return flight_data
	
				

def contextwin(l, win):
	assert (win % 2) == 1
	assert win >= 1
	l = list(l)

	lpadded = win // 2 * [-1] + l + win // 2 * [-1]
	out = [lpadded[i:(i + win)] for i in range(len(l))]

	assert len(out) == len(l)
	return out

def searchterm(request):
	#Load the model and dictionary
	#AIzaSyAADjRri8mKUJwPDRMdJkXQO1Kz-0uDlWg

	if request.POST:
		array = []
		finalquery = request.POST['term']
		finalquery = finalquery.strip()
		finalquery = finalquery.split()
		originalquery = finalquery
		
		array = []
		for z in finalquery:
			try:
				array.append(dicts_words[z.lower()])
			except KeyError:
				print z
				if z.isdigit() :
					if(len(z) == 1):
						array.append(8)
					elif (len(z) == 2):
						array.append(9)
					elif (len(z) == 3):
						array.append(10)
					elif (len(z) == 4):
						array.append(11)

				if z.lower() in city_name:
					array.append(333)


		query = numpy.asarray(array).astype('int32')
		prediction = rnn.classify(contextwin(query,7))
		#print prediction
		array = []
		for x in prediction:
			key = dicts['labels2idx'].keys()[dicts['labels2idx'].values().index(x)]
			array.append(key)
		finalquery = '   '.join(array)
		#d = analysis(originalquery,array)
		#print d
		'''
		fare_data = []
		fromcity_data = []
		tocity_data = []
		stoppage_data = []
		duration_data = []
		airbrand_data = []
		time_data = []

		for i in range(0,len(d['trips']['tripOption'])):
			fare_data.append(d['trips']['tripOption'][i]['saleTotal'])
			for j in range(0,len(d['trips']['tripOption'][i]['slice'])):
				fromcity_data.append(d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['origin'])
				tocity_data.append(d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['destination'])
				duration_data.append(d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['duration'])
		#print fromcity_data		

		'''
		return render_to_response('search.html', {'result': (finalquery)  } )
	else:
		return render_to_response('search.html' ,{'result': None })


#home page
def welcome(request):
	'''
	Ankita Code begin
	'''
	city = 'delhi'
	path = '../data/HotelTourismData-3/Sheet1-Table_1_append.csv'
	fp = open(path,'r')
	hotel = []
	for line in iter(fp):
		x = line.strip().split(',')
		#print x[1],
		if(x[1].strip().lower()==city.strip().lower()):
			hotel.append(x)
	output = hotel
	'''
	Ankita Code end
	'''
	temp = calculateTemp()
	if request.POST:
		array = []
		finalquery = request.POST['term']
		finalquery = finalquery.strip()
		finalquery = finalquery.split()
		originalquery = finalquery
		array = []
		for z in finalquery:
			try:
				array.append(dicts['words2idx'][z.lower()])
			except KeyError:
				if z.lower() in city_name:
					array.append(88)

		query = numpy.asarray(array).astype('int32')
		prediction = rnn.classify(contextwin(query,7))
		#print prediction
		array = []
		for x in prediction:
			key = dicts['labels2idx'].keys()[dicts['labels2idx'].values().index(x)]
			array.append(key)
		finalquery = '   '.join(array)
		d = analysis(originalquery,array)
		#print d
		fare_data = []
		fromcity_data = []
		tocity_data = []
		stoppage_data = []
		duration_data = []
		airbrand_data = []
		time_data = []
		fromtime_data = []
		totime_data = []

		for i in range(0,len(d['trips']['tripOption'])):
			fare_data.append(d['trips']['tripOption'][i]['saleTotal'])
			dicti = d['trips']['data']['carrier']
			
			for j in range(0,len(d['trips']['tripOption'][i]['slice'])):
				fromcity_data.append(d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['origin'])
				tocity_data.append(d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['destination'])
				duration_data.append(d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['duration'])
				fromtime_data.append(d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['arrivalTime'])
				totime_data.append(d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['departureTime'])
				name = d['trips']['tripOption'][i]['slice'][j]['segment'][0]['flight']['carrier']
				for x in dicti:
					if x['code'] == name:
						brandname = x['name']

				airbrand_data.append(brandname)


		city=city_codes.get( tocity_data[0] )

		return render_to_response('welcome.html', {'temp':(temp["temp"]), 'humidity':(temp["humidity"]), 'result': (finalquery), 'city': (output),  'fare_data':(fare_data) , 'fromcity_data':(fromcity_data) , 'tocity_data':(tocity_data) , 'airbrand_data':(airbrand_data) , 'duration_data':(duration_data) , 'fromtime_data':(fromtime_data) , 'totime_data':(totime_data)      })
	else:
		return render_to_response('welcome.html', {'temp':(temp["temp"]), 'humidity':(temp["humidity"]), 'result': None, 'city': (output) })


	return render_to_response('welcome.html', {'temp':(temp["temp"]), 'humidity':(temp["humidity"]), 'city': (output)})
