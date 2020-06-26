from starlette.applications import Starlette
from starlette.routing import Route

from . import routes


def create_app() -> Starlette:
    app = Starlette(debug=True, routes=[Route("/auth", routes.auth.get)])
    return app


app = create_app()
