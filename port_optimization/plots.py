import plotly.offline as po
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from data import views as data_views

def optimal_plot(non_optimal, optimal, start, end):
    sp_500 = data_views.get_stock_data('stock_data','SPY', start, end )
    print(type(sp_500))
    non_optimal = (non_optimal/non_optimal[0])*100
    optimal = (optimal/optimal[0])*100
    sp_500 = (sp_500['close']/sp_500['close'][0])*100

    trace1 = go.Scatter(x=non_optimal.index, y=non_optimal, mode = 'lines', name = 'Non Optimal Portfolio')
    trace2 = go.Scatter(x=optimal.index, y=optimal, mode = 'lines', name = 'Optimized Portfolio')
    trace3 = go.Scatter(x = sp_500.index, y=sp_500, mode='lines', name = 'S&P 500')
    data = [trace1, trace2, trace3]
    layout = go.Layout(title = 'Optimized Vs. Non Optimized portfolio', xaxis={'title':'Date'}, yaxis={'title':'Returns %'})
    fig = go.Figure(data=data, layout=layout)
    optimal_plots = po.plot(fig, output_type = 'div', include_plotlyjs= False)
    return optimal_plots


def market_bullet(vol_arr, ret_arr, sharpe_arr, max_vol, max_ret):
    trace1 = go.Scatter(x = vol_arr, y = ret_arr,name='Portfolios' ,mode = 'markers',marker = dict( color = sharpe_arr,colorscale='Viridis',showscale=True))
    trace2 = go.Scatter(x = [max_vol], y= [max_ret], name='Optimal Portfolio', mode = 'markers')
    layout = go.Layout(title='Portfolio Bullet', xaxis={'title':'Volatility'}, yaxis={'title':'Returns'}, legend=dict(x=-.1, y=1.2))
    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    bullet = po.plot(fig, output_type='div',include_plotlyjs=False)
    return bullet
