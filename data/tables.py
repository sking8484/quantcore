import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.figure_factory as ff


def make_stock_table(database, ticker):
    database.reset_index(inplace = True)
    database = database[:50]
    table = ff.create_table(database)
    table_div = pyo.plot(table, output_type = 'div', include_plotlyjs=False)
    return table_div
