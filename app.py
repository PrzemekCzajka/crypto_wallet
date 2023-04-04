from flask import Flask, render_template
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    bnb_price = get_price('BNBUSDT')
    bnb_data = get_historical_data('BNBUSDT')
    bnb_plot = generate_plot('BNB', bnb_data)

    algo_price = get_price('ALGOUSDT')
    algo_data = get_historical_data('ALGOUSDT')
    algo_plot = generate_plot('ALGO', algo_data)

    eth_price = get_price('ETHUSDT')
    eth_data = get_historical_data('ETHUSDT')
    eth_plot = generate_plot('ETH', eth_data)

    xrp_price = get_price('XRPUSDT')
    xrp_data = get_historical_data('XRPUSDT')
    xrp_plot = generate_plot('XRP', xrp_data)

    btc_price = get_price('BTCUSDT')
    btc_data = get_historical_data('BTCUSDT')
    btc_plot = generate_plot('BTC', btc_data)

    return render_template('index.html', algo_price=algo_price, bnb_price=bnb_price, btc_price=btc_price, eth_price=eth_price, xrp_price=xrp_price, btc_plot=btc_plot, eth_plot=eth_plot, xrp_plot=xrp_plot, bnb_plot=bnb_plot, algo_plot=algo_plot)

def get_price(symbol):
    response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}')
    data = response.json()
    price = float(data['price'])
    return price

def get_historical_data(symbol, interval='2h', limit=72):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    response = requests.get(url)
    data = response.json()
    prices = [float(entry[4]) for entry in data]
    times = [datetime.fromtimestamp(entry[0] / 1000) for entry in data]
    return {'prices': prices, 'times': times}

def generate_plot(symbol, data):
    plt.style.use('ggplot')
    plt.figure(figsize=(7, 3))
    plt.plot(data['times'], data['prices'],)
    plt.xlabel('Czas')
    plt.xticks(fontsize=8)
    plt.ylabel('Cena (USD)')
    plt.title(f'Poziom ceny {symbol} z ostatnich 24h')
    plt.grid(True)
    plt.tight_layout()
    min_price = min(data['prices'])
    max_price = max(data['prices'])
    plt.annotate(f"Min: {min_price:.4f}", xy=(data['times'][data['prices'].index(min_price)], min_price), 
                 xytext=(-20, 10), textcoords='offset points', color='red')
    plt.annotate(f"Max: {max_price:.4f}", xy=(data['times'][data['prices'].index(max_price)], max_price), 
                 xytext=(-20, -20), textcoords='offset points', color='green')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return f"data:image/png;base64,{image_base64}"

if __name__ == '__main__':
    app.run(debug=True)
