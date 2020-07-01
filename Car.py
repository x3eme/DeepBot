import pandas as pd
import matplotlib.pyplot as plt
from ta import add_all_ta_features
from ta.utils import dropna
from ta.volatility import BollingerBands
from datetime import datetime
import plotly
go = plotly.graph_objs





data = pd.read_csv("data/Binance_BTCUSDT_1h.csv").head(100)
data = data.iloc[::-1]
btc_data = dropna(data)

# Define the parameters for the Bollinger Band calculation
ma_size = 20
bol_size = 2

# Convert the timestamp data to a human readable format
btc_data.index = btc_data['Date']

# Calculate the SMA
btc_data.insert(0, 'moving_average', btc_data['Close'].rolling(ma_size).mean())

# Calculate the upper and lower Bollinger Bands
btc_data.insert(0, 'bol_upper', btc_data['moving_average'] + btc_data['Close'].rolling(ma_size).std() * bol_size)
btc_data.insert(0, 'bol_lower', btc_data['moving_average'] - btc_data['Close'].rolling(ma_size).std() * bol_size)
btc_data.insert(0, 'Action', 0)
btc_data.insert(0, 'trade_price', 0)


# btc_data['action'] = None

# Remove the NaNs -> consequence of using a non-centered moving average
# btc_data.dropna(inplace=True)

# Create an interactive candlestick plot with Plotly
# fig = go.Figure(data=[go.Candlestick(x=btc_data.index,
#                                      open=btc_data['Open'],
#                                      high=btc_data['High'],
#                                      low=btc_data['Low'],
#                                      showlegend=False,
#                                      close=btc_data['Close'])])

# Plot the three lines of the Bollinger Bands indicator
# for parameter in ['moving_average', 'bol_lower', 'bol_upper']:
#     fig.add_trace(go.Scatter(
#         x=btc_data.index,
#         y=btc_data[parameter],
#         showlegend=False,
#         line_color='blue',
#         mode='lines',
#         #line={'solid': 'solid'},
#         marker_line_width=2,
#         marker_size=10,
#         opacity=0.8))

# Add title and format axes
# fig.update_layout(
#     title=' Bollinger Bands',
#     yaxis_title='BTC/USD')
#
# fig.show()


# dt=[go.Candlestick(x=data['Date'],
#                 open=data['Open'],
#                 high=data['High'],
#                 low=data['Low'],
#                 close=data['Close'])]
#
# figSignal = go.Figure(data=dt)
# figSignal.show()
balance = 15000


def bollrsi_strategy(df: pd.DataFrame):
    global balance
    global fig
    position = False
    for index,row in df.iterrows():
        h:float = df.loc[index,'High']
        l:float = df.loc[index,'Low']
        bl:float = df.loc[index,'bol_lower']
        bh:float = df.loc[index,'bol_upper']
        close: float = df.loc[index, 'Close']



        if h>=bh and position:
            balance = balance +bh
            position = False
            print('sold - > sold at: {} balance: {}'.format(bh, balance))
            df.at[index,'trade_price']=bh
            df.at[index,'Action']=2


        elif l<=bl and not position:
            print('buy: {}'.format(close))
            balance = balance-bl
            position = True
            df.at[index, 'trade_price'] = bl
            df.at[index,'Action']=1

        else:
            df.at[index, 'trade_price'] = None
    #print(df)
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                        open=df['Open'],
                                        high=df['High'],
                                        low=df['Low'],
                                        showlegend=False,
                                        close=df['Close'])])
    # Plot the three lines of the Bollinger Bands indicator
    for parameter in ['moving_average', 'bol_lower', 'bol_upper']:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[parameter],
            showlegend=False,
            line_color='blue',
            mode='lines',
            line={'dash': 'solid'},
            marker_line_width=2,
            marker_size=10,
            opacity=0.8))


    for i in df.index:
        print(df['Action'])
        if df.at[i, 'Action'] == 1:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['trade_price'],
                showlegend=False,
                line_color='green',
                mode='markers',
            ))
        else:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['trade_price'],
                showlegend=False,
                line_color='black',
                mode='markers',
            ))

    # for parameter in ['trade_price']:
    #     #if (df[parameter] != 0):
    #     if df.at[index, 'Action'] == 1:
    #         fig.add_trace(go.Scatter(
    #             x=df.index,
    #             y=df[parameter],
    #             showlegend=False,
    #             line_color='green',
    #             mode='markers',
    #             #line={'dash':'solid'},
    #             #marker_line_width=4,
    #             #marker_size=10,
    #             #opacity=0.8
    #         ))
    #     else:
    #         print("t " + str(df.at[index, 'Action']))
    #         fig.add_trace(go.Scatter(
    #             x=df.index,
    #             y=df[parameter],
    #             showlegend=False,
    #             line_color='black',
    #             mode='markers',
    #             #line={'dash':'solid'},
    #             #marker_line_width=4,
    #             marker_size=5
    #             #opacity=0.8
    #         ))




    #Add title and format axes
    fig.update_layout(
        title=' Bollinger Bands',
        yaxis_title='BTC/USD')

    fig.show()









bollrsi_strategy(btc_data)