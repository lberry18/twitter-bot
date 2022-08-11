from warnings import catch_warnings
import requests
import tweepy

#following code opens up text file containing API keys for twitter developer account
all_keys = open('keys.txt', 'r').read().splitlines()
api_key = all_keys[0]
api_secret_key = all_keys[1]
access_token = all_keys[2]
access_secret_token = all_keys[3]

#following code opens up text file containing API weather request
weather_API = open('weatherApiKey.txt', 'r').read().splitlines()
weather_API = weather_API[0]

#code used to authenticate with twitter API
authenticator = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_secret_token)
api = tweepy.API(authenticator, wait_on_rate_limit=True)

#following code is used to get data by city names from the weather API
url = "https://api.ambeedata.com/latest/by-city"
cities = ["New York City", "Los Angeles", "Chicago", "Houston", "Phoenix"]
headers = {
    'x-api-key': weather_API,
    'Content-type': "application/json"
    }

#empty array to hold return values from API call
tweet = []

#following code loops through the length of array the cities are stored in and pulls the API retuen data from the json file and stores it in the empty array
for i in range(len(cities)):
    querystring = {"city":cities[i]}
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    city = response["stations"][0]["state"]
    aqi = response["stations"][0]["AQI"]
    category = response["stations"][0]["aqiInfo"]["category"]

    print(cities[i] , "Air quailty index is:" , aqi , "Condition:" , category)
    tweet += [cities[i] + " Air quality index is: " + str(aqi) + ", Condition: " + category]

print(tweet)

#this part just splits up the array by lines
formatted_list = '\n'.join(tweet)

print(formatted_list)

#this is the call to post data to the twiiter feed
api.update_status(formatted_list)