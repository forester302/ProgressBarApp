import importlib
import pkgutil

from fastapi import FastAPI
from pydantic import BaseModel
from database import session

import os

class SimpleRequest(BaseModel):
    id: int

class SimpleResponse(SimpleRequest): ...

def register(app: FastAPI):
    @app.post("/")
    async def root():
        return {}
    
    module_dir = os.path.dirname(__file__)
    for module_info in pkgutil.iter_modules([module_dir]):
        if not module_info.ispkg:
            module_name = module_info.name

            module = importlib.import_module(
                f".{module_name}", package=__name__)

            if hasattr(module, "register"):
                func = getattr(module, "register")
                func(app, session)
