import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

def load_graph():
    csv = 'https://raw.githubusercontent.com/archiewood/lightlogger/master/lightlog.csv'
    avg_window=5

    df = pd.read_csv(csv)
    df['date']=df['timestamp'].str[:10]
    df['time']=df['timestamp'].str[10:19]
    df['median']= df['light_reading'].rolling(avg_window).median()
    df['std'] = df['light_reading'].rolling(avg_window).std()
    df = df[(df.light_reading <= df['median']+3*df['std']) & (df.light_reading >= df['median']-3*df['std'])]
    df['light_reading_moving_avg'] = df.iloc[:,1].rolling(window=avg_window).mean()

    fig =px.line(df,x='timestamp',y='light_reading_moving_avg',title='Balcony Light Intensity',range_y=[0,100])
    
    return html.Div([dcc.Graph(figure=fig)])


app = dash.Dash(__name__)
server = app.server

app.layout = load_graph


if __name__ == '__main__':
    app.run_server(debug=False)
