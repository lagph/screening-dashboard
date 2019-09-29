import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

MAX_NUM_MODELS = 10


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

add_model_button = html.Button(id='add-model-button', children='add model')
add_model_button_err_cnt = html.Div(id='add-model-button-err-cnt')

model_buttons = html.Div([add_model_button, add_model_button_err_cnt])
model_panel_children = []
for i in range(MAX_NUM_MODELS):
    div_children = []
    recall_title = html.Div(id=f'recall-title-{i}', children='Recall')
    recall_slider = dcc.Slider(id=f'recall-slider-{i}',
                               min=0,
                               max=1,
                               step=1e-4,
                               updatemode='drag',
                               )
    div_children.append(html.Div([recall_title, recall_slider], className="six columns"))
    speci_title = html.Div(id=f'speci-title-{i}', children='Specificity')
    speci_slider = dcc.Slider(id=f'speci-slider-{i}',
                              min=0,
                              max=1,
                              step=1e-4,
                              updatemode='drag'
                              )
    div_children.append(html.Div([speci_title, speci_slider], className="six columns"))
    model_panel_children.append(html.Div(id=f'model-div-{i}', children=div_children,
                                         style={'display': 'none'}, className='row'))


model_panel = html.Div(model_panel_children)
app.layout = html.Div([model_buttons, model_panel])



for i in range(MAX_NUM_MODELS):
    @app.callback([Output(component_id=f'recall-title-{i}', component_property='children'),
                   Output(component_id=f'speci-title-{i}', component_property='children')],
                  [Input(
                      component_id=f'recall-slider-{i}', component_property='value'),
                  Input(
                     component_id=f'speci-slider-{i}', component_property='value')],
                  )
    def recall_callback(recall, speci):
        ret = []
        if recall is None:
            ret.append("Recall")
        else:
            ret.append("Recall = " + str(recall)[:5])
        if speci is None:
            ret.append("Specifcity")
        else:
            ret.append("Specificity = " + str(speci)[:5])
        return ret


@app.callback([Output(component_id=f'model-div-{i}', component_property='style')
               for i in range(MAX_NUM_MODELS)] +
              [Output(component_id='add-model-button-err-cnt',
                      component_property='children')],
              [Input(component_id='add-model-button',
                     component_property='n_clicks')],
              [State(component_id=f'model-div-{i}', component_property='style')
               for i in range(MAX_NUM_MODELS)])
def add_model(n_clicks, *model_divs):
    if n_clicks is None:
        return [{'display': 'none'} for _ in range(MAX_NUM_MODELS)] + [None]
    else:
        num_displayed = len(
            [div for div in model_divs if div['display'] == 'block'])
        if num_displayed == MAX_NUM_MODELS:
            ret = [{'display': 'block'} for _ in range(num_displayed)]
            ret.extend(['Maximum number of models reached!'])
            return ret
        ret = [{'display': 'block'} for _ in range(num_displayed + 1)]
        ret.extend([{'display': 'none'} for _ in range(MAX_NUM_MODELS - num_displayed - 1)])
        ret.extend([None])
        return ret


if __name__ == '__main__':
    app.run_server(debug=True)
