import api
import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
template_dir = "templates"
static_dir = "static"
templates = Jinja2Templates(directory=template_dir)

api.register(app)

def template_exists(template_name: str) -> bool:
    return os.path.exists(os.path.join(template_dir, template_name))


def static_file_exists(static_file_name: str) -> bool:
    return os.path.exists(os.path.join(static_dir, static_file_name))


@app.get("/{full_path:path}")
async def catch_all(full_path: str, request: Request):
    static_file_path = full_path or "index.html"
    if static_file_exists(static_file_path):
        return FileResponse(os.path.join(static_dir, static_file_path))

    template_file = f"{full_path or 'index'}.html"
    if template_exists(template_file):
        return templates.TemplateResponse(template_file, {"request": request})
    return FileResponse("static/404.html")
