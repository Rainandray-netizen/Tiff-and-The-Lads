import requests
import json

def fetch_all_stats():
  data = requests.get('https://api.covid19api.com/summary')
  parsed = json.loads(data.text)

  return(parsed['Global'])

def fetch_countries():
  data = requests.get('https://api.covid19api.com/summary')
  parsed = json.loads(data.text)

  countries_list=[{'Name' : country['Country'], 'NewConfirmed' : country['NewConfirmed'], 'TotalConfirmed' : country['TotalConfirmed'], 'NewDeaths' : country['NewDeaths'], 'TotalDeaths' : country['TotalDeaths'], 'NewRecovered' : country['NewRecovered'], 'TotalRecovered' : country['TotalRecovered'], 'Updated' : country['Date']} for country in parsed['Countries']]
  return countries_list


country_stats_list = fetch_countries()
global_stats = fetch_all_stats()
