import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

csv = 'https://raw.githubusercontent.com/archiewood/lightlogger/master/lightlog.csv'
df = pd.read_csv(csv)
df['date']=df['timestamp'].str[:10]
df['time']=df['timestamp'].str[10:19]
df.head()

app = dash.Dash(__name__)
server = app.server

dates=df['date'].unique()

app.layout = html.Div([
    html.Div([dcc.Dropdown(id='date-select', options=[{'label': i, 'value': i} for i in dates],
                           value='2020-04-11', style={'width': '140px'})]),
    dcc.Graph('light-graph', config={'displayModeBar': False})])

@app.callback(
    Output('light-graph', 'figure'),
    [Input('date-select','value')]
)
def update_graph(selected_date):
    import plotly.express as px
    return px.line(df[df.date==selected_date],x='time',y='light_reading',color='date')

if __name__ == '__main__':
    app.run_server(debug=False)
