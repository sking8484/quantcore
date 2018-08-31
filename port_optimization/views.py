from django.shortcuts import render
from data import views as data_views
from datetime import datetime
import pandas as pd
import numpy as np
from . import tables
from . import plots

global_portfolio_optimal_non_optimal = pd.DataFrame()

def optimize(request):
    if request.method == "POST":
        try:
            tickers = request.POST['Tickers']

            tickers = tickers.upper()



            print(tickers)
            print(type(tickers))
            if type(tickers) != list:
                if "'" in tickers:
                    tickers = tickers.replace("'", '')
                tickers = tickers.replace(',  ', ', ')
                tickers = str(tickers)
                tickers = tickers.split(', ')

                tickers = list(tickers)

            amount = request.POST['Amount']

            # start = datetime.strptime(request.POST['start'],'%Y-%m-%d')
            start = pd.to_datetime(request.POST['start'])
            # if len(tickers) > 7:
            #     start = pd.to_datetime('2013-06-01')
            if len(tickers) > 30:
                tickers = tickers[:30]
            start = pd.to_datetime('2015-06-01')
            tickers = tickers


            end = pd.to_datetime(request.POST['end'])
            datatype = 'stock_data'
            database = pd.DataFrame()
            """NON OPTIMAL PORTFOLIO"""

            for ticker, allocation in zip(tickers, [1/len(tickers) for ticker in tickers]):
                data = data_views.get_stock_data(datatype, ticker, start, end)
                data = data.loc[:, ['Adj. Close']]

                data.rename(columns = {'Adj. Close':ticker}, inplace = True)
                data[ticker + ' Normed_Returns'] = data[ticker]/data[ticker].iloc[0]
                data[ticker + ' Allocation'] = data[ticker + ' Normed_Returns']*allocation
                data[ticker + ' Position_values'] = data[ticker + ' Allocation']*int(amount)
                database = database.join(data, how = 'outer')
                database.dropna(inplace = True)


            non_optimal_position_val = pd.DataFrame()
            for ticker in tickers:
                non_optimal_position_val = pd.concat([non_optimal_position_val, database[ticker + ' Position_values']],axis = 1)

            non_optimal_position_val['Total_position'] = non_optimal_position_val.sum(axis=1)

            """CALCULATE LOG RETURNS"""
            log_df = pd.DataFrame()
            for ticker in tickers:
                log_df = pd.concat([log_df, database[ticker]], axis = 1)

            log_ret = np.log(log_df/log_df.shift(1))



            """OPTIMIZATION"""
            if len(tickers) > 10:
                num_ports = 5000
            num_ports = 8000
            all_weights = np.zeros((num_ports, len(tickers)))
            ret_arr = np.zeros(num_ports)
            vol_arr = np.zeros(num_ports)
            sharpe_arr = np.zeros(num_ports)

            for ind in range(num_ports):
                weights = np.array(np.random.random(len(tickers)))
                weights = weights/np.sum(weights)

                all_weights[ind,:] = weights

                ret_arr[ind] = np.sum((log_ret.mean() * weights) * 252)
                vol_arr[ind]= np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))

                sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]
            max_sharpe = sharpe_arr.argmax()
            optimized_weights = all_weights[max_sharpe,:]
            sharpe_ratio = sharpe_arr[max_sharpe].round(3)
            max_ret = ret_arr[max_sharpe]
            max_vol = vol_arr[max_sharpe]
            bullet = plots.market_bullet(vol_arr, ret_arr, sharpe_arr, max_vol, max_ret)
            weights_ticks_df = pd.DataFrame()

            opt_weights_series = pd.Series(optimized_weights, name='Weights')
            tickers_series = pd.Series(tickers, name = 'Tickers')
            weights_ticks_df = pd.concat([weights_ticks_df,tickers_series, opt_weights_series ], axis = 1)





            """OPTIMAL PLOT"""
            datatype = 'stock_data'
            database = pd.DataFrame()

            for ticker, allocation in zip(tickers, optimized_weights):
                data = data_views.get_stock_data(datatype, ticker, start, end)
                data = data.loc[:, ['Adj. Close']]
                data.rename(columns = {'Adj. Close':ticker}, inplace = True)
                data[ticker + ' Normed_Returns'] = data[ticker]/data[ticker].iloc[0]
                data[ticker + ' Allocation'] = data[ticker + ' Normed_Returns']*allocation
                data[ticker + ' Position_values'] = data[ticker + ' Allocation']*int(amount)
                database = database.join(data, how = 'outer')
                database.dropna(inplace = True)
            optimal_position_val = pd.DataFrame()
            for ticker in tickers:
                optimal_position_val = pd.concat([optimal_position_val, database[ticker + ' Position_values']],axis = 1)

            optimal_position_val['Total_position'] = optimal_position_val.sum(axis=1)


            portfolio_plot = plots.optimal_plot(non_optimal_position_val['Total_position'], optimal_position_val['Total_position'])


            portfolio_table = pd.concat([optimal_position_val['Total_position'].round(2),non_optimal_position_val['Total_position'].round(2)],axis = 1)

            portfolio_table.columns = ['Optimal Position Value','Non Optimal Position Value']
            global global_portfolio_optimal_non_optimal
            global_portfolio_optimal_non_optimal = portfolio_table
            placeholder = optimal_portfolio_global_holder()


            portfolio_table['Difference'] = portfolio_table['Optimal Position Value'] - portfolio_table['Non Optimal Position Value']
            table = tables.make_stock_table(portfolio_table.round(2))

            weights_table = tables.weights(weights_ticks_df.round(2))


            return render(request, 'port_optimization/optimized.html', {'sharpe_ratio':sharpe_ratio, 'weights_table':weights_table,'table':table,'tickers':tickers, 'portfolio_plot':portfolio_plot, 'bullet':bullet})

        except Exception as e:
            error_message = e
            error = 'One or more of your inputs was not accepted: '
            return render(request, 'port_optimization/optimization_form.html', {'error':error, 'error_message':error_message})
    return render(request, 'port_optimization/optimization_form.html')

def optimal_portfolio_global_holder():
    global_variable_holding = global_portfolio_optimal_non_optimal
    return global_variable_holding


def get_optimal_portfolio_table():
    global_portfolio_money = optimal_portfolio_global_holder()

    return global_portfolio_money
