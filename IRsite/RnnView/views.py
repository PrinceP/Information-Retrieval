
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

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from word2number import w2n

def month_converter(month):
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    return months.index(month.lower()) + 1



def analysis(originalquery,finalquery):

	fromcity = None
	tocity = None
	par3 = (time.strftime("%Y-%m-%d"))
	par4 = None
	time_day = None
	time_relative = None
	time_nu = None
	time_period = None



	time_spec_month = None 
	time_spec_date = None
	
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
			
	#print fromcity,tocity
		if finalquery[i] =='B-depart_date.day_name':
			time_day = originalquery[i]

		if finalquery[i] == 'B-depart_time.time_relative':
			time_relative = originalquery[i]

		if finalquery[i] == 'B-depart_time.time':
			time_nu = originalquery[i]
			try:
				if finalquery[i+1] == 'I-depart_time.time':
					time_nu = time_nu + ' ' + originalquery[i+1]
			except IndexError:
				pass
			try:
				time_nu = time_nu + ' ' + originalquery[i+1]
			except IndexError:
				pass
		if finalquery[i] == 'B-arrive_time.period_of_day':
			time_period = originalquery[i]
			try:
				if finalquery[i+1] == 'I-arrive_time.period_of_day':
					time_period = time_period + ' ' + originalquery[i+1]
			except IndexError:
				pass
			try:
				time_period = time_period + ' ' + originalquery[i+1]
			except IndexError:
				pass


		if finalquery[i] =='B-depart_date.month_name':
			time_spec_month = originalquery[i]
			time_spec_month = month_converter(time_spec_month)

		if finalquery[i] == 'B-depart_date.day_number':
			time_spec_date = originalquery[i]
			time_spec_date = w2n.word_to_num(time_spec_date)





				



	if time_day is not None:		
		x = 0
		if time_day.lower() == 'monday':
			time_day = 0
		elif time_day.lower() =='tuesday':
			time_day = 1
		elif time_day.lower() =='wednesday':
			time_day = 2
		elif time_day.lower() =='thursday':
			time_day = 3
		elif time_day.lower() =='friday':
			time_day = 4
		elif time_day.lower() =='saturday':
			time_day = 5
		elif time_day.lower() =='sunday':
			time_day = 6
		x = int(datetime.today().weekday()) - time_day	
		date_after = datetime.now()+ relativedelta(days=int(x))
		print date_after
		par3 = date_after.strftime('%Y-%m-%d')
	

	if time_spec_month is not None:
		if (str(time_spec_month))==1:
			time_spec_month = '0'+str(time_spec_month)
		par3 = '2016-'+str(time_spec_month)+'-'+str(time_spec_date)
		print par3 



		
	 	

				
	flight_data  =  makeparameters(fromcity,tocity,par3,par4)
	return flight_data,time_period,time_relative,time_nu
	
				

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
		
		return render_to_response('search.html', {'result': (finalquery)  } )
	else:
		return render_to_response('search.html' ,{'result': None })


