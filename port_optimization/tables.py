import plotly.figure_factory as ff
import plotly.offline as po
import plotly.graph_objs as go


def make_stock_table(database):
    database.sort_index(ascending = False, inplace = True)
    database.reset_index(inplace = True)
    database = database

    table = ff.create_table(database)
    table_div = po.plot(table, output_type = 'div', include_plotlyjs=False)
    return table_div[:256]

def weights(database):
    database.sort_index(ascending = True, inplace = True)
    table = ff.create_table(database)
    table_div = po.plot(table, output_type = 'div', include_plotlyjs=False)
    return table_div
