from dash import html
import dash_bootstrap_components as dbc

def sidebar():
    return html.Div([
        html.Img(src="/assets/Iconsdg.png", style={'width': '80%', 'margin': '10px auto', 'display': 'block', 'opacity': '1'}),
        html.Hr(style={'borderColor': 'white', 'margin': '10px 0'}),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact", style={'color': 'white', 'fontSize': '18px', 'padding': '10px'}),
                dbc.NavLink("GDP Map", href="/gdp-map", active="exact", style={'color': 'white', 'fontSize': '18px', 'padding': '10px'}),
                dbc.NavLink("Income Map", href="/income-map", active="exact", style={'color': 'white', 'fontSize': '18px', 'padding': '10px'}),
                dbc.NavLink("Salary Map", href="/salary-map", active="exact", style={'color': 'white', 'fontSize': '18px', 'padding': '10px'}),
                dbc.NavLink("MPI Map", href="/mpi-map", active="exact", style={'color': 'white', 'fontSize': '18px', 'padding': '10px'}),
                dbc.NavLink("GDP Forecasting", href="/forecasting", active="exact", style={'color': 'white', 'fontSize': '18px', 'padding': '10px'}),
                dbc.NavLink("Income Forecasting", href="/incForecasting", active="exact", style={'color': 'white', 'fontSize': '18px', 'padding': '10px'})
            ],
            vertical=True,
            pills=True,
        ),
    ], style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '200px',
        'padding': '0px',
        'backgroundColor': '#d5bdaf'
    })
