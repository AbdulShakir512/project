import requests

url = "https://api.apilayer.com/exchangerates_data/convert?to=aed&from=&amount=1"

payload = {}
headers= {
  "apikey": "h0KlbgndrZNf211bIwWH3dYHNE9F7YtA"
}



response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text
