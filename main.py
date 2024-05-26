from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from db import BackendDBHook
from models import DBModel, DBSchemaModel, DBTableModel, TableFieldModelFullType

app = FastAPI()
templates = Jinja2Templates(directory="templates")
backend_db_hook = BackendDBHook()


@app.get("/catalog")
def get_catalog(request: Request):
    hook = BackendDBHook()
    databases = hook.get_all_databases()
    return templates.TemplateResponse("catalog.html", {"request": request, "databases": databases})


@app.get("/catalog/{database_name}")
async def get_database_details(request: Request, database_name: str):
    database = backend_db_hook.get_database(database_name)
    schemas = backend_db_hook.get_all_database_schemas(database_name)
    return templates.TemplateResponse("database.html",
                                      {"request": request, "database_name": database_name, "database": database,
                                       "schemas": schemas})


@app.post("/catalog/{database_name}")
async def update_database(database_name: str,
                          database_type: str = Form(...),
                          database_url: str = Form(...),
                          database_description: str = Form(None)):
    new_database = DBModel(database_name=database_name,
                           database_type=database_type,
                           database_url=database_url,
                           database_description=database_description)
    database = backend_db_hook.update_database(new_database)
    if database:
        pass
    else:
        backend_db_hook.add_database(new_database)
    return RedirectResponse(url=f"/catalog/{database_name}", status_code=303)


@app.get("/catalog/{database_name}/{schema_name}")
async def get_database_details(request: Request, database_name: str, schema_name: str):
    schema = backend_db_hook.get_database_schema(database_name, schema_name)
    tables = backend_db_hook.get_all_schema_tables(database_name, schema_name)
    return templates.TemplateResponse("schema.html",
                                      {"request": request, "schema_name": schema_name, "schema": schema,
                                       "tables": tables})


@app.post("/catalog/{database_name}/{schema_name}")
async def update_database(database_name: str, schema_name: str,
                          database_schema_description: str = Form(None)):
    new_schema = DBSchemaModel(database_name=database_name,
                               database_schema_name=schema_name,
                               database_schema_description=database_schema_description)
    schema = backend_db_hook.update_database_schema(new_schema)
    if schema:
        pass
    else:
        backend_db_hook.add_database_schema(new_schema)
    return RedirectResponse(url=f"/catalog/{database_name}/{schema_name}", status_code=303)


@app.get("/catalog/{database_name}/{schema_name}/{table_name}")
async def get_database_details(request: Request, database_name: str, schema_name: str, table_name: str):
    table = backend_db_hook.get_schema_table(database_name, schema_name, table_name)
    fields = backend_db_hook.get_all_table_fields(database_name, schema_name, table_name)
    return templates.TemplateResponse("table.html",
                                      {"request": request, "table_name": table_name, "table": table,
                                       "fields": fields})


@app.post("/catalog/{database_name}/{schema_name}/{table_name}")
async def update_database(database_name: str, schema_name: str, table_name: str,
                          table_description: str = Form(None)):
    new_table = DBTableModel(database_name=database_name,
                             database_schema_name=schema_name,
                             table_name=table_name,
                             table_description=table_description)
    table = backend_db_hook.update_schema_table(new_table)
    if table:
        pass
    else:
        backend_db_hook.add_schema_table(new_table)
    return RedirectResponse(url=f"/catalog/{database_name}/{schema_name}/{table_name}", status_code=303)


@app.get("/catalog/{database_name}/{schema_name}/{table_name}/{field_name}")
async def get_database_details(request: Request, database_name: str, schema_name: str, table_name: str,
                               field_name: str):
    field = backend_db_hook.get_table_field(database_name, schema_name, table_name, field_name)
    field['field_type'] = backend_db_hook.get_field_type(field['field_type_id'])['type_name']
    return templates.TemplateResponse("field.html",
                                      {"request": request, "field_name": field_name, "field": field})

# TO DO: finish
@app.post("/catalog/{database_name}/{schema_name}/{table_name}/{field_name}")
async def update_database(database_name: str, schema_name: str, table_name: str, field_name: str,
                          field_description: str = Form(None)):
    new_field = TableFieldModel(database_name=database_name,
                             database_schema_name=schema_name,
                             table_name=table_name,
                             field_name=field_name,
                             field_description=field_description)
    field = backend_db_hook.update_table_field(new_field)
    if field:
        pass
    else:
        backend_db_hook.add_table_field(new_field)
    return RedirectResponse(url=f"/catalog/{database_name}/{schema_name}/{table_name}/{field_name}", status_code=303)
