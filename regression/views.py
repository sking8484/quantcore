from django.shortcuts import render
from data import views as data_views
from . import plots

import pandas as pd
import pandas_datareader as web
from datetime import datetime
import quandl
import numpy as np
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import plotly.offline as po
import plotly.graph_objs as go
import statsmodels.formula.api as sm

def regression_home(request):
    return render(request, 'regression/regression.html')

def simple_regression(request):
    if request.method == "POST":
        try:
            """GETTING THE DATA"""
            datatype_1 = request.POST['datatype1']
            datatype_2 = request.POST['datatype2']
            ticker1 = request.POST['symbol1'].upper()
            ticker2 = request.POST['symbol2'].upper()
            start = pd.to_datetime(request.POST['start'])
            end = pd.to_datetime(request.POST['end'])
            # try:
            if datatype_1 == 'stock_data':
                y = data_views.get_stock_data(datatype_1, ticker1, start, end)
                y = y['Adj. Close']
                y.rename(ticker1, inplace = True)

            if datatype_1=='real_estate':
                y = data_views.get_stock_data(datatype_1,ticker1,start,end)
                y.columns = ([ticker1])
            if datatype_1 == 'economic':
                y = data_views.get_stock_data(datatype_1, ticker1, start, end)
                y.columns = ([ticker1])

            if datatype_2 == 'stock_data':
                X = data_views.get_stock_data(datatype_2, ticker2, start, end)
                X = X['Adj. Close']
                X.rename(ticker2, inplace = True)

            if datatype_2 == 'real_estate':
                X = data_views.get_stock_data(datatype_2,ticker2,start,end)
                X.columns = ([ticker2])
            if datatype_2 == 'economic':
                X = data_views.get_stock_data(datatype_2, ticker2, start, end)
                X.columns = ([ticker2])



            """ACTUAL REGRESSION PART"""

            dataframe = pd.DataFrame(X)
            dataframe = dataframe.join(y, how = 'outer')
            dataframe = dataframe.sort_index(ascending = False)
            dataframe.dropna(inplace = True)
            print(dataframe)

            X = dataframe.iloc[:,:1]
            X_name = dataframe.columns[0]
            y_name = dataframe.columns[1]
            y = dataframe.iloc[:,-1]


            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=0)
            from sklearn.linear_model import LinearRegression
            regressor = LinearRegression()
            regressor.fit(X_train, y_train)
            y_pred = regressor.predict(X_train)


            regression_plot = plots.plot_regression(X_test, X_train, y_train, y_test, y_pred, X_name, y_name)
            X = np.append(arr = np.ones((len(X), 1)).astype(int), values =X , axis = 1)
            regressor_OLS = sm.OLS(endog=y , exog=X).fit()
            summary = regressor_OLS.summary().as_html()
        except Exception as e:
            print(e)
            help = (
            ' Make sure the data from quandl has enough entries.' +
            'and type in your area if you are unsure how to find the correct real estate code. Copy and paste the key into ticker.')
            return render(request,'regression/regression.html', {'help':help})

        return render(request, 'regression/simple_regression.html', {'regression_plot':regression_plot,
                                                                    'summary':summary})
    return render(request, 'regression/regression.html')
