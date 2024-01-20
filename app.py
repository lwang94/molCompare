from dash import html
from dash_extensions.enrich import DashProxy, BlockingCallbackTransform

from upload_layout import upload
from left_layout import left
from right_layout import right

from upload_callbacks import callbacks_upload
from left_callbacks import callbacks_left
from right_callbacks import callbacks_right

app = DashProxy(transforms=[BlockingCallbackTransform(timeout=5)])

app.layout = html.Div([
    upload(),
    left(),
    right()
])

callbacks_upload(app)
callbacks_left(app)
callbacks_right(app)


if __name__ == '__main__':
    app.run(debug=True)