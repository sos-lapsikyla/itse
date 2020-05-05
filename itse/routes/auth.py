import os

from starlette.templating import Jinja2Templates

dirname = os.path.dirname(__file__)
template_dir = os.path.join(dirname, "templates")
templates = Jinja2Templates(directory=template_dir)


class Auth:
    def get(request):
        return templates.TemplateResponse("login.html", {"request": request})

    def post(request):
        pass
