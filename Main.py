# import dash_bootstrap_components as dbc
# import dash_html_components as html
# import dash
# import pandas as pd
# import dash_core_components as dcc
# from dash.dependencies import Input, Output
# import plotly.graph_objs as go
# import plotly.express as px
# from math import log10









import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input, Output


import plotly.graph_objs as go
import plotly.express as px

import numpy as np

import matplotlib.pyplot as plt

from math import log10

from plotly.tools import mpl_to_plotly

import seaborn as sns










    
df= pd.read_excel("C:/Users/Administrator/Desktop/new/P&L final.xlsx",sheet_name='data', skiprows=5,nrows=18, usecols="D:Q")
waterfall_data=df.copy()
waterfall_data.iloc[[1,3,5],1:]=waterfall_data.iloc[[1,3,5],1:]*(-1)
def finval(col):
    sm=0
    for i in waterfall_data[col][0:6]:
        sm+=i
    return sm
waterfall_data.loc[18]=[finval(x) for x in ["JAN","JAN", "FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","Total"]]
df[df["Indicator Name"]=="% of Income Budget"]
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
month_options = []
for month in months:
    month_options.append({'label':month, 'value': month})
db=df.drop([ "Total"], axis=True).T
db.reset_index(inplace=True)
clss=["cat"]
clss.extend(list(df["Indicator Name"]))
db.columns=clss
def pcc(month, catgg):
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    if month =="JAN":
        return 0.00
    else:
        for i in months:
            if month==i:
                m=round(100*(-df[df["Indicator Name"]==catgg][months[months.index(month)-1]]+df[df["Indicator Name"]==catgg][month])/(df[df["Indicator Name"]==catgg][months[months.index(month)-1]]), 1)
                return "{} %".format(m[list(m.index)[0]])
            else:
                pass
def tcv(mnt, catgg):
    return df[mnt][list(df["Indicator Name"]).index(catgg)]



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



dropdowns=   html.Div([dcc.Dropdown (id= 'month_picker', 
                    options=month_options, 
                    value="JAN",
                    placeholder="Select Month",
                    style = dict(
                            width = '175px',
                            
                            display = 'inline-block',
                            verticalAlign = "middle"
                            )                           
                            )])
wfgraph = dbc.Card([dbc.Card(
    [
        dbc.CardBody(html.Div([
html.Div(html.A(html.P("Statemennt"), style={'text-align': 'center', "font-weight": "bold"})),
            dcc.Graph (config = {'displayModeBar': False},id='wfg')]),
        ),
    ],
)],style={"width": "36rem"})




