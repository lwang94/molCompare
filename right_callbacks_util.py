def populate_filtered_table_histogram(data, children, rows, click, filtered_rows):
    if rows is None:
        rows = []
    initial_rows = set(rows)
    graph_rows = []
    for _bin in click['Histogram']['points']:
        for row in click['Histogram']['points'][_bin]:
            if row not in initial_rows:
                graph_rows.append(row)

    style_data_conditional=[{
        'if': {'column_id': 'SMILES'},
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0
    }]
    style_data_conditional += [
        {
            'if': {'row_index': i},
            'backgroundColor': 'red',
            'color': 'white'
        } for i in range(len(initial_rows))
    ]
    style_data_conditional += [
        {
            'if': {'row_index': i},
            'backgroundColor': 'pink'
        } for i in range(len(initial_rows), len(initial_rows) + len(graph_rows))
    ]
            
    filtered_rows = set(filtered_rows)
    data_rows = []
    for row in rows + graph_rows:
        data_rows.append(row)
        if row in filtered_rows:
            filtered_rows.remove(row)
    data_rows += list(filtered_rows)
    return (
        [data[row] for row in data_rows],
        [children['props']['data'][2][row] for row in data_rows], 
        style_data_conditional, 
        data_rows
    )


def populate_filtered_table_scatter(data, children, rows, click, filtered_rows):
    if rows is None:
        rows = []
    initial_rows = set(rows)
    graph_rows = []
    for point in click['Scatter']:
        if click['Scatter'][str(point)] not in initial_rows:
            graph_rows.append(click['Scatter'][str(point)])

    style_data_conditional=[{
        'if': {'column_id': 'SMILES'},
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0
    }]
    style_data_conditional += [
        {
            'if': {'row_index': i},
            'backgroundColor': 'red',
            'color': 'white'
        } for i in range(len(initial_rows))
    ]
    style_data_conditional += [
        {
            'if': {'row_index': i},
            'backgroundColor': 'pink'
        } for i in range(len(initial_rows), len(initial_rows) + len(graph_rows))
    ]

    filtered_rows = set(filtered_rows)
    data_rows = []
    for row in rows + graph_rows:
        data_rows.append(row)
        if row in filtered_rows:
            filtered_rows.remove(row)
    data_rows += list(filtered_rows)
    return (
        [data[row] for row in data_rows],
        [children['props']['data'][2][row] for row in data_rows], 
        style_data_conditional, 
        data_rows
    )