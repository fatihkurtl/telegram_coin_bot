import requests
import matplotlib.pyplot as plt

data = str(input("Coin: "))
url = f'https://api.coingecko.com/api/v3/coins/{data}/market_chart'
vs_currency = 'usd'
days = 30
params = {
    'vs_currency': vs_currency,
    'days': days
}

headers = {
    'Content-Type': 'application/json',
    'X-CoinAPI-Key': 'YOUR_API_KEY'
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

prices = data['prices']
timestamps = [price[0] for price in prices]
values = [price[1] for price in prices]

plt.plot(timestamps, values)
plt.title(f'{data} fiyatı ({vs_currency})')
plt.xlabel('Tarih')
plt.ylabel('Fiyat')
plt.show()
