import plotly.graph_objs as go
import plotly.offline as po
import pandas as pd
import pandas_datareader as web
from datetime import datetime
import quandl
import numpy as np
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

def plot_regression(X_test, X_train, y_train, y_test, y_pred, X_name, y_name):
    trace1 = go.Scatter(x = X_train.squeeze(), y = y_train.squeeze(), mode = 'markers',name = 'Given Data', marker = {'color':'rgba(152, 0, 0, .8)'} )
    trace2 = go.Scatter(x = X_train.squeeze(), y = y_pred, mode = 'lines', name = 'Linear Prediction')
    trace3 = go.Scatter(x = X_test.squeeze(), y = y_test.squeeze(), mode = 'markers',name = 'Values Unknow Prior to Fit', marker = {'color':'#FFBAD2'})
    data = [trace1, trace2, trace3]
    layout = go.Layout(title = 'simple regression', xaxis={'title':X_name}, yaxis={'title':y_name})
    fig = go.Figure(data=data, layout=layout)
    regression = po.plot(fig, output_type = 'div', include_plotlyjs= False)
    return regression
