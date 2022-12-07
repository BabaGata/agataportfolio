#!/usr/bin/env python
# coding: utf-8

from dash import Dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX],
                 meta_tags=[
                     {'name':'viewport', 'content':'width=device_width, initial-scale=1.0'}
                 ])
server=app.server

app.title = 'AV Portfolio'
top_df = pd.read_csv('top_top.csv')
gen_df = pd.read_csv('gen_max.csv')
fam_df = pd.read_csv('fam_max.csv')

colors_dict = {
    'INFJ' : '#52BE80', 'INFP' : '#1E8449', 'ENFJ' : '#58D68D', 'ENFP' : '#239B56',
    'INTJ' : '#AF7AC5', 'INTP' : '#76448A', 'ENTJ' : '#CD6155', 'ENTP' : '#922B21',
    'ISTJ' : '#5499C7', 'ISFJ' : '#1F618D', 'ESTJ' : '#5DADE2', 'ESFJ' : '#2874A6',
    'ISTP' : '#F4D03F', 'ISFP' : '#B7950B', 'ESTP' : '#EB984E', 'ESFP' : '#AF601A',
}

fig_3D = px.scatter_3d(
    top_df, x="GDP_per_capita_$", y="Life_expectancy", z = 'Unemployment_rate',
    size="Population", color="Genus",
    height=800,
    hover_name="Country", log_x=True, log_z=True, size_max=60
)
fig_3D.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(yanchor="top", y=0, xanchor="left", x=0.01, orientation='h'),
    title=dict(yanchor="top", y=1, xanchor="left", x=0),
    paper_bgcolor='rgba(0,0,0,0)',
    legend_font_color='rgba(235,237,239,1)',
    scene=dict(
        xaxis=dict(color='rgba(235,237,239,1)'),
        yaxis=dict(color='rgba(235,237,239,1)'),
        zaxis=dict(color='rgba(235,237,239,1)')
              )
)

gen_options = []
for x in list(gen_df.columns)[0:36]:
    gen_options.append({'label':x, 'value':x})
fam_options = []
for x in list(fam_df.columns)[0:18]:
    fam_options.append({'label':x, 'value':x})
    
@app.callback(
    Output(component_id='gen_go_bubble', component_property='figure'),
    Input(component_id='gen_go_dropdown', component_property='value')
)

def update_gen(value):
    fig = make_subplots()
    for abc in value:
        trace = go.Scatter(
            x=gen_df.index,
            y=gen_df[abc],
            marker_size=gen_df['{}_T'.format(abc)],
            name=abc,
        )
        fig.add_trace(trace)
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(yanchor="top", y=-0.1, xanchor="left", x=0.01, orientation='h'),
        title=dict(yanchor="top", y=1, xanchor="left", x=0),
        paper_bgcolor='rgba(0,0,0,0)',
        legend_font_color='rgba(235,237,239,1)',
        xaxis_color='rgba(235,237,239,1)',
        yaxis_color='rgba(235,237,239,1)',
    )
    return fig

@app.callback(
    Output(component_id='fam_go_bubble', component_property='figure'),
    Input(component_id='fam_go_dropdown', component_property='value')
)
def update_gen(value):
    # Plotly express
    fig = make_subplots()
    for abc in value:
        trace = go.Scatter(
            x=fam_df.index,
            y=fam_df[abc],
            marker_size=fam_df['{}_T'.format(abc)],
            name=abc,
        )
        fig.add_trace(trace)
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(yanchor="top", y=-0.1, xanchor="left", x=0.01, orientation='h'),
        title=dict(yanchor="top", y=1, xanchor="left", x=0),        
        paper_bgcolor='rgba(0,0,0,0)',
        legend_font_color='rgba(235,237,239,1)',
        xaxis_color='rgba(235,237,239,1)',
        yaxis_color='rgba(235,237,239,1)',
    )
    return fig

