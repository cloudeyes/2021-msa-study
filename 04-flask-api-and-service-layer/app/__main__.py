from .apps.flask import init_app
import sys 

app = init_app()
app.run(use_reloader=True)

