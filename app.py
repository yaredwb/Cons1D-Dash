# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import theory as theory
from anasol import analyticalSolution

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, static_folder='static')
app.scripts.append_script({ 'external_url' : mathjax })

app.title = 'Consolidation 1D'

app.layout = html.Div([

  html.Div([

    html.Div([
      html.H2(children='Consolidation 1D')
    ], className='banner'),

    html.Div([

      html.Div([
        html.H4(children='Governing Equation'),
        html.P(children=theory.th['gov'])
      ], className='six columns'),

      html.Div([
        html.H4(children='Analytical Solution'),
        html.P(children=theory.th['ana']),
        html.P(children=theory.th['deg'])
      ], className='six columns')

    ], className='row boundary', style={'text-align': 'justify'}),

    html.H6('Demo', className='boundary', style={'text-align': 'center', 'background-color': 'rgb(234, 229, 240)'}),

    html.Div([

      html.Div([
        html.Div([
          html.P('Boundary drainage condition:', style={'margin-top': '15'}),
          dcc.Dropdown(
            id='drainage',
            options=[
              {'label': 'Top and bottom', 'value': 'tb'},
              {'label': 'Top only', 'value': 't'},
              {'label': 'Bottom only', 'value': 'b'}
            ],
            value='tb',
            clearable=False
          ),
          html.Br(),
          html.Div([
            html.P(r'Model height, \( H \) [m]:', className='one-half column'),
            html.P(r'Initial pore pressure, \( u_o \) [kPa]:', className='one-half column')
          ], className='row'),
          dcc.Input(
            id='height',
            value=2,
            type='number',
            min=1,
            style={'width': '50%'}
          ),
          dcc.Input(
            id='excess-u',
            value=100,
            type='number',
            min=10,
            style={'width': '50%'}
          )
        ])
      ], className='six columns'),

      html.Div([
        html.P(r'Coefficient of consolidation, \( c_v~[\mathrm{cm^2/s}] \):', style={'margin-top': '15'}),
        dcc.Slider(
          id='cons-coeff',
          min=-6,
          max=1,
          step=0.1,
          value=-3,
          marks={i: '{}'.format(10 ** i) for i in list(range(-6,2))},
          included=False
        ),
        html.Div(
          id='selected-cv',
          style={'padding-top': '20', 'text-align': 'center'}
        ),
        html.P(children=r'Dimensionless time, \( T \):'),
        dcc.RangeSlider(
          id='dimensionless-time',
          min=-4,
          max=1,
          step=0.1,
          value=[-2,0.176091],
          marks={i: '{}'.format(10 ** i) for i in list(range(-4,2))}
        ),
        html.Div(
          id='selected-time-range',
          style={'padding-top': '20', 'text-align': 'center'}
        )
      ], className='six columns')

    ], className='row boundary'),

    html.Br(),

    html.Div([
      html.Div(
        id='div-graph1',
        children=[
          dcc.Graph()
        ],
        className='six columns'
      ),
      html.Div(
        id='div-graph2',
        children=[
          dcc.Graph()
        ],
        className='six columns'
      )
    ], className='row boundary', style={'margin-top': '-15'})

  ], className='content'),

  html.Div([

    html.Div([
      html.A(
        [html.Img(src='/static/GitHub-Mark-32px.png')],
        href='https://github.com/yaredwb?tab=repositories',
        target='_blanc'
      ),
      html.A(
        [html.Img(src='/static/Twitter_Social_Icon_Circle_Color.png')],
        href='https://twitter.com/yaredwb',
        target='_blanc'
      ),
      html.A(
        [html.Img(src='/static/In-2C-28px-R.png')],
        href='https://www.linkedin.com/in/yaredworku',
        target='_blanc'
      )
    ], className='six columns'),
    html.Div([
      html.P('Powered by: Plotly Dash')
    ], className='six columns')

  ], className='row footer')

], className='container-mod')

@app.callback(
  Output('selected-cv', 'children'),
  [Input('cons-coeff', 'value')]
)
def updateConsCoeff(value):
  return 'Selected value: {:0.3e}'.format(10**value)

@app.callback(
  Output('selected-time-range', 'children'),
  [Input('dimensionless-time', 'value')]
)
def updateRange(selected_range):
  T_range = [10**i for i in selected_range]
  return 'Selected range: [{:0.4f}, {:0.3f}]'.format(T_range[0], T_range[1])

@app.callback(
  Output('div-graph1', 'children'),
  [Input('height', 'value'),
   Input('cons-coeff', 'value'),
   Input('excess-u', 'value'),
   Input('dimensionless-time', 'value'),
   Input('drainage', 'value')]
)
def updateGraph1(H, cv, uo, selected_range, drainage):
  data1, _ = analyticalSolution(H, cv, uo, selected_range, drainage)
  return [
    dcc.Graph(
      id='anasol',
      figure={
        'data': data1,
        'type': 'bar',
        'layout': {
          'xaxis': {
            'title': 'Pore pressure, u [kPa]',
            'mirror': True,
            'ticks': 'outside',
            'showline': True,
            'zeroline': False
          },
          'yaxis': {
            'title': 'Height, H [m]',
            'mirror': True,
            'ticks': 'outside',
            'showline': True,
            'zeroline': False
          },
          'showlegend': False,
          'width': 580,
          'height': 450,
          'margin': {
            "r": 45,
            "t": 45,
            "b": 45,
            "l": 50
          }
        }
      },
      style={
        'align': 'center',
        'padding-top': '15',
        'padding-bottom': '15',
        'margin-left': '30'
      }
    )
  ]

@app.callback(
  Output('div-graph2', 'children'),
  [Input('height', 'value'),
   Input('cons-coeff', 'value'),
   Input('excess-u', 'value'),
   Input('dimensionless-time', 'value'),
   Input('drainage', 'value')]
)
def updateGraph2(H, cv, uo, selected_range, drainage):
  _, data2 = analyticalSolution(H, cv, uo, selected_range, drainage)
  return [
    dcc.Graph(
      id='degree-of-cons',
      figure={
        'data': data2,
        'layout': {
          'xaxis': {
            'title': 'Dimensionless time, T',
            'type': 'log',
            'mirror': True,
            'ticks': 'outside',
            'showline': True
          },
          'xaxis2': {
            'title': 'Real time, t (days)',
            'overlaying': 'x',
            'side': 'top',
            'type': 'log',
            'mirror': True,
            'ticks': 'outside',
            'showline': True
          },
          'yaxis': {
            'title': 'Degree of consolidation, U [%]',
            'autorange': 'reversed',
            'mirror': True,
            'ticks': 'outside',
            'showline': True,
            'zeroline': False
          },
          'showlegend': False,
          'width': 580,
          'height': 450,
          'margin': {
            "r": 45,
            "t": 45,
            "b": 45,
            "l": 50
          }
        }
      },
      style={
        'align': 'center',
        'padding-top': '15',
        'padding-bottom': '15',
        'margin-right': '30'
      }
    )
  ]

if __name__ == "__main__":
  app.run_server(debug=False)