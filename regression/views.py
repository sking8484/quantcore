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
from port_optimization import views as port_views

def regression_home(request):
    return render(request, 'regression/regression.html')

def simple_regression(request):
    if request.method == "POST":
        try:

            if request.POST['datatype1'] == 'run':
                port_regression = request.POST['datatype1']

                data = request.session['global_portfolio_optimal_non_optimal']
                data = pd.read_json(data)
                data['Returns'] = data['Optimal Position Value']
                y = data['Returns']

                X = data_views.get_stock_data('stock_data', 'SPY', pd.to_datetime('12-12-2010'), datetime.now())
                X['Returns'] = X['close']

                X = X['Returns']
                X.rename('SP500', inplace = True)
            elif request.POST['datatype1'] == 'do_not_run':
                return render(request, 'port_optimization/optimization_form.html')


            else:

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
                    y = y['close']
                    y.rename(ticker1, inplace = True)

                if datatype_1=='real_estate':
                    y = data_views.get_stock_data(datatype_1,ticker1,start,end)
                    y.columns = ([ticker1])
                if datatype_1 == 'economic':
                    y = data_views.get_stock_data(datatype_1, ticker1, start, end)
                    y.columns = ([ticker1])

                if datatype_2 == 'stock_data':
                    X = data_views.get_stock_data(datatype_2, ticker2, start, end)
                    X = X['close']
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
            y_pred = regressor.predict(X_test)


            regression_plot = plots.plot_regression(X_test, X_train, y_train, y_test, y_pred, X_name, y_name)
            X = np.append(arr = np.ones((len(X), 1)).astype(int), values =X , axis = 1)
            regressor_OLS = sm.OLS(endog=y , exog=X).fit()
            summary = regressor_OLS.summary().as_html()
            beta_value = regressor_OLS.params[1]
        except Exception as e:
            error_message = e
            error = 'One or more of your inputs was not accepted: '
            return render(request,'regression/regression.html', {'error':error, 'error_message':error_message})

        return render(request, 'regression/simple_regression.html', {'beta_value':beta_value, 'regression_plot':regression_plot,
                                                                    'summary':summary})
    return render(request, 'regression/regression.html')
