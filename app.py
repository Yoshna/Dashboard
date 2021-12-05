import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from datetime import date
from datetime import datetime

app = Dash(__name__)
server = app.server
# -- Import and clean data (importing csv into pandas)

df = pd.read_csv("dataset.csv")
# App layout
# this is the layout of the webpage i.e our dashboard
app.layout = html.Div([
# Heading
    html.H1("India's state-wise data", style={'text-align': 'center'}),
# Date Picker and graph
    html.Div(
        children=[
            html.Div(
        children=[
           dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "Income", "value": "2011-12-INC"},
                     {"label": "Literacy rate", "value": "2011- LIT"},
                     {"label": "Total population", "value": "2011- POP"},
                     {"label": "Sex-Ratio", "value": "2011 -SEX_Ratio"},
                     {"label": "Unemployment rate", "value": "2001 -UNEMP"}],
                 multi=False,
                 value="2011-12-INC",
                 style={'width': "40%"}
                 ),

            html.Div(id='output-container-date-picker-single', children=[]),
            html.Br(),

            dcc.Graph(id='my_bee_map', figure={}),
        ],style={ 'flex': 1}
    )
        ]
        ,style={'display': 'flex', 'flex-direction': 'row'}
    )
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
# This is basically the calllback to connect the Dash Component and Dash Graph with each other
@app.callback(
    [Output('output-container-date-picker-single', 'children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input('slct_year', 'value')]
)
# the funnction that will trigeer on the value change in date picker
def update_graph(value):
    print(value)
    container = 'Showing Results of : {}'.format(value)
    dff = df.copy()
    # getting alll the datat at that selected date
    print(dff)
    # here we are making the map of india using GeoJson because its not available on PLotly only US map is avaialble
    fig = go.Figure(data=go.Choropleth(
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locationmode='geojson-id',
    locations=dff['States_Union Territories'],
    z=dff[value],
    # text=dff['text'],

    autocolorscale=False,
    colorscale="Reds",
    marker_line_color='peachpuff',
    ))
    fig.update_geos(
      visible=False,
      projection=dict(
        type='conic conformal',
        parallels=[12.472944444, 35.172805555556],
        rotation={'lat': 24, 'lon': 80}
      ),
      lonaxis={'range': [68, 98]},
      lataxis={'range': [6, 38]}
    )
    fig.update_layout(
         title=dict(
        text="India's state-wise " + value,
        xanchor='center',
        x=0.5,
        yref='paper',
        yanchor='bottom',
        y=1,
        pad={'b': 10}
    ),
      margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
    )
    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
