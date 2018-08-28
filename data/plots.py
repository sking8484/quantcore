import plotly.offline as pyo
import plotly.graph_objs as go

def stock_plot(database, ticker):
    index_values = database.index
    close_values = database.iloc[:, 0]

    database['EMA_30'] = database.iloc[:, 0].ewm(span=14).mean().round(4)
    ewm_30 = database['EMA_30']


    trace1 = go.Scatter(x=index_values,
                        y=close_values,
                        mode = 'lines',
                        name='Close')
    trace2 = go.Scatter(x=index_values,
                        y=ewm_30,
                        mode = 'lines',
                        name='EWM_30')
    data = [trace1, trace2]
    layout = go.Layout(title = ticker, xaxis={'title':'Date'}, yaxis={'title':'Price'})
    fig = go.Figure(data=data, layout=layout)
    plot_div = pyo.plot(fig, output_type='div',include_plotlyjs=False)
    return plot_div

def real_estate_plot(database, ticker):

    index_values = database.index
    data_values = database['Value']

    data = [go.Scatter(x=index_values,
                        y=data_values,
                        mode = 'lines')]

    layout = go.Layout(title = ticker, xaxis={'title':'Date'}, yaxis={'title':'Price'})
    fig = go.Figure(data=data, layout=layout)
    plot_div = pyo.plot(fig, output_type='div',include_plotlyjs=False)
    return plot_div
