def pick_datapoint_histogram(
    data, 
    rows, 
    columns, 
    fig, 
    clicked_points, 
    triggered_id, 
    click,
    index_map 
):
    if rows is not None:
        x_vals = set([data[row][columns[0]] for row in rows])
        fig['layout']['shapes'] = []
        for x in x_vals:
            fig['layout']['shapes'].append({
                'line': {'color': 'red'},
                'type': 'line',
                'x0': x,
                'x1': x,
                'xref': 'x',
                'y0': 0,
                'y1': 1,
                'yref': 'y domain'
            })
    if triggered_id == 'graph':
        bin_val = str(click['points'][0]['binNumber'])
        if bin_val in clicked_points['Histogram']['points']:
            clicked_points['Histogram']['points'].pop(bin_val)
        else:
            if index_map is None:
                clicked_points['Histogram']['points'][bin_val] = (
                    click['points'][0]['pointNumbers']
                )
            else:
                clicked_points['Histogram']['points'][bin_val] = [
                    index_map[str(row)] for row in click['points'][0]['pointNumbers']
                ]

    colors = []
    for i in range(clicked_points['Histogram']['num_unique']):
        if str(i) in clicked_points['Histogram']['points']:
            colors.append('pink')
        else:
            colors.append('blue')

    fig['data'][0]['marker'] = {'color': colors}
    return fig, clicked_points


def pick_datapoint_scatter(data, rows, columns, fig, clicked_points, triggered_id, index_map, click):
    if len(columns) < 2:
        return fig, clicked_points
    else:
        if triggered_id == 'graph':
            point_val = str(click['points'][0]['pointNumber'])
            if point_val in clicked_points['Scatter']:
                clicked_points['Scatter'].pop(point_val)
            else:
                if index_map is None:
                    clicked_points['Scatter'][point_val] = click['points'][0]['pointNumber']
                else:
                    clicked_points['Scatter'][point_val] = index_map[point_val]

        if rows is None:
            rows = []
        row_values = {(data[row][columns[0]], data[row][columns[1]]) for row in rows}
        
        colors = []
        for i in range(len(fig['data'][0]['x'])):
            if (fig['data'][0]['x'][i], fig['data'][0]['y'][i]) in row_values:
                colors.append('red')
            elif str(i) in clicked_points['Scatter']:
                colors.append('pink')
            else:
                colors.append('blue')
        fig['data'][0]['marker'] = {'color': colors}

        return fig, clicked_points