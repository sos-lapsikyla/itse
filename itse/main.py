from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

import uvicorn

import routes

async def login_page(request):
    return JSONResponse({'hello': 'world'})

def create_app():
    app = Starlette(debug=True, routes=[
        Route('/auth', routes.Auth.get),
    ])
    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
