from fastapi import FastAPI, HTTPException
from db import BackendDBHook
from models import DBModel
from typing import List

app = FastAPI()
backend_db_hook = BackendDBHook()


@app.get("/catalog/", response_model=List[DBModel])
def read_catalog():
    databases = backend_db_hook.get_all_databases()
    if not databases:
        raise HTTPException(status_code=404, detail="No databases found")
    return databases


@app.get("/catalog/{database_name}")
def get_database(database_name: str):
    hook = BackendDBHook()
    database = hook.get_database(database_name)
    if database:
        return database
    else:
        raise HTTPException(status_code=404, detail="Database not found")
