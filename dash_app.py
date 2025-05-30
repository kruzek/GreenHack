import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import numpy as np
import rasterio
from dijkstra import dijkstra

# Load and store raster data on app startup
tif_file_path = "landuse_cutout.tif"
with rasterio.open(tif_file_path) as dataset:
    band1 = dataset.read(1)

app = dash.Dash(__name__)

def downsample_raster(data, factor):
    if factor <= 1:
        return data
    h, w = data.shape
    h_trim = h - (h % factor)
    w_trim = w - (w % factor)
    trimmed = data[:h_trim, :w_trim]
    downsampled = trimmed.reshape(
        h_trim // factor, factor,
        w_trim // factor, factor
    ).max(axis=(1, 3))
    return downsampled

def create_cost_matrix(data):
    return np.where(data > 0, data, np.inf)

def generate_figure(data, path=None, start=None, goal=None):
    trace_map = go.Heatmap(
        z=data,
        colorscale='Gray',
        showscale=True,
        colorbar=dict(title='Cost')
    )

    data_traces = [trace_map]

    if path:
        path_x, path_y = zip(*path)
        path_trace = go.Scatter(
            x=path_y,
            y=path_x,
            mode='lines+markers',
            line=dict(color='red', width=3),
            marker=dict(color='red', size=3),
            name='Shortest Path'
        )
        data_traces.append(path_trace)

    # Show start and goal points
    if start:
        start_trace = go.Scatter(
            x=[start[1]], y=[start[0]],
            mode='markers',
            marker=dict(color='green', size=10, symbol='circle'),
            name='Start'
        )
        data_traces.append(start_trace)
    if goal:
        goal_trace = go.Scatter(
            x=[goal[1]], y=[goal[0]],
            mode='markers',
            marker=dict(color='blue', size=10, symbol='circle'),
            name='Goal'
        )
        data_traces.append(goal_trace)

    layout = go.Layout(
        title="Cost Map with Shortest Path",
        xaxis=dict(title='Column Index', autorange='reversed'),
        yaxis=dict(title='Row Index', autorange='reversed'),
        clickmode='event+select',
        height=600,
        width=800
    )
    fig = go.Figure(data=data_traces, layout=layout)
    return fig


app.layout = html.Div([
    html.H1("Interactive Dijkstra on Cutout Map"),
    html.Div([
        html.Label("Downsample Factor:"),
        dcc.Dropdown(
            id='downsample-factor',
            options=[
                {'label': str(f), 'value': f} for f in [1, 2, 5, 10]
            ],
            value=1,
            clearable=False,
            style={'width': '100px'}
        ),
        html.Button("Reset Points", id="reset-points", n_clicks=0),
    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '20px', 'marginBottom': '10px'}),

    dcc.Graph(
        id='cost-map',
        figure=generate_figure(band1),
        config={'scrollZoom': True}
    ),

    html.Div(id='selected-points', children="Select start and goal points by clicking on the map."),
    html.Button("Run Dijkstra", id='run-dijkstra', n_clicks=0),
    html.Div(id='path-output')
])

# Store points in memory
start_goal_points = {'start': None, 'goal': None}

@app.callback(
    Output('cost-map', 'figure'),
    Output('selected-points', 'children'),
    Input('cost-map', 'clickData'),
    Input('downsample-factor', 'value'),
    Input('run-dijkstra', 'n_clicks'),
    Input('reset-points', 'n_clicks'),
    State('cost-map', 'figure'),
    prevent_initial_call=True
)
def update_map(clickData, downsample_factor, run_clicks, reset_clicks, current_fig):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    global start_goal_points

    # Reset points if requested
    if triggered_id == 'reset-points':
        start_goal_points = {'start': None, 'goal': None}
        data_down = downsample_raster(band1, downsample_factor)
        fig = generate_figure(data_down)
        return fig, "Select start and goal points by clicking on the map."

    # Update points on click
    if triggered_id == 'cost-map' and clickData:
        point = clickData['points'][0]
        y = int(round(point['y']))
        x = int(round(point['x']))
        if start_goal_points['start'] is None:
            start_goal_points['start'] = (y, x)
            message = f"Start point selected at (row={y}, col={x}). Now select goal point."
        elif start_goal_points['goal'] is None:
            start_goal_points['goal'] = (y, x)
            message = f"Goal point selected at (row={y}, col={x}). Click 'Run Dijkstra' to find path."
        else:
            # Both points selected, do nothing or reset start to new click
            message = "Both points selected. Click 'Reset Points' to choose new points."

        data_down = downsample_raster(band1, downsample_factor)
        fig = generate_figure(data_down, start=start_goal_points['start'], goal=start_goal_points['goal'])
        return fig, message

    # Run Dijkstra when button clicked
    if triggered_id == 'run-dijkstra':
        if start_goal_points['start'] is None or start_goal_points['goal'] is None:
            data_down = downsample_raster(band1, downsample_factor)
            fig = generate_figure(data_down)
            return fig, "Please select both start and goal points before running Dijkstra."

        data_down = downsample_raster(band1, downsample_factor)
        cost_matrix = create_cost_matrix(data_down)
        path = dijkstra(cost_matrix, start_goal_points['start'], start_goal_points['goal'])

        fig = generate_figure(data_down, path=path, start=start_goal_points['start'], goal=start_goal_points['goal'])
        if path:
            message = f"Shortest path found with length {len(path)}."
        else:
            message = "No path found."
        return fig, message

    # On downsample factor change, just update the figure and keep points cleared/reset
    if triggered_id == 'downsample-factor':
        start_goal_points = {'start': None, 'goal': None}
        data_down = downsample_raster(band1, downsample_factor)
        fig = generate_figure(data_down)
        return fig, "Downsample factor changed. Select start and goal points."

    # Default fallback
    data_down = downsample_raster(band1, downsample_factor)
    fig = generate_figure(data_down)
    return fig, "Select start and goal points by clicking on the map."

if __name__ == '__main__':
    app.run(debug=True)