max_figs = []
for i in range(2):
    fig = px.choropleth(
        locations = top_df['CODE'],
        color = top_df['MAX_{}'.format(i)],
        color_discrete_map = colors_dict,
        hover_name = top_df['Country'],
        hover_data = [top_df['Languages'], top_df['Genus'], top_df['Family']],
        labels={'locations':'Alpha-3 code', 'color':'Type', 
                'hover_data_0':'Language', 'hover_data_1':'Genus', 'hover_data_2':'Family'}
    )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(yanchor="top", y=0.6, xanchor="left", x=0.01),
        title=dict(yanchor="top", y=0.9, xanchor="left", x=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
    )
    max_figs.append(fig)

    
@app.callback(
    Output(component_id='slider-map-container', component_property='figure'),
    Input(component_id='my-slider', component_property='value'))
def update_output(value):    
    if value<8:
        fig = px.choropleth(
            locations = top_df['CODE'],
            color = top_df['MAX_{}'.format(value)],
            color_discrete_map = colors_dict,
            hover_name = top_df['Country'],
            hover_data = [top_df['Languages'], top_df['Genus'], top_df['Family']],
            labels={'locations':'Alpha-3 code', 'color':'Type', 
                    'hover_data_0':'Language', 'hover_data_1':'Genus', 'hover_data_2':'Family'}
        )
    else:
        fig = px.choropleth(
            locations = top_df['CODE'],            
            color = top_df['MIN_{}'.format(15-value)],
            color_discrete_map = colors_dict,
            hover_name = top_df['Country'],
            hover_data = [top_df['Languages'], top_df['Genus'], top_df['Family']],
            labels={'locations':'Alpha-3 code', 'color':'Type', 
                    'hover_data_0':'Language', 'hover_data_1':'Genus', 'hover_data_2':'Family'}
        )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(yanchor="top", y=-0.05, xanchor="left", x=0.01, orientation='h'),
        title=dict(yanchor="top", y=1, xanchor="left", x=0),
        paper_bgcolor='rgba(0,0,0,0)',
        legend_font_color='rgba(235,237,239,1)',
    )
    return fig

@app.callback(
     Output(component_id='my_bubble_chart', component_property='figure'),
    [Input(component_id='slct_chart_1', component_property='value'),
     Input(component_id='slct_chart_2', component_property='value'),
     Input(component_id='slct_chart_3', component_property='value')]
)
def update_graph(option_slctd_1, option_slctd_2, option_slctd_3):
    color_map={16:'Genus', 17:'Family', 18:'Region'}
    
    if option_slctd_3 < 8:
        fig = px.scatter(
            data_frame = top_df,
            x=option_slctd_1, 
            y=option_slctd_2,
            size="Population",
            color='MAX_{}'.format(option_slctd_3),
            color_discrete_map = colors_dict,
            hover_name="Country",
            log_x=True,
            size_max=60
        )
    elif option_slctd_3 > 15:
        fig = px.scatter(
            data_frame = top_df,
            x=option_slctd_1, 
            y=option_slctd_2,
            size="Population",
            color=color_map[option_slctd_3],
            hover_name="Country",
            log_x=True,
            size_max=60
        )
    else:
        fig = px.scatter(
            data_frame = top_df,
            x=option_slctd_1, 
            y=option_slctd_2,
            size="Population",
            color='MIN_{}'.format(15-option_slctd_3),
            color_discrete_map = colors_dict,
            hover_name="Country",
            log_x=True,
            size_max=60
        )
        
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(yanchor="top", y=-0.2, xanchor="left", x=0.01, orientation='h'),
        title=dict(yanchor="top", y=1, xanchor="left", x=0),
        paper_bgcolor='rgba(0,0,0,0)',
        legend_font_color='rgba(235,237,239,1)',
        xaxis_color='rgba(235,237,239,1)',
        yaxis_color='rgba(235,237,239,1)',
    )
    return fig

