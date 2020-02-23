import json
import time
import HTTPInterface

##
# Gets the details when a movie id is passed.
#
# Returns a tuple as follows:
# 			(id, name, picture_url)
##
def get_movie_detail(movie_id):
	time.sleep(0.4)
	API_URL = 'http://www.einthusan.com/webservice/movie.php?id=' + str(movie_id)
	html = HTTPInterface.http_get(API_URL)
	response_json = {}
	try:
		response_json = json.loads(html)
	except ValueError:
		print("Value Error: Error when decoding JSON")
		print(html)
	return response_json['movie_id'], response_json['movie'], response_json['cover']
##
# Returns a list of movie id for a specific filters
# returns json decoded of the response from the server
##
def apply_filter(filters):
	API_URL = 'http://www.einthusan.com/webservice/filters.php'
	result = HTTPInterface.http_post(API_URL, data=filters)
	response_json = {}
	try:
		response_json = json.loads(result)
	except ValueError:
		print("Value Error: Error when decoding JSON")
		print(result)
	return  response_json

def get_options(attr, language):
	API_URL = 'http://www.einthusan.com/webservice/discovery.php'
	data = 'lang='+language

	html = HTTPInterface.http_post(API_URL, data=data)
	result = {}
	try:
		print(result)
		result = json.loads(html)
		return result['organize'][attr]['filtered']
	except KeyError:
		print("Key Error")
	except ValueError:
		print("Value Error: Error when decoding JSON")
		print(html)
	return {}
	
##
# Returns the list of actors from the API endpoint.
##
def get_actor_list(language):
	return get_options('Cast', language)

##
# Returns the list of years available from the API endpoint.
##
def get_year_list(language):
	return get_options('Year', language)

##
# Retuns the list of directors available from the JSON API.
##
def get_director_list(language):
	return get_options('Director', language)