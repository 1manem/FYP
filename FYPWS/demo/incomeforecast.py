from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sidebar import sidebar

# Load the income dataset
income_dataset = pd.read_csv("incomeMap.csv")

# Extract unique country names for the dropdown
country_options = [{'label': country, 'value': country} for country in income_dataset['Country'].unique()]

# Function to create the forecasting layout
def incForecasting_layout():
    return html.Div([
        sidebar(),
        html.Div([
            html.H2("Inequality in Income Forecast"),
            html.Div([
                html.Label("Select Country:"),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=country_options,
                    placeholder='Select a country',
                    style={'margin-right': '10px', 'width': '300px'}
                ),
                html.Button(id='submit-button', n_clicks=0, children='Submit'),
            ], style={'margin-bottom': '20px', 'display': 'flex'}),
            html.Div(id='inc-forecast-output', style={'display': 'flex'})
        ], style={'margin-left': '-170px', 'padding': '20px', 'backgroundColor': '#f5ebe0'})
    ], style={'display': 'flex', 'backgroundColor': '#f5ebe0'})

# Function to register the callbacks for the forecasting page
def inc_register_forecasting_callbacks(app):
    @app.callback(
        Output('inc-forecast-output', 'children'),
        Input('submit-button', 'n_clicks'),
        State('country-dropdown', 'value')
    )
    def update_inc_forecast(n_clicks, country):
        if not n_clicks or not country:
            return ''
        df_country = income_dataset[income_dataset['Country'] == country]
        if df_country.empty:
            return f"No data available for {country}."
        
        df_country = df_country[['Year', 'Value']]
        df_country.set_index('Year', inplace=True)
        df_country = df_country[df_country['Value'] != 0]
        
        if df_country.empty:
            return f"No valid data available for {country} after filtering out zero values."
        
        try:
            # Prepare data for Polynomial Regression
            X = df_country.index.values.reshape(-1, 1)
            y = df_country['Value'].values
            
            # Create polynomial features
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)
            
            # Create and fit the model
            model2BestLR = LinearRegression()
            model2BestLR.fit(X_poly, y)
            
            # Forecast the next 10 years
            future_years = np.arange(df_country.index[-1] + 1, df_country.index[-1] + 11).reshape(-1, 1)
            future_years_poly = poly.transform(future_years)
            forecast = model2BestLR.predict(future_years_poly)
            
            # Create a DataFrame for future dates
            future_df = pd.DataFrame({
                'Year': future_years.flatten(),
                'Value': forecast
            }).set_index('Year')
            
            # Plotting
            fig, ax = plt.subplots(figsize=(14, 8))
            df_country.plot(ax=ax, label='Historical Data', color='blue')
            future_df.plot(ax=ax, label='Forecast', linestyle='--', color='orange')
            ax.set_title(f'Income Forecast for {country}', fontsize=16)
            ax.set_xlabel('Year', fontsize=14)
            ax.set_ylabel('Income Value', fontsize=14)
            ax.legend()
            ax.grid(True)
            plt.xticks(np.arange(df_country.index.min(), future_df.index.max() + 1, 5), rotation=45)
            plt.tight_layout()
            
            # Save plot to PNG and encode to base64
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()
            
            # Return the plot and forecasted data
            return html.Div([
                html.Div([
                    html.Img(src='data:image/png;base64,{}'.format(image_base64)),
                ], style={'flex': '2'}),
                html.Div([
                    html.H4('Forecasted Income Values:', style={'margin-bottom': '10px', 'font-size': '18px'}),
                    dcc.Markdown(future_df.to_markdown(index=True))
                ], style={'flex': '1', 'padding-left': '20px'})
            ], style={'display': 'flex', 'backgroundColor': '#f5ebe0'})
        except Exception as e:
            return f"An error occurred while fitting the model or forecasting: {e}"
