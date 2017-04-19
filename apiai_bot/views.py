from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

try:
    from urllib.parse import urlparse, urlencode
except ImportError:
     from urllib2 import urlparse
     from urllib import urlencode

try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request

try:
 	from urllib.error import HTTPError
except ImportError:
 	from urllib2 import HTTPError


import json
import os

@csrf_exempt
def test_list(request):
	# OrderedDict([('id', 1), ('title', u'test snippet'), ('code', u'test1test'), ('linenos', True), ('language', 'abap'), ('style', 'abap')])
	a = {"id": 1}
	return JsonResponse(a, safe=False)


@csrf_exempt
def webhook(request):
	if request.method == 'POST':
		print("Request1:")
		print(JSONParser().parse(request))
		# req = request.get_json(silent=True, force=True)
		req = request.__dict__(silent=True, force=True)

		print("Request: ")
		print(json.dumps(req, indent = 4))

		res = processRequest(req)

		res = json.dumps(res, indent=4)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r

def processRequest(req):
	baseurl = "https://api.themoviedb.org/3/discover/movie?api_key=a6669e892c1628955e0af913f38dbb91&"
	params = checkParams(req)
	url = baseurl + params

	result = urlopen(url).read()
	data = json.loads(result)
	res = makeWebhookResult(req, data)

	return res

def checkParams(req):
	result = req.get("result")
	action = req.get("action")
	parameters = req.get("parameters")
	keyword = req.get("keyword")

	context = result.get("contexts")[0]
	context_name = context.get("name")

	if keyword == "popular":
		url_params = "sort_by=popularity.desc"
	else:
		url_params = "sort_by=popularity.desc"
	return url_params

def makeWebhookResult(req, data):
	result = req.get("result")
	action = result.get("action")
	parameters = result.get("parameters")
	keyword = result.get("keyword")

	context = result.get("contexts")[0]
	context_name = context.get("name")

	total_results = data.get('total_results')

	if req.get("result").get("action") == "movieTeller":
		speech = req.get("result").get("action") + "(two-way-new)We found " + str(total_results) + " movies."
	elif req.get("result").get("action") == "movieOption":
		speech = "Movie Option"
	else:
		speech = "Error !"

	print("Response:")
	print(speech)

	return {
		"speech": speech,
		"displayText": speech,
		"sourcee": "apiai_bot"
	}



