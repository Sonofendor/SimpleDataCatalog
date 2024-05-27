from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from db import BackendDBHook
from models import DBModel, DBSchemaModel, DBTableModel, TableFieldModel

router = APIRouter(prefix="/catalog")
backend_db_hook = BackendDBHook()
templates = Jinja2Templates(directory="templates")

def mask_database_url(url: str) -> str:
    protocol, uri = url.split('//')
    credentials, rest = uri.split('@')
    login, password = credentials.split(':')
    masked_password = '*' * len(password)
    masked_url = f"{protocol}//{login}:{masked_password}@{rest}"
    return masked_url


@router.get("/")
def get_catalog(request: Request):
    hook = BackendDBHook()
    databases = hook.get_all_databases()
    for database in databases:
        database['masked_database_url'] = mask_database_url(database['database_url'])
    return templates.TemplateResponse("catalog.html", {"request": request, "databases": databases})


@router.get("/{database_name}")
async def get_database_details(request: Request, database_name: str):
    database = backend_db_hook.get_database(database_name)
    if database:
        schemas = backend_db_hook.get_all_database_schemas(database_name)
        database_type = backend_db_hook.get_database_type(database['database_type'])
        database['database_type_name'] = database_type['database_type_name']
        database['masked_database_url'] = mask_database_url(database['database_url'])
        return templates.TemplateResponse("database.html",
                                      {"request": request, "database_name": database_name, "database": database,
                                       "schemas": schemas})
    else:
        raise HTTPException(status_code=404)


@router.post("/{database_name}/delete")
async def delete_database(database_name: str):
    backend_db_hook.delete_database(database_name)
    return RedirectResponse(url=f"/catalog/", status_code=303)


@router.post("/{database_name}")
async def update_database(database_name: str,
                          database_type: str = Form(...),
                          database_url: str = Form(...),
                          database_description: str = Form(None)):
    new_database = DBModel(database_name=database_name,
                           database_type=database_type,
                           database_url=database_url,
                           database_description=database_description)
    print(new_database)
    database = backend_db_hook.update_database(new_database)
    if database:
        pass
    else:
        backend_db_hook.add_database(new_database)
    return RedirectResponse(url=f"/catalog/{database_name}", status_code=303)


@router.get("/{database_name}/{schema_name}")
async def get_database_schema_details(request: Request, database_name: str, schema_name: str):
    schema = backend_db_hook.get_database_schema(database_name, schema_name)
    if schema:
        tables = backend_db_hook.get_all_schema_tables(database_name, schema_name)
        return templates.TemplateResponse("schema.html",
                                      {"request": request, "schema_name": schema_name, "schema": schema,
                                       "tables": tables})
    else:
        raise HTTPException(status_code=404)


@router.post("/{database_name}/{schema_name}/delete")
async def delete_database_schema(database_name: str, schema_name: str):
    backend_db_hook.delete_database_schema(database_name, schema_name)
    return RedirectResponse(url=f"/catalog/{database_name}", status_code=303)


@router.post("/{database_name}/{schema_name}")
async def update_database_schema(database_name: str, schema_name: str,
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


@router.get("/{database_name}/{schema_name}/{table_name}")
async def get_database_table_details(request: Request, database_name: str, schema_name: str, table_name: str):
    table = backend_db_hook.get_schema_table(database_name, schema_name, table_name)
    if table:
        fields = backend_db_hook.get_all_table_fields(database_name, schema_name, table_name)
        return templates.TemplateResponse("table.html",
                                      {"request": request, "table_name": table_name, "table": table,
                                       "fields": fields})
    else:
        raise HTTPException(status_code=404)


@router.post("/{database_name}/{schema_name}/{table_name}/delete")
async def delete_database_table(database_name: str, schema_name: str, table_name: str):
    backend_db_hook.delete_schema_table(database_name, schema_name, table_name)
    return RedirectResponse(url=f"/catalog/{database_name}/{schema_name}", status_code=303)


@router.post("/{database_name}/{schema_name}/{table_name}")
async def update_database_table(database_name: str, schema_name: str, table_name: str,
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


@router.get("/{database_name}/{schema_name}/{table_name}/{field_name}")
async def get_table_field_details(request: Request, database_name: str, schema_name: str, table_name: str,
                                  field_name: str):
    field = backend_db_hook.get_table_field(database_name, schema_name, table_name, field_name)
    if field:
        field['type_name'] = backend_db_hook.get_field_type(field['field_type_id'])['type_name']
        return templates.TemplateResponse("field.html",
                                      {"request": request, "field_name": field_name, "field": field})
    else:
        raise HTTPException(status_code=404)


@router.post("/{database_name}/{schema_name}/{table_name}/{field_name}/delete")
async def delete_database_table(database_name: str, schema_name: str, table_name: str, field_name: str):
    backend_db_hook.delete_table_field(database_name, schema_name, table_name, field_name)
    return RedirectResponse(url=f"/catalog/{database_name}/{schema_name}/{table_name}", status_code=303)


@router.post("/{database_name}/{schema_name}/{table_name}/{field_name}")
async def update_table_field(database_name: str, schema_name: str, table_name: str, field_name: str,
                             type_name: str = Form(None), field_description: str = Form(None)):
    database_type = backend_db_hook.get_database(database_name)['database_type']
    field_type_id = backend_db_hook.get_field_type_by_name(database_type, type_name)['field_type_id']
    new_field = TableFieldModel(
        database_name=database_name, database_schema_name=schema_name, table_name=table_name,
        field_name=field_name, field_type_id=field_type_id, field_description=field_description
    )
    field = backend_db_hook.update_table_field(new_field)
    if field:
        pass
    else:
        backend_db_hook.add_table_field(new_field)
    return RedirectResponse(url=f"/catalog/{database_name}/{schema_name}/{table_name}/{field_name}", status_code=303)
