import requests
import json

class Products:
	#This gets you a random product name and image.
	def get_random_products(self):
		url = "https://the-cocktail-db.p.rapidapi.com/randomselection.php"

		headers = {
			"X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com",
			"X-RapidAPI-Key": "eff52018ddmshba57fe675624e94p169c8ajsn5685027421e4"
			}
		response = requests.request("GET", url, headers=headers)
		data = response.text
		data1 = json.loads(data)
		return data1
	
	def search_cocktail(self):
		
		url = "https://the-cocktail-db.p.rapidapi.com/search.php"

		querystring = {"i":"vodka"}

		headers = {
			"X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com",
			"X-RapidAPI-Key": "eff52018ddmshba57fe675624e94p169c8ajsn5685027421e4"
		}

		response = requests.request("GET", url, headers=headers, params=querystring)
		data = response.text
		data1 = json.loads(data)
		return data1

	def lookupdrinks(self,id):
		url = "https://the-cocktail-db.p.rapidapi.com/lookup.php"
		querystring = {"i":id}
		headers = {
			"X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com",
			"X-RapidAPI-Key": "eff52018ddmshba57fe675624e94p169c8ajsn5685027421e4"
			}
		response = requests.request("GET", url, headers=headers, params=querystring)
		data = response.text
		data1 = json.loads(data)
		return data1



