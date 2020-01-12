from hexlt import hexlt_app,response,event_handler

resp = response()
app = hexlt_app()


def main_handler(event, context):
    global req
    req=event_handler(event)
    return app.run(req,resp)


@app.route("/")
def index():
    return resp.html("index!")
