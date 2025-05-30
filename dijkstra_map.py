import numpy as np
import rasterio
import plotly.graph_objs as go
from dijkstra import dijkstra

def load_raster(tif_file_path):
    with rasterio.open(tif_file_path) as dataset:
        band1 = dataset.read(1)
    return band1

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

def run_dijkstra(cost_matrix, start, goal):
    return dijkstra(cost_matrix, start, goal)

def plot_map_with_path(data, path=None, start=None, goal=None):
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
