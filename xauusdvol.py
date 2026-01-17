import numpy as np
from polygon import RESTClient
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

API_KEY = 'O8bUajLRgDB2G_ndsRdUptEgw0MKdZL4'

client = RESTClient(api_key=API_KEY)

from_date = '2020-01-01'
to_date = datetime.now().strftime('%Y-%m-%d')
aggs = client.get_aggs(ticker='C:XAUUSD', multiplier=1, timespan='day', from_=from_date, to=to_date, limit=50000)

data = pd.DataFrame(aggs)
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
data.set_index('timestamp', inplace=True)
data = data[['close']] 
data.rename(columns={'close': 'Close'}, inplace=True)

data['Log_Return'] = np.log(data['Close'] / data['Close'].shift(1))

windows = [10, 20, 30, 60, 90, 120, 252] 
vol_data = pd.DataFrame(index=data.index)
for w in windows:
    vol_data[f'Vol_{w}d'] = data['Log_Return'].rolling(window=w).std() * np.sqrt(252)

vol_data.dropna(inplace=True)

time_numeric = np.arange(len(vol_data))
time_mesh, window_mesh = np.meshgrid(time_numeric, windows)
Z = vol_data.values.T 

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(time_mesh, window_mesh, Z, cmap='viridis')
ax.set_xlabel('Temps (jours depuis le début)')
ax.set_ylabel('Fenêtre glissante (jours)')
ax.set_zlabel('Volatilité annualisée')
ax.set_title('Surface 3D de la volatilité du XAUUSD')
plt.show()

vol_data.to_csv('xauusd_volatility.csv')
plt.savefig('volatility_3d.png')