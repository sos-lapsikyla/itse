import os
from typing import Any

from starlette.requests import Request
from starlette.templating import Jinja2Templates

dirname = os.path.dirname(__file__)
template_dir = os.path.join(dirname, "templates")
templates = Jinja2Templates(directory=template_dir)


def get(request: Request) -> Any:
    return templates.TemplateResponse("login.html", {"request": request})


def post(request: Request) -> Any:
    pass
