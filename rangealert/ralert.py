import ta
import plotly.graph_objects as go
import pandas as pd

class range_screen():
    ''' using donchian channels to alert when market may breakout '''
    def __init__(self):
        self.last_open = None
        self.last_high = None
        self.last_low = None
        self.last_close = None
        self.last_tradingDay = None
        self.last_atr = None
        self.avelow = None
        self.avehigh = None
        self.avemidprice = None
        self.rangemaxprice = None
        self.rangeminprice = None
        self.last_maxprice = None
        self.last_minprice = None
        self.last_upb = None
        self.last_lpb = None
        self.last_atr = None
        self.upb = None
        self.lpb = None

    def range_trading(self, df, symbol, atr_window=14, range_periods=20, atrmultiple_test=1.5, create_chart=False):
        ''' identify range trading markets '''
        self.last_open = df.Open[-1]
        self.last_high = df.High[-1]
        self.last_low = df.Low[-1]
        self.last_close = df.Close[-1]
        self.last_tradingDay = df.index[-1]

        self.avehigh = df['High'].rolling(range_periods).mean()
        self.avelow = df['Low'].rolling(range_periods).mean()
        self.avemidprice = (self.avehigh + self.avelow) / 2

        # get upper and lower bounds to compare to period highs and lows
        indicator_atr = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close'], window=atr_window, fillna=False)
        self.atr = indicator_atr.average_true_range()
        self.last_atr = self.atr[-1]

        self.upb = self.avemidprice + atrmultiple_test * self.atr
        self.lpb = self.avemidprice - atrmultiple_test * self.atr
        self.last_upb = self.upb[-1]
        self.last_lpb = self.lpb[-1]

        # get the period highs and lows
        self.rangemaxprice = df['High'].rolling(range_periods).max()
        self.rangeminprice = df['Low'].rolling(range_periods).min()
        self.last_maxprice = self.rangemaxprice[-1]
        self.last_minprice = self.rangeminprice[-1]

        if create_chart:
            chart = self.get_range_plot(df, symbol, self.upb, self.lpb, self.rangemaxprice, self.rangeminprice)
        else:
            chart = None

        if self.last_maxprice < self.last_upb and self.last_maxprice > self.last_lpb and self.last_minprice < self.last_upb and self.last_minprice > self.last_lpb:
            return 1, chart
        else:
            return 0, chart


    def get_range_plot(self, dfp, symbol, upb, lpb, rangemaxprice, rangeminprice):
        ''' plotly candlestick chart '''
        fig = go.Figure()
        trace1=go.Candlestick(x=dfp.index, open=dfp['Open'], high=dfp['High'], low=dfp['Low'], close=dfp['Close'], name=symbol)
        trace2 = go.Scatter(x=upb.index, y=upb.values, mode='lines', line_color='blue', name='Upper test band')
        trace3 = go.Scatter(x=lpb.index, y=lpb.values, mode='lines', line_color='blue', name='Lower test band')
        trace4 = go.Scatter(x=rangemaxprice.index, y=rangemaxprice.values, mode='lines', line_color='black', name='Period max price')
        trace5 = go.Scatter(x=rangeminprice.index, y=rangeminprice.values, mode='lines', line_color='black', name='Period min price')

        fig.add_trace(trace1)
        fig.add_trace(trace2)
        fig.add_trace(trace3)
        fig.add_trace(trace4)
        fig.add_trace(trace5)

        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(
        title='Range Trading Analysis: ' + symbol,
        xaxis_title="Date",
        yaxis_title="Price")
        return fig
