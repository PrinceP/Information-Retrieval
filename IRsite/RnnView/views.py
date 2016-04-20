from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect

from rnnmodel import returnModel,returnDictionary
import numpy

city_name = ['agartala', 'agra', 'ahmedabad', 'allahabad', 'amritsar', 'aurangabad', 'bagdogra', 'bangalore', 'bhavnagar', 'bhopal', 'bhubaneswar', 'bhuj', 'calcutta', 'chandigarh', 'chennai', 'cochin', 'coimbatore', 'daman', 'dehradun', 'dibrugarh', 'dimapur', 'diu', 'gauhati', 'goa', 'gwalior', 'hubli', 'hyderabad', 'imphal', 'indore', 'jaipur', 'jammu', 'jamnagar', 'jamshedpur', 'jodhpur', 'jorhat', 'kanpur', 'khajuraho', 'kozhikode', 'leh', 'lucknow', 'ludhiana', 'madurai', 'mangalore', 'mumbai', 'nagpur', 'nanded', 'nasik', 'patna', 'pondicherry', 'pune', 'porbandar', 'puttaparthi', 'rajkot', 'ranchi', 'shillong', 'silchar', 'srinagar', 'surat', 'tezpur', 'tiruchirapally', 'tirupati', 'trivandrum', 'udaipur', 'vadodara', 'varanasi', 'vijayawada', 'vishakhapatnam', 'new delhi', 'port blair', 'rae bareli']
rnn = returnModel()
dicts = returnDictionary()



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
	


	if request.POST:
		array = []
		finalquery = request.POST['term']
		finalquery = finalquery.strip()
		finalquery = finalquery.split()
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
		return render_to_response('search.html', {'result': (finalquery)  } )
	else:
		return render_to_response('search.html' ,{'result': None })

	

