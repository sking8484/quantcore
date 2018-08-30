import plotly.offline as po
import plotly.graph_objs as go
import pandas as pd
import numpy as np

def optimal_plot(non_optimal, optimal):
    trace1 = go.Scatter(x=non_optimal.index, y=non_optimal, mode = 'lines', name = 'Non Optimal Portfolio')
    trace2 = go.Scatter(x=optimal.index, y=optimal, mode = 'lines', name = 'Optimized Portfolio')
    data = [trace1, trace2]
    layout = go.Layout(title = 'Optimized Vs. Non Optimized portfolio', xaxis={'title':'Price'}, yaxis={'title':'Date'})
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
