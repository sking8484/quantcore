import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.figure_factory as ff

def correlation_heatmap(database):
    data = [go.Heatmap(x=database.columns,y=database.columns, z=database.values.tolist(), colorscale='Jet')]
    layout = go.Layout(title = 'Correlation Heat Map')
    fig = go.Figure(data=data, layout=layout)
    heatmap = pyo.plot(fig, output_type = 'div', include_plotlyjs= False)
    return heatmap

def correlation_plot(database):
    cols = database.columns
    trace1 = go.Scatter(x=database.index, y=database[cols[0]],
                        mode='lines',
                        name = cols[0])

    trace2 = go.Scatter(x=database.index, y=database[cols[1]],
                        mode='lines',
                        name=cols[1])
    data = [trace1, trace2]
    if len(cols) == 3:
        trace3 = go.Scatter(x=database.index, y=database[cols[2]],
                            mode='lines',
                            name = cols[2])
        data.append(trace3)
    if len(cols) ==4:
        trace3 = go.Scatter(x=database.index, y=database[cols[2]],
                            mode='lines',
                            name = cols[2])
        trace4 = go.Scatter(x=database.index, y=database[cols[3]],
                            mode = 'lines',
                            name = cols[3])
        data.append(trace3)
        data.append(trace4)


    layout = go.Layout(title = ('Plot with ' + str(cols[:])), xaxis={'title':'Date'}, yaxis={'title':'Price'})
    fig = go.Figure(data=data, layout=layout)
    plot_div = pyo.plot(fig, output_type='div',include_plotlyjs=False)
    return plot_div
