def pick_datapoint_histogram(data, rows, columns, fig, clicked_points, triggered_id, click):
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
    clicked_points['Histogram'][0] = set(clicked_points['Histogram'][0])
    if triggered_id == 'graph':
        if click['points'][0]['binNumber'] in clicked_points['Histogram'][0]:
            clicked_points['Histogram'][0].remove(click['points'][0]['binNumber'])
        else:
            clicked_points['Histogram'][0].add(click['points'][0]['binNumber'])
    colors = []
    for i in range(clicked_points['Histogram'][1]):
        if i in clicked_points['Histogram'][0]:
            colors.append('red')
        else:
            colors.append('blue')

    fig['data'][0]['marker'] = {'color': colors}
    clicked_points['Histogram'][0] = list(clicked_points['Histogram'][0])
    return fig, clicked_points


def pick_datapoint_scatter(data, rows, columns, fig, clicked_points, triggered_id, click):
    if len(columns) < 2:
        return fig, clicked_points
    else:
        clicked_points['Scatter'] = {
            tuple(point) for point in clicked_points['Scatter']
        }
        if triggered_id == 'graph':
            if (click['points'][0]['x'], click['points'][0]['y']) in clicked_points['Scatter']:
                clicked_points['Scatter'].remove((
                    click['points'][0]['x'],
                    click['points'][0]['y']
                ))
            else:
                clicked_points['Scatter'].add((
                    click['points'][0]['x'],
                    click['points'][0]['y']
                ))
        point_values = set()
        if rows is not None:
            for row in rows:
                point_values.add((data[row][columns[0]], data[row][columns[1]]))
        red_points = point_values.update(clicked_points['Scatter'])
        colors = []
        for x, y in zip(fig['data'][0]['x'], fig['data'][0]['y']):
            if (x, y) in point_values:
                colors.append('red')
            else:
                colors.append('blue')
        fig['data'][0]['marker'] = {'color': colors}
        clicked_points['Scatter'] = list(clicked_points['Scatter'])
        return fig, clicked_points