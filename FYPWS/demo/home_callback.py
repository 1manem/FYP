# home_callback.py
import html
from dash import callback_context
from dash.dependencies import Input, Output

import plotly.express as px
import dash
import pandas as pd

data = pd.read_csv("C:/Users/William/Documents/FYPWS/demo/complete_data.csv")
df = pd.DataFrame(data)

def register_callbacks(app):
    @app.callback(
        Output('bar-plot', 'figure'),
        [Input('metric-dropdown', 'value')]
    )
    def update_graph(selected_metric):
        # Filter out countries where any of the columns have a value of 0
        non_zero_countries = df[(df['Median Salary'] > 0) & 
                                (df['Inequality in Income'] > 0) & 
                                (df['GDP per capita'] > 0) & 
                                (df['Intensity of Deprivation Urban'] > 0) & 
                                (df['Intensity of Deprivation Rural'] > 0)]
        
        # Sort by the selected metric and select bottom 10
        bottom_10_countries = non_zero_countries.sort_values(by=selected_metric, ascending=True).head(10)
        
        # Create the plot
        fig = px.bar(
            bottom_10_countries,
            x=selected_metric,
            y='Country',
            orientation='h',
            title=f'Bottom 10 Countries by {selected_metric}',
            labels={selected_metric: selected_metric, 'Country': 'Country'},
            color=selected_metric
        )
        fig.update_layout(yaxis=dict(autorange='reversed'))

        return fig

