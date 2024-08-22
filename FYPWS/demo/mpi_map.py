from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from sidebar import sidebar

# Load the data
MPImap = pd.read_csv("MPImap.csv")

def mpi_map_layout():
    return html.Div([
        sidebar(),
        html.Div([
            html.H2("Intensity of Deprivation Map", style={'text-align': 'left'}),
            html.Div([
                html.Div([
                    html.Label("Select Map Type:"),
                    dcc.Dropdown(
                        id='map-type-dropdown',
                        options=[
                            {'label': 'Urban Deprivation', 'value': 'urban'},
                            {'label': 'Rural Deprivation', 'value': 'rural'}
                        ],
                        value='urban',
                        style={'margin-bottom': '0px', 'width': '200px'}
                    ),
                ], style={'display': 'inline-block', 'margin-right': '20px'}),
                html.Div([
                    html.Label("Select Country:"),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': country, 'value': country} for country in MPImap['Country'].unique()],
                        value=None,
                        placeholder='Select a country',
                        style={'margin-bottom': '0px', 'width': '200px'}
                    ),
                ], style={'display': 'inline-block', 'margin-right': '20px'}),
                html.Div([
                    html.Label("Select Sub-national Region:"),
                    dcc.Dropdown(
                        id='subnational-dropdown',
                        options=[],
                        value=None,
                        placeholder='Select a sub-national region',
                        style={'margin-bottom': '0px', 'width': '200px'}
                    ),
                ], style={'display': 'inline-block', 'margin-right': '20px'}),
                html.Div([
                    html.Label("Select Projection Type:"),
                    dcc.Dropdown(
                        id='projection-dropdown',
                        options=[
                            {'label': 'Map View', 'value': 'natural earth'},
                            {'label': 'Globe View', 'value': 'orthographic'}
                        ],
                        value='natural earth',
                        style={'margin-bottom': '0px', 'width': '200px'}
                    ),
                ], style={'display': 'inline-block'})
            ], style={'display': 'flex', 'margin-bottom': '20px'}),
            dcc.Graph(
                id='mpi-intensity-map',
                style={'width': '80%', 'height': '800px', 'margin-right': '20px', 'margin-left': '0px'}
            ),
        ], style={'marginLeft': '-170px', 'width': 'calc(100% - 250px)', 'padding-left': '0px'})
    ], style={'display': 'flex'})

def register_callbacks(app):
    @app.callback(
        Output('subnational-dropdown', 'options'),
        [Input('country-dropdown', 'value')]
    )
    def update_subnational_options(selected_country):
        if selected_country:
            filtered_df = MPImap[MPImap['Country'] == selected_country]
            options = [{'label': region, 'value': region} for region in filtered_df['Sub-national region'].unique()]
        else:
            options = []
        return options

    @app.callback(
        Output('mpi-intensity-map', 'figure'),
        [Input('country-dropdown', 'value'),
         Input('subnational-dropdown', 'value'),
         Input('map-type-dropdown', 'value'),
         Input('projection-dropdown', 'value')]
    )
    def update_map(selected_country, selected_subnational, map_type, selected_projection):
        filtered_df = MPImap
        if selected_country:
            filtered_df = filtered_df[filtered_df['Country'] == selected_country]
        if selected_subnational:
            filtered_df = filtered_df[filtered_df['Sub-national region'] == selected_subnational]

        if map_type == 'urban':
            size_col = 'Intensity of Deprivation Urban'
            color_col = 'Intensity of Deprivation Urban'
            title_text = 'Intensity of Deprivation Urban by Country and Region'
        elif map_type == 'rural':
            size_col = 'Intensity of Deprivation Rural'
            color_col = 'Intensity of Deprivation Rural'
            title_text = 'Intensity of Deprivation Rural by Country and Region'

        fig = px.scatter_geo(
            filtered_df,
            lat='Latitude',
            lon='Longitude',
            hover_name='Hover Name',
            hover_data={
                'Country': True,
                'Sub-national region': True
            },
            size=size_col,
            color=color_col,
            color_continuous_scale='Viridis',
            projection=selected_projection,
            title=title_text
        )

        fig.update_layout(
            title={
                'text': title_text,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            geo=dict(
                showframe=True,
                showcoastlines=True,
                coastlinecolor='black',
                projection_type=selected_projection,
                bgcolor='#f5ebe0'
            ),
            coloraxis_colorbar=dict(
                title='Intensity',
                tickprefix='',
                titlefont=dict(size=14),
                tickfont=dict(size=12)
            ),
            paper_bgcolor='#f5ebe0',
            plot_bgcolor='#f5ebe0',
            height=800,
            width=1600
        )
        return fig
