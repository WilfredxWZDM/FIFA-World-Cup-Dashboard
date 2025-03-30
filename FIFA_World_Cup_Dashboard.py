import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

world_cup_data = pd.DataFrame({
    'Year': [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],
    'Winner': ['Uruguay', 'Italy', 'Italy', 'Uruguay', 'Germany', 'Brazil', 'Brazil', 'England', 'Brazil', 'Germany', 'Argentina', 'Italy', 'Argentina', 'Germany', 'Brazil', 'France', 'Brazil', 'Italy', 'Spain', 'Germany', 'France', 'Argentina'],
    'Runner_up': ['Argentina', 'Czechoslovakia', 'Hungary', 'Brazil', 'Hungary', 'Sweden', 'Czechoslovakia', 'Germany', 'Italy', 'Netherlands', 'Netherlands', 'Germany', 'Germany', 'Argentina', 'Italy', 'Brazil', 'Germany', 'France', 'Netherlands', 'Argentina', 'Croatia', 'France']
})

app = dash.Dash(__name__)
server = app.server

wins_by_country = world_cup_data['Winner'].value_counts().reset_index()
wins_by_country.columns = ['Country', 'Wins']

app.layout = html.Div([
    html.H1('FIFA World Cup Dashboard', style={'textAlign': 'center'}),
    
    html.Div([
        html.H3('Select World Cup Year:'),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in world_cup_data['Year']],
            value=2022
        ),
        html.Div(id='year-output')
    ]),
    
    html.Div([
        html.H3('Select Country:'),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in wins_by_country['Country']],
            value='Brazil'
        ),
        html.Div(id='country-output')
    ]),
    
    dcc.Graph(id='world-cup-map')
])

@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_output(selected_year):
    filtered_data = world_cup_data[world_cup_data['Year'] == selected_year]
    if filtered_data.empty:
        return 'Please select a year'
    winner = filtered_data['Winner'].iloc[0]
    runner_up = filtered_data['Runner_up'].iloc[0]
    return f'In {selected_year}, {winner} won the World Cup, and {runner_up} was the runner-up.'

@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_output(selected_country):
    if selected_country is None:
        return 'Please select a country'
    wins = len(world_cup_data[world_cup_data['Winner'] == selected_country])
    return f'{selected_country} has won the World Cup {wins} time(s).'

@app.callback(
    Output('world-cup-map', 'figure'),
    Input('year-dropdown', 'value')
)
def update_map(selected_year):
    all_winners = pd.DataFrame(wins_by_country)
    
    fig = px.choropleth(
        all_winners,
        locations='Country',
        locationmode='country names',
        color='Wins',
        hover_name='Country',
        color_continuous_scale='Viridis',
        title='World Cup Wins by Country'
    )
    
    fig.update_layout(
        title_x=0.5,
        title_font_color='black',
        geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
        width=1000,
        height=600
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug = True, port =  8055)