donut_card = dbc.Card([
        dbc.CardBody(
            [         
                html.Div([
html.Div(html.A(html.P("Net Profit Margin %"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.A(dcc.Graph(config={'displayModeBar':False},id="dnc"), style={'text-align': 'center', "font-weight": "bold", "margin-left":"0px"})
                ]),
            ]
        ),       
        ],style={"width": "18rem"})




incpie = dbc.Card([
        dbc.CardBody(
            [
            html.Div(html.A(html.P('% of Income Budget'), style={'text-align': 'center', "font-weight": "bold"})),   
            html.A(dcc.Graph(config={'displayModeBar':False},id="incpiechart"),  style={'textAlign': 'center', "font-weight": "bold"})
            ]
        ),
        ], style={"width": "18rem"})
expie = dbc.Card([
        dbc.CardBody(
            [
            html.Div(html.A(html.P('% of Expenses Budget'), style={'text-align': 'center', "font-weight": "bold"})),    
            html.A(dcc.Graph(config={'displayModeBar':False},id="expiechart"),  style={'textAlign': 'center', "font-weight": "bold"}),
            



            ]
        ),
        
        
        ],style={"width": "18rem"})


dashbar = dbc.Card([

        dbc.CardBody(
            [
            
                html.Div([
html.Div(html.A(html.P("Income and Expenses"), style={'text-align': 'center', "font-weight": "bold"})),
                    dcc.Graph(config={'displayModeBar':False},id="dash_bar_plot")
                ]),
            ]
        ),
        
        
        ],style={"width": "36rem"})





incomecard = dbc.Card([

        dbc.CardBody(
            [
            
                html.Div([
                    html.Div(html.A(html.P("Income"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P(id="intot"), style={'text-align': 'center', "font-weight": "bold"})),
                    dcc.Graph(config={'displayModeBar':False},id="inclc"),
                    html.Div(html.A(html.P(id="inper"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P("vs. Previous month"), style={'text-align': 'center'}))
                ])
            ])

        ],style={"width": "18rem"})
expensescard = dbc.Card([

        dbc.CardBody(
            [
            
                html.Div([
                    html.Div(html.A(html.P("Expenses"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P(id="extot"), style={'text-align': 'center', "font-weight": "bold"})),
                    dcc.Graph(config={'displayModeBar':False},id="explc"),
                    html.Div(html.A(html.P(id="exper"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P("vs. Previous month"), style={'text-align': 'center'}))
                ])
            ])
        
        
        ],style={"width": "18rem"})

accountsrecieveable = dbc.Card([

        dbc.CardBody(
            [
            
                html.Div([
                    html.Div(html.A(html.P("Accounts Receivable"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P(id="acrctot"), style={'text-align': 'center', "font-weight": "bold"})),
                    dcc.Graph(config={'displayModeBar':False},id="accrcv"),
                    html.Div(html.A(html.P(id="acrcper"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P("vs. Previous month"), style={'text-align': 'center'}))
                ])
            ])
        
        
        ],style={"width": "18rem"})

accountspayable = dbc.Card([

        dbc.CardBody(
            [
            
                html.Div([
                    html.Div(html.A(html.P("Accounts Payable"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P(id="acpytot"), style={'text-align': 'center', "font-weight": "bold"})),
                    dcc.Graph(config={'displayModeBar':False},id="accpay"),
                    html.Div(html.A(html.P(id="acpyper"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P("vs. Previous month"), style={'text-align': 'center'}))
                ])
            ])       
        
        ],style={"width": "18rem"})

netprofitcard = dbc.Card([

        dbc.CardBody(
            [
            
                html.Div([
                    html.Div(html.A(html.P("Net Profit"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P(id="netprofittot"), style={'text-align': 'center', "font-weight": "bold"})),
                    dcc.Graph(config={'displayModeBar':False},id="nplc"),
                    html.Div(html.A(html.P(id="netprofitper"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P("vs. Previous month"), style={'text-align': 'center'}))
                ])
            ])       
        
        ],style={"width": "18rem"})

cashatEOM = dbc.Card([

        dbc.CardBody(
            [
            
                html.Div([
                    html.Div(html.A(html.P("Cash at EOM"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P(id="caeomtot"), style={'text-align': 'center', "font-weight": "bold"})),
                    dcc.Graph(config={'displayModeBar':False},id="caeom"),
                    html.Div(html.A(html.P(id="caeomper"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P("vs. Previous month"), style={'text-align': 'center'}))
                ])
            ])        
        
        ],style={"width": "18rem"})

quickratio = dbc.Card([

        dbc.CardBody(
            [
            
                html.Div([
                    html.Div(html.A(html.P("Quick Ratio"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P(id="qrtot"), style={'text-align': 'center', "font-weight": "bold"})),
                    dcc.Graph(config={'displayModeBar':False},id="qrlc"),
                    html.Div(html.A(html.P(id="qrper"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P("vs. Previous month"), style={'text-align': 'center'}))
                ])
            ])        
        
        ],style={"width": "18rem"})


currentratio = dbc.Card([

        dbc.CardBody(
            [
            
                html.Div([
                    html.Div(html.A(html.P("Current Ratio"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P(id="crtot"), style={'text-align': 'center', "font-weight": "bold"})),
                    dcc.Graph(config={'displayModeBar':False},id="crlc"),
                    html.Div(html.A(html.P(id="crper"), style={'text-align': 'center', "font-weight": "bold"})),
                    html.Div(html.A(html.P("vs. Previous month"), style={'text-align': 'center'}))
                ])
            ])
        
        
        ],style={"width": "18rem"})



lineone=html.Div([ 

    dbc.Row(
        [wfgraph, donut_card, dashbar
        ]
    ),

    dbc.Row(
            [incomecard,expensescard, incpie, accountsrecieveable,accountspayable
            
                
            ]),

    dbc.Row(
            [netprofitcard, cashatEOM, expie,quickratio, currentratio
                
            ]),   
            ])



cards = html.Div([dbc.Row([
                    dbc.Col(dbc.Card(dropdowns, style={'height':'100%'}), width='auto'),
                    dbc.Col(dbc.Card(lineone, style={'height':'100%'}),width='100%' ),
            ]),])






app.layout= cards







@app.callback(Output ('wfg', 'figure'), [Input('month_picker', 'value')])
def waterfall_graph(mnth):

    fig = go.Figure(go.Waterfall(
        name = "WaterFallGraph", orientation = "v",
        measure = ["Total", "relative", "relative", "relative", "relative", "relative", "total"],
        x =waterfall_data.iloc[[0,1,2,3,4,5,18]]["Indicator Name"],
        textposition = "outside",
        text = waterfall_data.iloc[[0,1,2,3,4,5,18]][mnth],
        y = waterfall_data.iloc[[0,1,2,3,4,5,18]][mnth],
        increasing = {"marker":{"color":"lightseagreen"}},
        decreasing = {"marker":{"color":"#EE5C42"}},
        totals = {"marker":{"color":"#27408B"}},
        connector = {"visible": False},),
        layout = {'xaxis': {
            'visible': True,
            'showticklabels': True},
        'yaxis': {
            'visible': False,
            'showticklabels': False},
    
            'height': 300,
            'width' : 520,
            'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
    
        }
        
        
        
        )

    fig.update_layout(
            title = "Profit and loss statement",
            showlegend = False
    ).add_shape(
    type="rect", fillcolor="#27408B", line=dict(color="#27408B"), opacity=1,
    x0=-0.4, x1=0.4, xref="x", y0=0.0, y1=fig.data[0].y[0], yref="y")


    fig.update_layout(
    xaxis = dict(
        tickangle=0,
        tickmode = 'array',
        tickvals = [0, 3, 6],
        ticktext = ['Total Income', 'Total Operating Expenses', 'Net Profit']
    )
)

    return fig





@app.callback(Output ('dnc', 'figure'), [Input('month_picker', 'value')])
def donut_chart(mnth):

    val = round(df.iloc[7][mnth]*100,1)
    labels = [str(round(val-14.0,1)), str(val)]
    data = [14.0,val]
    n = len(data)
    k = 10 ** int(log10(max(data)))
    m = k * (1 + max(data) // k)
    outer_values = [data[0], m-data[0]]
    inner_values = [data[1], m - data[1]]







    trace1 = go.Pie(
        hole=0.6,
        sort=False,
        values=inner_values,
        textinfo='text',
        direction='clockwise',
        marker={'colors': ['lightseagreen', "white"],
                    'line': {'color': 'white', 'width': 1}}
    )

    trace2 = go.Pie(
        hole=0.8,
        sort=False,
        textinfo='text',
        direction='clockwise',
        values=outer_values,
        marker={'colors': ["#EE5C42", "white"],
                    'line': {'color': 'white', 'width': 1}}
    )




    layout = go.Layout(
    xaxis=dict(
        autorange=True,
        showgrid=False,
        ticks='',
        showticklabels=False
    ),
    yaxis=dict(
        autorange=True,
        showgrid=False,
        ticks='',
        showticklabels=False
    ),
        height=150,
        width=250,
        margin=dict(l= 0, b= 0, t= 0, r= 0)
)





    fig = go.FigureWidget(data=[trace1, trace2], layout=layout)
    fig.update_layout(showlegend=False)




    fig.update_layout(showlegend=False,
        annotations=[dict(text=labels[1]+"%", x=0.515, y=0.56, font_size=20, showarrow=False),
                    dict(text=labels[0]+"%", x=0.515, y=0.44, font_size=20, showarrow=False)])


    return fig







@app.callback(Output ('incpiechart', 'figure'), [Input('month_picker', 'value')])
def inc_donut_chart(mnth):

    labels = [str(round(df.iloc[15][mnth]*100)), str(100-round(df.iloc[15][mnth]*100))]
    data = [(round(df.iloc[15][mnth]*100)), (100-round(df.iloc[15][mnth]*100))]
    n = len(data)
    k = 10 ** int(log10(max(data)))
    m = k * (1 + max(data) // k)
    outer_values = [data[0], m-data[0]]
    inner_values = [m-data[0], data[0]]







    trace1 = go.Pie(
        hole=0.6,
        sort=True,
        values=inner_values,
        textinfo='text',
        direction='counterclockwise',
        marker={'colors': ['black', "white"],
                    'line': {'color': 'white', 'width': 1}}
    )

    trace2 = go.Pie(
        hole=0.8,
        sort=False,
        textinfo='text',
        direction='clockwise',
        values=outer_values,
        marker={'colors': ["lightseagreen", "white"],
                    'line': {'color': 'white', 'width': 1}}
    )




    layout = go.Layout(
    xaxis=dict(
        autorange=True,
        showgrid=False,
        ticks='',
        showticklabels=False
    ),
    yaxis=dict(
        autorange=True,
        showgrid=False,
        ticks='',
        showticklabels=False
    ),
        height=100,
        width=180,
        margin=dict(l= 0, b= 0, t= 0, r= 0)
)





    fig = go.FigureWidget(data=[trace1, trace2], layout=layout)
    fig.update_layout(showlegend=False)




    fig.update_layout(showlegend=False,
        annotations=[dict(text=labels[0]+"%", x=0.515, y=0.54, font_size=20, showarrow=False)])


    return fig





@app.callback(Output ('expiechart', 'figure'), [Input('month_picker', 'value')])
def exp_donut_chart(mnth):


    labels = [str(round(df.iloc[17][mnth]*100)), str(100-round(df.iloc[17][mnth]*100))]
    data = [(round(df.iloc[17][mnth]*100)), (100-round(df.iloc[17][mnth]*100))]

    n = len(data)
    k = 10 ** int(log10(max(data)))
    m = k * (1 + max(data) // k)
    outer_values = [data[0], m-data[0]]
    inner_values = [m-data[0], data[0]]







    trace1 = go.Pie(
        hole=0.6,
        sort=True,
        values=inner_values,
        textinfo='text',
        direction='counterclockwise',
        marker={'colors': ['black', "white"],
                    'line': {'color': 'white', 'width': 1}}
    )

    trace2 = go.Pie(
        hole=0.8,
        sort=False,
        textinfo='text',
        direction='clockwise',
        values=outer_values,
        marker={'colors': ["lightseagreen", "white"],
                    'line': {'color': 'white', 'width': 1}}
    )




    layout = go.Layout(
    xaxis=dict(
        autorange=True,
        showgrid=False,
        ticks='',
        showticklabels=False
    ),
    yaxis=dict(
        autorange=True,
        showgrid=False,
        ticks='',
        showticklabels=False
    ),
        height=100,
        width=180,
        margin=dict(l= 0, b= 0, t= 0, r= 0)
)





    fig = go.FigureWidget(data=[trace1, trace2], layout=layout)
    fig.update_layout(showlegend=False)




    fig.update_layout(showlegend=False,
        annotations=[
                    dict(text=labels[0]+"%", x=0.515, y=0.54, font_size=20, showarrow=False)])


    return fig





















@app.callback(
    Output(component_id='inclc', component_property='figure'),
    [Input(component_id='month_picker', component_property='value')]
)
def income_line(input_value):
    return px.line(y=list(df.loc[0][1:-1]), x=list(df.columns[1:-1])).update_layout(
    showlegend=False,
    plot_bgcolor="white",
    height=50,
    width=180,
    xaxis=dict(visible=False,
    showticklabels= False),
    yaxis=dict(visible=False,
    showticklabels= False),
    margin=dict(t=0,l=0,b=0,r=0)
)

@app.callback(
    Output(component_id='explc', component_property='figure'),
    [Input(component_id='month_picker', component_property='value')]
)
def expenses_line_graph(input_value):
    return px.line(y=list(df.loc[8][1:-1]), x=list(df.columns[1:-1])).update_layout(
    showlegend=False,
    plot_bgcolor="white",
    height=50,
    width=180,
    xaxis=dict(visible=False,
    showticklabels= False),
    yaxis=dict(visible=False,
    showticklabels= False),
    margin=dict(t=0,l=0,b=0,r=0)
)

@app.callback(
    Output(component_id='accrcv', component_property='figure'),
    [Input(component_id='month_picker', component_property='value')]
)
def acc_rec_graph(input_value):
    return px.line(y=list(df.loc[12][1:-1]), x=list(df.columns[1:-1])).update_layout(
    showlegend=False,
    plot_bgcolor="white",
    height=50,
    width=180,
    xaxis=dict(visible=False,
    showticklabels= False),
    yaxis=dict(visible=False,
    showticklabels= False),
    margin=dict(t=0,l=0,b=0,r=0)
)



@app.callback(
    Output(component_id='accpay', component_property='figure'),
    [Input(component_id='month_picker', component_property='value')]
)
def acc_pay_graph(input_value):
    return px.line(y=list(df.loc[13][1:-1]), x=list(df.columns[1:-1])).update_layout(
    showlegend=False,
    plot_bgcolor="white",
    height=50,
    width=180,
    xaxis=dict(visible=False,
    showticklabels= False),
    yaxis=dict(visible=False,
    showticklabels= False),
    margin=dict(t=0,l=0,b=0,r=0)
)




@app.callback(
    Output(component_id='nplc', component_property='figure'),
    [Input(component_id='month_picker', component_property='value')]
)
def net_profit_graph(input_value):
    return px.line(y=list(df.loc[6][1:-1]), x=list(df.columns[1:-1]), ).update_layout(
    showlegend=False,
    plot_bgcolor="white",
    height=50,
    width=180,
    xaxis=dict(visible=False,
    showticklabels= False),
    yaxis=dict(visible=False,
    showticklabels= False),
    margin=dict(t=0,l=0,b=0,r=0)
)



@app.callback(
    Output(component_id='caeom', component_property='figure'),
    [Input(component_id='month_picker', component_property='value')]
)
def cash_eom_graph(input_value):
    return px.line(y=list(df.loc[9][1:-1]), x=list(df.columns[1:-1])).update_layout(
    showlegend=False,
    plot_bgcolor="white",
    height=50,
    width=180,
    xaxis=dict(visible=False,
    showticklabels= False),
    yaxis=dict(visible=False,
    showticklabels= False),
    margin=dict(t=0,l=0,b=0,r=0)
)



@app.callback(
    Output(component_id='qrlc', component_property='figure'),
    [Input(component_id='month_picker', component_property='value')]
)
def qr_graph(input_value):
    return px.line(y=list(df.loc[10][1:-1]), x=list(df.columns[1:-1])).update_layout(
    showlegend=False,
    plot_bgcolor="white",
    height=50,
    width=180,
    xaxis=dict(visible=False,
    showticklabels= False),
    yaxis=dict(visible=False,
    showticklabels= False),
    margin=dict(t=0,l=0,b=0,r=0)
)



@app.callback(
    Output(component_id='crlc', component_property='figure'),
    [Input(component_id='month_picker', component_property='value')]
)
def cr_line(input_value):
    return px.line(y=list(df.loc[11][1:-1]), x=list(df.columns[1:-1])).update_layout(
    showlegend=False,
    plot_bgcolor="white",
    height=50,
    width=180,
    xaxis=dict(visible=False,
    showticklabels= False),
    yaxis=dict(visible=False,
    showticklabels= False),
    margin=dict(t=0,l=0,b=0,r=0)
)






@app.callback(
    Output(component_id='dash_bar_plot', component_property='figure'),
    [Input(component_id='month_picker', component_property='value')]
)
def dash_barmat_graph(input_value):

    fig=go.Figure(data=[  
        go.Bar(x=db[1:]["cat"], y=db[1:]["Income"]-db[1:]["Operating Profit (EBIT)"], marker_color='#C1CDCD'),
        go.Bar(x=db[1:]["cat"], y=db[1:]["Operating Profit (EBIT)"], marker_color='#C1CDCD'),
    ],
            layout = {'xaxis': {
                'visible': False,
                'showticklabels': False},
            'yaxis': {
                'visible': False,
                'showticklabels': False},
        
                'height': 300,
                'width' : 550,
                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
        
            }               
                
    )
    fig.update_layout(barmode='stack')
    [fig.add_annotation(
        xref="x",
        yref="y",
        x=i-1,
        y=db[1:]["Income"][i]-db[1:]["Operating Profit (EBIT)"][i]-200,
        text=str(db[1:]["Income"][i]),
        axref="x",
        ayref="y",
        ax=i-1,
        ay=0,
        arrowhead=2,
        arrowwidth=3,
        arrowcolor="green"
    ) for i in range(1,13)] 

    [fig.add_annotation(
        xref="x",
        yref="y",
        x=i-1,
        y=db[1:]["Income"][i]-db[1:]["Operating Profit (EBIT)"][i]+200,
        text=str(db[1:]["Operating Profit (EBIT)"][i]),
        axref="x",
        ayref="y",
        ax=i-1,
        ay=db[1:]["Income"][i],
        arrowhead=2,
        arrowwidth=3,
        arrowcolor="red"
    ) for i in range(1,13)] 



    [fig.add_annotation(
        xref="x",
        yref="y",
        x=i-1,
        y=db[1:]["Income"][i]-db[1:]["Operating Profit (EBIT)"][i],
        text=str(db[1:]["Income"][i]-db[1:]["Operating Profit (EBIT)"][i]),
        showarrow=False,

    ) for i in range(1,13)] 

    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output(component_id='inper', component_property='children'),
    Output(component_id='exper', component_property='children'),
    Output(component_id='acrcper', component_property='children'),
    Output(component_id='acpyper', component_property='children'),
    Output(component_id='netprofitper', component_property='children'),
    Output(component_id='caeomper', component_property='children'),
    Output(component_id='qrper', component_property='children'),
    Output(component_id='crper', component_property='children'),
    [Input(component_id='month_picker', component_property='value')]
)
def percenchange(mnh):
    return pcc(mnh, "Income"),pcc(mnh, "Expenses"),pcc(mnh, "Accounts Receivable"),pcc(mnh, "Accounts Payable"),pcc(mnh, "Net Profit   "),pcc(mnh, "Cash at EOM"),pcc(mnh, "Quick Ratio"),pcc(mnh, "Current Ratio")

@app.callback(
    Output(component_id='intot', component_property='children'),
    Output(component_id='extot', component_property='children'),
    Output(component_id='acrctot', component_property='children'),
    Output(component_id='acpytot', component_property='children'),
    Output(component_id='netprofittot', component_property='children'),
    Output(component_id='caeomtot', component_property='children'),
    Output(component_id='qrtot', component_property='children'),
    Output(component_id='crtot', component_property='children'),
    [Input(component_id='month_picker', component_property='value')]
)
def percenchange(mnh):
    return tcv(mnh, "Income"),tcv(mnh, "Expenses"),tcv(mnh, "Accounts Receivable"),tcv(mnh, "Accounts Payable"),tcv(mnh, "Net Profit   "),tcv(mnh, "Cash at EOM"),tcv(mnh, "Quick Ratio"),tcv(mnh, "Current Ratio")



if __name__ == "__main__":
    app.run_server(debug=True, port=8183)