#home page
def welcome(request):
	'''
	Ankita Code begin
	'''
	city = 'Delhi'
	path = '../data/HotelTourismData-3/Sheet1-Table_1_append32.csv'
	fp = open(path,'r')
	hotel = []
	for line in iter(fp):
		x = line.strip().split(',')
		if(x[0].strip().lower()==city.strip().lower()):
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
		d,time_period,time_relative,time_nu = analysis(originalquery,array)
		#print d
		fare_data = []
		fromcity_data = []
		tocity_data = []
		#stoppage_data = []
		duration_data = []
		airbrand_data = []
		
		fromtime_data = []
		totime_data = []

		





		
		for i in range(0,len(d['trips']['tripOption'])):
			fare_data.append(d['trips']['tripOption'][i]['saleTotal'])
			dicti = d['trips']['data']['carrier']
			
			for j in range(0,len(d['trips']['tripOption'][i]['slice'])):
				fromcity_data.append(d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['origin'])
				tocity_data.append(d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['destination'])
				duration = (d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['duration'])
				duration =str(duration)
				if len(duration) == 3:
					duration = duration[0]+'H'+duration[1:]+'M'
				elif len(duration) == 4:
					duration = duration[0:2]+'H'+duration[2:]+'M'
				duration_data.append(duration)	
				 	
				
				m = d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['arrivalTime'].split('T')
				m[1] = m[1][0:5]
				m = m[0] +'   '+m[1]
				fromtime_data.append(m)
				n = d['trips']['tripOption'][i]['slice'][j]['segment'][0]['leg'][0]['departureTime'].split('T')
				n[1] = n[1][0:5]
				n = n[0] + '  '+n[1]
				totime_data.append(n)


				name = d['trips']['tripOption'][i]['slice'][j]['segment'][0]['flight']['carrier']
				for x in dicti:
					if x['code'] == name:
						brandname = x['name']

				airbrand_data.append(brandname)
		m = -1		
		if time_nu is not None:
			time_nu = time_nu.split()
			if time_nu[1] == 'pm':
				m = int(time_nu[0])
				m = m + 12
			else:
				m = int(time_nu[0])
		flag = -1
		if time_relative is not None:
			if time_relative == 'after':
				flag = 1
			else:
				flag = 0  
		slot1 = -1
		slot2 = -1
		if time_period is not None :
			if time_period == 'morning':
				slot1 = 4
				slot2 = 11

			elif time_period == 'afernoon':
				slot1 = 11
				slot2 = 15

			elif time_period == 'evening':
				slot1 = 15
				slot2 = 18


			elif time_period == 'night':
				slot1 = 18
				slot2 = 24

				
				


		total_data = []
		for i in range(0,len(fare_data)):

			if m > 0:
				x = fromtime_data[i].split()
				x = x[1].split(':')
				if flag == 1:
					if m >= int(x[0]):
						tot = {'fare':fare_data[i], 'from':fromcity_data[i] , 'to':tocity_data[i] , 'brand':airbrand_data[i] , 'duration':duration_data[i] , 'starttime':fromtime_data[i] , 'endtime': totime_data[i] }
				
				elif flag == 0:
					if m <= int(x[0]):
						tot = {'fare':fare_data[i], 'from':fromcity_data[i] , 'to':tocity_data[i] , 'brand':airbrand_data[i] , 'duration':duration_data[i] , 'starttime':fromtime_data[i] , 'endtime': totime_data[i] }
			
			elif slot1 > 0:
				x = fromtime_data[i].split()
				x = x[1].split(':')
				if  int(x[0]) < slot2:
					tot = {'fare':fare_data[i], 'from':fromcity_data[i] , 'to':tocity_data[i] , 'brand':airbrand_data[i] , 'duration':duration_data[i] , 'starttime':fromtime_data[i] , 'endtime': totime_data[i] }
			




			else :
				tot = {'fare':fare_data[i], 'from':fromcity_data[i] , 'to':tocity_data[i] , 'brand':airbrand_data[i] , 'duration':duration_data[i] , 'starttime':fromtime_data[i] , 'endtime': totime_data[i] }
			tot = {'fare':fare_data[i], 'from':fromcity_data[i] , 'to':tocity_data[i] , 'brand':airbrand_data[i] , 'duration':duration_data[i] , 'starttime':fromtime_data[i] , 'endtime': totime_data[i] }
			
			total_data.append(tot)
		city=city_codes.get( tocity_data[0] )

		
		
		return render_to_response('welcome.html', {'temp':(temp["temp"]), 'humidity':(temp["humidity"]), 'result': (finalquery), 'total_data':(total_data)  })
	else:
		return render_to_response('welcome.html', {'temp':(temp["temp"]), 'humidity':(temp["humidity"]), 'result': None, 'city': (output) })


	return render_to_response('welcome.html', {'temp':(temp["temp"]), 'humidity':(temp["humidity"]), 'city': (output)})
