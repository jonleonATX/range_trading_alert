This module is not intended as advice to trade, it is for use in your trading analyses and algorithms. Use at your own risk.

This screener attempts to find range bound markets based on given inputs.

**Required data:**

-Pandas dataframe containing index as datetime and columns (High, Low, Open, Close) as float
-Define the number of breakout periods (default: 55 periods)
-Average True Range (ATR) window (default: 14 periods)
-ATR multiple (default: 1.5)- sensitivity used to determine a level at which the alert will provide a range signal

**Response:**

The response returned is a tuple of the signal and a plotly chart: (signal, chart) create_chart=False is default. The signal is one of three options: 1, 0

  * 1 - trading in a range
  * 0 - not trading in a range

**Dependencies:**

- pandas
- ta
- plotly

**Install module:**

https://pypi.org/project/rangealert/

pip install rangealert

**Detailed documentation:**

https://github.com/jonleonATX/range_trading_alert/blob/master/rangealert.ipynb
