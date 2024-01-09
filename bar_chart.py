import pandas as pd
import plotly.express as px   
import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)    # Initialize the dash app 

# Read and clean Data Frame 
df = pd.read_csv("data/intro_bees.csv")

df.head(5)
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code' ])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)

print(df[:5])

# App Layout  
app.layout = html.Div([
     html.H1("Bee Colony Dashboard with Dash", style={'text-align': 'center'}),

     dcc.Dropdown(id="select_year",
                 options= [
                     {"label" : "2015", "value": 2015},
                     {"label" : "2016", "value": 2016},
                     {"label" : "2017", "value": 2017},
                     {"label" : "2018", "value": 2018}],
                    multi=False,
                    value=2015,
                    style={'width': "40%"}
                    ),

    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='my_bee_map', figure={})
]) 

# connect graphs Dash components by callbacks
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='my_bee_map', component_property= 'figure')], 
    [Input(component_id='select_year', component_property= 'value')]
)
def update_graph(option_selected):
    print(option_selected)
    print(type(option_selected))

    container = "The year chosen by user was : {}".format(option_selected)

    dff = df.copy()
    dff = dff[dff["Year"] == option_selected]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    # initializing plotly graph

    fig = px.bar(
        data_frame=dff,
        x='State',
        y='Pct of Colonies Impacted',
        hover_data= ['State', 'Pct of Colonies Impacted'],
        labels={'Pct of Colonies Impacted': '% of Bee Colonie'}, 
        template='plotly_dark'
    )

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)