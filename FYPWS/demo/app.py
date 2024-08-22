from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import your layout functions and callbacks
from home import home_layout, update_graph
from mpi_map import mpi_map_layout, register_callbacks as mpi_register_callbacks
from salary_map import salary_map_layout, register_callbacks as salary_register_callbacks
from income_map import income_map_layout, register_callbacks as income_register_callbacks
from GDP_map import gdp_map_layout, register_callbacks as gdp_register_callbacks
from forecast import forecasting_layout, register_forecasting_callbacks
from incomeforecast import incForecasting_layout, inc_register_forecasting_callbacks 
from sidebar import sidebar

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        sidebar(),
        html.Div(id='page-content', style={'margin-left': '20%', 'backgroundColor': '#f5ebe0', 'padding': '20px'})
    ], style={'backgroundColor': '#f5ebe0'})
], style={'backgroundColor': '#f5ebe0'})

# Register callbacks for each page
mpi_register_callbacks(app)
salary_register_callbacks(app)
income_register_callbacks(app)
gdp_register_callbacks(app)
register_forecasting_callbacks(app)
inc_register_forecasting_callbacks(app)

# Callback to navigate between pages
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/salary-map':
        return salary_map_layout()
    elif pathname == '/mpi-map':
        return mpi_map_layout()
    elif pathname == '/income-map':
        return income_map_layout()
    elif pathname == '/gdp-map':
        return gdp_map_layout()
    elif pathname == '/forecasting':
        return forecasting_layout()
    elif pathname == '/incForecasting':
        return incForecasting_layout()
    else:
        return home_layout()

# Define the callback to update the graph based on the selected metric
@app.callback(
    Output('bar-plot', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_graph_callback(selected_metric):
    return update_graph(selected_metric)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
