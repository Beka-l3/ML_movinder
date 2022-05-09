# importing the requests library
import requests
import json
# api-endpoint
URL = "http://192.168.1.56:5000/get_recommendation"
  
# location given here
location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API
PARAMS = {'recommend_on': json.dumps([]), 'movie_exceptions': json.dumps(['62740938459a7d03615407b7', '62740938459a7d03615407b7'])}
  
# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)
  
# extracting data in json format
data = r.json()

print(data)
  