navbar = dbc.Navbar([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Nav([
                    dbc.NavItem(html.A('Home', href='#'), className='nav-zuta'),
                ])
            ], xs=6, sm=6, md=6, lg=1, xl=1),
            dbc.Col([
                dbc.Nav([
                    dbc.NavItem(html.A('Introduction', href='#introduction'), className='nav-zelena1'),
                    dbc.NavItem(
                        dbc.DropdownMenu([
                            dbc.DropdownMenuItem(html.A('Process', href='#process')),
                            dbc.DropdownMenuItem(html.A('Data searching', href='#data_searching')),
                            dbc.DropdownMenuItem(html.A('Data cleaning', href='#data_cleaning')),
                            dbc.DropdownMenuItem(html.A('Analysis & Visualization', href='#analysis')),
                            dbc.DropdownMenuItem(html.A('Presentation of the results', href='#presentation')),
                        ], 
                            className='nav-plava1',
                            nav=True,
                            in_navbar=True,
                            label='Process',
                            toggle_style={'color':'#000000'},
                        )
                    ),
                    dbc.NavItem(html.A('Conclusion', href='#conclusion'), className='nav-crvena1'),
                    dbc.NavItem(html.A('Contact', href='#footer'), className='nav-ljubicasta1'),
                    dbc.NavItem(html.A('More about me', href='#footer'), className='nav-tirkizna1'),
                    dbc.NavItem(
                        dbc.DropdownMenu([
                            dbc.DropdownMenuItem(html.A('Introduction', href='#introduction'), className='nav-zelena'),
                            dbc.DropdownMenuItem(html.A('Process', href='#process'), className='nav-plava'),
                            dbc.DropdownMenuItem(html.A('Data searching', href='#data_searching'), className='nav-plava'),
                            dbc.DropdownMenuItem(html.A('Data cleaning', href='#data_cleaning'), className='nav-plava'),
                            dbc.DropdownMenuItem(html.A('Analysis', href='#analysis'), className='nav-plava'),
                            dbc.DropdownMenuItem(html.A('Presentation', href='#presentation'), className='nav-plava'),
                            dbc.DropdownMenuItem(html.A('Conclusion', href='#conclusion'), className='nav-crvena'),
                            dbc.DropdownMenuItem(html.A('Contact', href='#footer'), className='nav-ljubicasta'),
                            dbc.DropdownMenuItem(html.A('More about me', href='#footer'), className='nav-tirkizna'),
                        ], 
                            className='hamburger',
                            nav=True,
                            label=None,
                            in_navbar=True,
                            toggle_style={'color':'#000000'},
                        ),
                        className='right-nav',
                    )
                ],
                    className='right-nav',
                )
            ], 
                xs=6, sm=6, md=6, lg=11, xl=11,
                className='right-nav',
            )
        ])
    ],
        className='navbar'
    )
])

container = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            html.H1('Research on language, personality and development of the countries of the world'),
            html.Br(),
            html.P('--- by Agata Vujić ---'),
            
        ], 
            xs=12, sm=12, md=10, lg=10, xl=10,
            className='hero-text',
        )
    ], 
        justify='around',
        className='hero',
    ),
    dbc.Row([
        dbc.Col([
            html.Br()
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H2('Introduction'),
            html.P(
                '''
                Hello! I am Agata and I am looking forward to starting my career in the Data Science field. This is research 
                that I did out of curiosity and here will be used to demonstrate my analysis process.
                '''
            ),
            html.P([
                '''
                After I learned a bit of Dutch and started to recognize patterns in sentences and not just translate word by 
                word, it came to my mind that I became good at English only when I learned to think in English. And my 
                thinking in English is different than in Croatian which started to bug me. Later on I was introduced to 
                psychologist 
                ''',
                html.A('Alia Crum research on mindsets', 
                       href='https://hubermanlab.com/dr-alia-crum-science-of-mindsets-for-health-performance/'),
                ''' 
                which was very interesting. Then I came to the idea that maybe different languages produce different 
                mindsets and that differences in nations' mindsets might influence development of nations. After doing 
                some research I even  stumbled up on an article 
                ''', 
                html.A('"Evidence for a Cultural Mindset"', 
                       href='https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8461051/'),
                ''' 
                which somewhat confirmed my assumptions.
                '''
            ]),
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ], 
        justify='around',
        id='introduction'
    ),    
    
    
    dbc.Row([
        dbc.Col([
            html.H2('Goal'),
            html.P(
                '''
                I decided that I really want to make a big map on languages and mindsets and figure out what is the correlation 
                between that and the development of countries. Goal is to find out from that map which mindset to keep in mind 
                while learning Dutch and hopefully make that process easier. Also from correlation between development of 
                countries and mindsets, to find out which language will be good to learn next and by doing that, treat myself 
                with some good mindsets.
                '''
            ),
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ], 
        justify='around',
    ),
    
    dbc.Row([
        dbc.Col([
            html.H2('Process'),
            html.P('''
            In the next sections my research and analysis process will be described in 4 steps:
            '''),
            html.Ol([
                html.Li(html.A('Data searching', href='#data_searching')),
                html.Li(html.A('Data cleaning', href='#data_cleaning')),
                html.Li(html.A('Analysis & Visualization', href='#analysis')),
                html.Li(html.A('Presentation of the results', href='#presentation')),
            ]),
            html.P(
                '''
                Going through these steps was not a linear process, of course. I can't count how many times I needed to 
                search for new data again, because data I was already using ended up not being much usable. But with every 
                loop I learned  something interesting. Now in the end I am glad that not everything went as smoothly as I 
                imagined.
                '''
            ),
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ], 
        justify='around',
        id='process'
    ),
    
    dbc.Row([
        dbc.Col([
            html.H3('1. Data Searching'),
            html.P(
                '''
                I mostly searched data by writing out key words and adding .csv to get only results with tables or
                used Google Dataset Search.
                '''
            ),
            html.P([
                '''
                This was the hardest part. I searched through so many articles and found so much data that was not useful 
                at all. At last I found  
                ''',
                html.A('CIA pages', 
                       href='https://www.cia.gov/the-world-factbook/references/guide-to-country-comparisons/'),                
                '''
                 that had a lot of useful and clean tables on and societal data of countries. For language data I settled 
                 on multiple tables that at first were very chaotic: 
                ''',
                html.A('https://github.com/JovianML/...', 
                       href='https://github.com/JovianML/opendatasets/blob/master/data/countries-languages-spoken/countries-languages.csv'),
                ', ',
                html.A('http://www.fullstacks.io/...', 
                       href='http://www.fullstacks.io/2016/07/countries-and-their-spoken-languages.html'),
                ', ',
                html.A('table from Wikipedia', 
                       href='https://en.wikipedia.org/wiki/List_of_official_languages_by_country_and_territory'),
                '''
                and more. For language families data I used 
                ''',
                html.A('Wikitionary table', 
                       href='https://en.wiktionary.org/wiki/Wiktionary:List_of_languages,_csv_format'),
                '''
                and 
                ''',
                html.A('https://github.com/lukes/...', 
                       href='https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv'),
                ''' 
                for country codes. When I tried to find mindsets per country data, results were not usable at all. 
                It turns out that data on mindsets is not so easy to collect with apps, therefore there is not much 
                data on the web. Then I decided that I will do research on personality. Data I used on personality was 
                ''',
                html.A('https://www.kaggle.com/', 
                       href='https://www.kaggle.com/datasets/yamaerenay/mbtitypes-full'),
                '''
                from personality questionnaire 
                ''', 
                html.A('16Personalities', href='https://www.16personalities.com/'),
                '.'
            ]),
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ], 
        justify='around',
        id='data_searching'
    ),
    
    dbc.Row([
        dbc.Col([
            html.H3('2. Data cleaning'),
            html.P('Data cleaning I had done with Python in Jupyter Notebook, using libraries: NumPy, Pandas, re, csv.'),
            html.P([
                '''
                Firstly, I deleted "NaN-s", not relevant columns and similar. Secondly, data on language, personality, 
                economical and societal data had not common key so I needed to combine every table with tables on 
                countries and country codes. After everything was set and done I combined tables in just a few ones 
                that I can use easily.
                '''
            ]),
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ], 
        justify='around',
        id='data_cleaning'
    ),
    
    dbc.Row([
        dbc.Col([
            html.H3('3. Analysis & Visualization'),
            html.P(
                '''
                For analysis and visualization I used Python in Jupyter Notebook and used mostly Pandas and Plotly libraries.
                '''
            ),
            html.P([
                '''
                For the first table I sorted personality types by percentage from the most common to the least
                common personality type per country. This data was used to plot the following maps.
                '''
            ]),
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ], 
        justify='around',
        id='analysis'
    ),
    
    dbc.Row([
        dbc.Col([
            html.H4('Most common personality type per country'),
            dcc.Graph(figure=max_figs[0]),
        ], 
            xs=12, sm=12, md=12, lg=6, xl=6,
        ),
        
        dbc.Col([
            html.H4('Second most common personality type per country'),
            dcc.Graph(figure=max_figs[1]),
        ] ,  
            xs=12, sm=12, md=12, lg=6, xl=6,
        ),
        
        dbc.Col([
            html.Br(),
            html.P(
                '''
                Maps are showing the most common and second most common personality type by country. From the maps we
                can see clearly  that The Diplomats are the most common personality group in the world. Hovering over 
                countries (tap for mobile users) will show more data for selected countries.
                '''
            ),
        ] ,  
            xs=12, sm=12, md=12, lg=12, xl=12,
        )
    ],
        className='graph-row--zelena',
    ),
    
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.P([
                '''
                Colors indicating personality types are selected in a manner to correspond with the colors of 
                personality groups in 
                ''', 
                html.A('16Personalities', href='https://www.16personalities.com/personality-types'),
                ' questionnaire. The Diplomats (', html.A('INFJ', href='https://www.16personalities.com/infj-personality'),
                ', ', html.A('INFP', href='https://www.16personalities.com/infp-personality'),
                ', ', html.A('ENFJ', href='https://www.16personalities.com/enfj-personality'),
                ', ', html.A('ENFP', href='https://www.16personalities.com/enfp-personality'),
                ' personality types) are marked with green colors, the Sentinels (',
                html.A('ISTJ', href='https://www.16personalities.com/istj-personality'),
                ', ', html.A('ISFJ', href='https://www.16personalities.com/isfj-personality'),
                ', ', html.A('ESTJ', href='https://www.16personalities.com/estj-personality'),
                ', ', html.A('ESFJ', href='https://www.16personalities.com/esfj-personality'),
                ') are marked with blue colors, the Analysts (',
                html.A('INTJ', href='https://www.16personalities.com/intj-personality'),
                ', ', html.A('INTP', href='https://www.16personalities.com/intp-personality'),
                ', ', html.A('ENTJ', href='https://www.16personalities.com/entj-personality'),
                ', ', html.A('ENTP', href='https://www.16personalities.com/entp-personality'),
                ') are marked with purple and red colors and the Explorers (',
                html.A('ISTP', href='https://www.16personalities.com/istp-personality'),
                ', ', html.A('ISFP', href='https://www.16personalities.com/isfp-personality'),
                ', ', html.A('ESTP', href='https://www.16personalities.com/estp-personality'),
                ', ', html.A('ESFP', href='https://www.16personalities.com/esfp-personality'),
                ') are marked with yellow and orange colors.'
            ]),
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ], 
        justify='around',
    ),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id='slider-map-container', figure={}),
                dcc.Slider(
                    0, 15, step=1,
                    marks={
                        0:'1st', 1:'2nd', 2:'3rd', 3:'4th', 4:'5th', 5:'6th', 6:'7th', 7:'8th', 8:'9th', 
                        9:'10th', 10:'11th', 11:'12th', 12:'13th', 13:'14th', 14:'15th', 15:'16th',
                    },
                    value=2, id='my-slider'
                ),
                html.P('... most common personality type.'),
            ])
        ], xs=12, sm=12, md=12, lg=12, xl=12),
        dbc.Col([
            html.Br(),
            html.P(
                '''
                From the third most common personality type and on grupations of personality types emerge. Countries
                that have personality types in common are more likely to have the same language genus. Also, sliding 
                through the options from the most to the least common personality type, the transition of the dominant 
                color in the map from the green and blue, over red and violet to the yellow and orange colors can be seen.
                '''
            ),
            html.P(
                '''
                The shift of dominant color indicates that in general the Diplomats are the most common personality 
                group followed by the Sentinels, the Analysts and the least common, the Explorers
                '''
            )
        ],xs=12, sm=12, md=12, lg=12, xl=12)
    ], 
        justify='around',
        className='graph-row--crvena',
    ),
    
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.P(
                '''
                Combining data on the range from the most common to the least common personality per country with 
                data on socioeconomic elements of countries gave me the possibility to explore further.
                '''
            ),
            html.P(
                '''
                For analysis on the development of the countries I decided to focus on GDP per capita and life expectancy 
                metrics. Unlike the other metrics, models from these metrics can be easily approximated with logarithmic 
                function, which is a sign that this model is a good one. Distribution of data in the following chart is 
                linear and not logarithmic as said before. It is because the scale of the x axis is logarithmic and not 
                linear. Logarithmic scale of the x axis makes data distribution more dispersed and transparent.
                '''
            ),
            html.P(
                '''
                Although I focused primarily on GDP per capita and life expectancy for analysis, for the following chart 
                there are more options in the dropdown menus for exploration. There is also a slider below the chart for 
                different bubble color options.
                '''
            ),
        ], xs=12, sm=12, md=10, lg=10, xl=10,)
    ], justify='around'),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Dropdown(id='slct_chart_1',
                             options=[
                                 {'label':'GDP per capita', 'value':'GDP_per_capita_$'},
                                 {'label':'Life expectancy', 'value':'Life_expectancy'},
                                 {'label':'Unemployment rate', 'value':'Unemployment_rate'},                             
                                 {'label':'Migration rate', 'value':'migration_rate'},
                                 {'label':'Population growth rate', 'value':'Population_growth_rate'},
                                 {'label':'GDP growth rate', 'value':'GDP_growth'},
                                 {'label':'GDP in 10^9 $', 'value':'GDP_10^9_$'},
                                 {'label':'Inflation rate', 'value':'Inflation_rate'},
                             ],
                             multi=False,
                             value='GDP_per_capita_$',
                             style={'width':'100%', 'color':'#000000'}
                            ),
            ]),
        ], 
            xs=6, sm=6, md=6, lg=6, xl=6
        ),
                
        dbc.Col([
            html.Div([
                dcc.Dropdown(id='slct_chart_2',
                             options=[
                                 {'label':'GDP per capita', 'value':'GDP_per_capita_$'},
                                 {'label':'Life expectancy', 'value':'Life_expectancy'},
                                 {'label':'Unemployment rate', 'value':'Unemployment_rate'},                             
                                 {'label':'Migration rate', 'value':'migration_rate'},
                                 {'label':'Population growth rate', 'value':'Population_growth_rate'},
                                 {'label':'GDP growth rate', 'value':'GDP_growth'},
                                 {'label':'GDP in 10^9 $', 'value':'GDP_10^9_$'},
                                 {'label':'Inflation rate', 'value':'Inflation_rate'},
                             ],
                             multi=False,
                             value='Life_expectancy',
                             style={'width':'100%', 'color':'#000000'}
                            ),
            ])
            
        ], 
            xs=6, sm=6, md=6, lg=6, xl=6
        ),
        dbc.Col([
            html.Div([
                html.Br(),
                dcc.Graph(id='my_bubble_chart', figure={}),
                dcc.Slider(
                    0, 18, step=1,
                    marks={
                        0:'1st', 1:'2nd', 2:'3rd', 3:'4th', 4:'5th', 5:'6th', 6:'7th', 7:'8th', 8:'9th', 
                        9:'10th', 10:'11th', 11:'12th', 12:'13th', 13:'14th', 14:'15th', 15:'16th',
                        16:'Genus', 17:'Family', 18:'Region' 
                    },
                    value=1, id='slct_chart_3'
                ),
                html.Br(),
                html.P(
                    '''
                    Mapping language genus in this model and representing it with a color of bubbles gave some insights. 
                    Language of the most developed countries (found in the upper right corner) is mostly primarily
                    Germanic. Also looking at less developed countries, Germanic language speaking countries are 
                    less frequent and in these countries Germanic language is often found as secondary official 
                    language of the country.
                    '''
                ),
                html.P(
                    '''
                    After mapping personality types in this model few patterns can be distinguished. Starting from 
                    the most common and moving to the least common personality type results in a shift from green 
                    to yellow color as discussed before. In the charts that show distribution from the most to the 
                    5th most common personality type by country, it can be seen that purple and red colors are more 
                    likely to be found in the upper right quarter of the chart. This means that in more developed 
                    countries, the Analyst personality types are more likely to be one of the most common personality 
                    types. Moving more to the least common personality types, these colors emerge more often both 
                    among more and less developed countries since the Analyst in general is one of the more rare 
                    personality groups.
                    '''
                ),
            
            ]),
            
        ],
            xs=12, sm=12, md=12, lg=12, xl=12,
        )
    ], 
        className='graph-row--plava',
    ),
    
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.P(
                '''
                If we add one more dimension, unemployment rate, in the part with the highest GDP per capita and life 
                expectancy and the lowest unemployment rate, there are still mostly Germanic language speaking countries.
                '''
            ),
        ], xs=12, sm=12, md=10, lg=10, xl=10,)
    ], justify='around'),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_3D),
        ], xs=12, sm=12, md=12, lg=12, xl=12),
    ], 
        justify='around',
        className='graph-row--tirkizna',
    ),
    
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.P(
                '''
                Counting data on personality types of countries whose language belongs to the same genus or family 
                and plotting it confirmed my assumptions. Plotted data was not much dispersed with clear spikes 
                meaning that indeed similar languages produce similar patterns in personality type distribution. 
                These charts are not going to be presented because they are overcrowded with information.
                '''
            ),
            html.P(
                '''
                For the following charts I summed percentages of distinct personality types per country with the 
                languages of the same genus/family. From that I sorted personality types by summed percentage and 
                plotted results.
                '''
            ),
        ], xs=12, sm=12, md=10, lg=10, xl=10,)
    ], justify='around'),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Dropdown(id='gen_go_dropdown',
                             options=gen_options,
                             multi=True,
                             value=['Germanic', 'Romance', 'Slavic'],
                             style={'width':'100%', 'color':'#000000'}
                            ),
                html.Br(),
                dcc.Graph(id='gen_go_bubble', figure={}),
                html.Br(),
                html.P(
                    '''
                    Here is visible how languages of different genus languages produce different patterns of the
                    personality type distribution. It is also visible that the most common and least common 
                    personality is mostly the same in general.
                    '''
                ),
            ]),
        ], xs=12, sm=12, md=12, lg=12, xl=12)
    ],
        justify='around',
        className='graph-row--narancasta',
    ),
    
    dbc.Row(dbc.Col(html.Br())),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Dropdown(id='fam_go_dropdown',
                             options=fam_options,
                             multi=True,
                             value=['Afro-Asiatic','Turkic','Sino-Tibetian'],
                             style={'width':'100%', 'color':'#000000'}
                            ),
                html.Br(),
                dcc.Graph(id='fam_go_bubble', figure={}),
                html.Br(),
                html.P(
                    '''
                    Almost everything that applies for language genus also applies for language families. 
                    Some families are drastically bigger than others (like Indo-European), and in that case 
                    it is probably better to look in the genus chart for only genuses of that language family. 
                    Size of dots indicate sizes of language families.
                    '''
                ),
            ]),
        ], xs=12, sm=12, md=12, lg=12, xl=12)
    ], 
        justify='around',
        className='graph-row--ljubicasta',
    ),
    
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H3('4. Presentation of the results'),
            html.P(
                '''
                This web app was made with the Dash framework in Jupyter Notebook. Last form of this web app was
                converted from .ipynb file to .py file to avoid complications in production.
                '''
            ),
            html.P([
                '''
                I decided that now is not the time for me to learn a new programming language, JavaScript and for
                that this app is made with the Dash framework in Python. Figuring out how to use Bootstrap in Dash 
                was a bit harder but once I did, everything felt easier. Another stepback was styling, but then I 
                found out how to use a custom stylesheet and overwrite the default style. 
                '''
            ]),
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ], 
        justify='around',
        id='presentation'
    ),
    
    dbc.Row([
        dbc.Col([
            html.H2('Conclusion'),
            html.P(
                '''
                To get back to the mindsets I tried to find research on how mindsets and personality affect
                each other. Unfortunately there was no such article on the web.
                '''
            ),
            html.P(
                '''
                In general, Diplomats and secondly Sentinels are the most common personality groups. In more 
                developed countries personalities from the Analyst group are more likely to emerge as one of 
                the most common ones. So for people  that would like to be successful it would be good to learn 
                the language of the countries that have a high percentage of personality types from the Analyst group.
                '''
            ),
            html.P(
                '''
                10 countries with highest percentages in the Analyst personality group are: Algeria, Syria, Morocco, 
                Georgia, Montenegro, Tunisia, Serbia, Bosnia and Herzegovina, Poland and Russia.
                '''
            ),
            html.P(
                '''
                And for learning Dutch I will keep in mind the most common personalities in The Netherlands which 
                are: INFP, ENFP, ESFJ, INFJ, ENFJ, INTP, ISFJ, ENTP.
                '''
            ),
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ], 
        justify='around',
        id='conclusion'
    ),
    
    html.Footer([
        dbc.Row([
            dbc.Col([
                html.H3('Contact'),
                html.P([
                    'E-mail: ', html.A('vujic.agata@gmail.com', href='mailto: vujic.agata@gmail.com')
                ]),
                html.P([
                    'Mobile phone: ', html.A('+385 92 366 6999', href='tel: +385923666999'),
                ])
            ], xs=12, sm=12, md=6, lg=6, xl=6),
            dbc.Col([
                html.H3('More about me'),
                html.P(html.A('LinkedIn', href='https://www.linkedin.com/in/agata-vuji%C4%87-a07779219/')),
                html.P(html.A('Resume', href='https://docs.google.com/document/d/1nuAFoGGmnL9OQYgbZGcqdphfa6l6nDQ7uLn_cLjdifs/edit?usp=sharing')),
            ], xs=12, sm=12, md=6, lg=6, xl=6)
        ], 
            justify='around', 
            className='graph-row--zuta'
        )
    ], 
        id='footer'
    )    
])

app.layout = dbc.Container(
    [navbar, container], 
    fluid=True, style={"padding":0}
)

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)