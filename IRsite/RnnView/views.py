from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect

from rnnmodel import returnModel,returnDictionary


def searchterm(request):
	#Load the model and dictionary
	rnn = returnModel()
	dicts = returnDictionary()







	if request.POST:
		finalquery = request.POST['term']
		finalquery = finalquery.trim()
		finalquery = finalquery.split()

		for x in finalquery:
			if x in dicts['words2idx'].keys():
				idx = dicts['words2idx'][x]
			else:
				











		
		return render_to_response('search.html', {'result': (finalquery)  } )
	else:
		return render_to_response('search.html' ,{'result': None })