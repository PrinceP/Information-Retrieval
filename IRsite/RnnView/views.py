
import json
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect

from rnnmodel import returnModel,returnDictionary,returnDictionaryOriginal
import numpy


from DynamicFlight import makeparameters
city_name = ['agartala', 'agra', 'ahmedabad', 'allahabad', 'amritsar', 'aurangabad', 'bagdogra', 'bangalore', 'bhavnagar', 'bhopal', 'bhubaneswar', 'bhuj', 'calcutta', 'chandigarh', 'chennai', 'cochin', 'coimbatore', 'daman', 'dehradun', 'dibrugarh', 'dimapur', 'diu', 'gauhati', 'goa', 'gwalior', 'hubli', 'hyderabad', 'imphal', 'indore', 'jaipur', 'jammu', 'jamnagar', 'jamshedpur', 'jodhpur', 'jorhat', 'kanpur', 'khajuraho', 'kozhikode', 'leh', 'lucknow', 'ludhiana', 'madurai', 'mangalore', 'mumbai', 'nagpur', 'nanded', 'nasik', 'patna', 'pondicherry', 'pune', 'porbandar', 'puttaparthi', 'rajkot', 'ranchi', 'shillong', 'silchar', 'srinagar', 'surat', 'tezpur', 'tiruchirapally', 'tirupati', 'trivandrum', 'udaipur', 'vadodara', 'varanasi', 'vijayawada', 'vishakhapatnam', 'new delhi', 'port blair', 'rae bareli']
rnn = returnModel()
dicts_words = returnDictionary()
dicts = returnDictionaryOriginal()

fromcity = None
tocity = None
par3 = None


def analysis(originalquery,finalquery):
	
	for i in range(0,len(finalquery)):
		if finalquery[i] == 'B-fromloc.city_name':
			fromcity = originalquery[i]
			if finalquery[i+1] == 'I-fromloc.city_name':
				fromcity = fromcity + ' ' + originalquery[i+1]

		if finalquery[i] == 'B-toloc.city_name':
			tocity = originalquery[i]
			if finalquery[i+1] == 'I-toloc.city_name':
				tocity = tocity + ' ' + originalquery[i+1]

	flight_data  =  makeparameters(fromcity,tocity,par3)
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
		data = analysis(originalquery,array)

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
















		
		return render_to_response('search.html', {'result': (fare_data)  } )
	else:
		return render_to_response('search.html' ,{'result': None })

	

