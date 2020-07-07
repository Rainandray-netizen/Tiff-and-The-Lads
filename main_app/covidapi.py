import requests
import json

def fetch_all_stats():
  data = requests.get('https://api.covid19api.com/summary')
  parsed = json.loads(data.text)

  return(parsed['Global'])

def fetch_countries():
  data = requests.get('https://api.covid19api.com/summary')
  parsed = json.loads(data.text)

  countries_list=[{'Name' : country['Country'], 'TotalConfirmed' : country['TotalConfirmed']} for country in parsed['Countries']]
  print(countries_list)
  return countries_list


country_stats_list = fetch_countries()
global_stats = fetch_all_stats
