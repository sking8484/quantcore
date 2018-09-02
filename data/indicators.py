import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
import numpy as np

def moving_averages(database):
    database['EMA_200'] = database['Adj. Close'].ewm(span=200).mean()
    database['EMA_100'] = database['Adj. Close'].ewm(span=100).mean()
    database['EMA_50'] = database['Adj. Close'].ewm(span=50).mean()
    moving_avarages = database[['EMA_200', 'EMA_100', 'EMA_50']]
    return moving_avarages
