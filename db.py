from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import app_config
from tables import Database, DatabaseSchema, DatabaseTable, TableField, TableFieldType
from models import DBModel, DBSchemaModel, DBTableModel, TableFieldModel
from pydantic import parse_obj_as
from typing import List


backend_db_conn = app_config.get('DATABASE', 'BACKEND_DB_CONN')


class BackendDBHook:

    def __init__(self):
        self.__engine = create_engine(backend_db_conn)
        self.__Session = sessionmaker(bind=self.__engine)

    def __session_decorator(func):
        def wrapper(self, *args, **kwargs):
            session = self.__Session()
            result = func(self, session, *args, **kwargs)
            session.commit()
            session.close()
            return result
        return wrapper

    @__session_decorator
    def get_all_databases(self, session) -> List[DBModel]:
        return [database.__dict__ for database in session.query(Database).all()]

    @__session_decorator
    def get_database(self, session, database_name: str) -> DBModel:
        return session.query(Database).filter_by(database_name=database_name).first().__dict__

    @__session_decorator
    def get_all_database_schemas(self, session, database_name: str):
        return [schema.__dict__ for schema in session.query(DatabaseSchema).filter_by(database_name=database_name).all()]

    @__session_decorator
    def get_database_schema(self, session, database_name: str, schema_name: str):
        return session.query(DatabaseSchema).filter_by(database_name=database_name,
                                                       database_schema_name=schema_name).first().__dict__

    @__session_decorator
    def get_all_schema_tables(self, session, database_name: str, schema_name: str):
        return [table.__dict__ for table in session.query(DatabaseTable).filter_by(database_name=database_name,
                                                      database_schema_name=schema_name).all()]

    @__session_decorator
    def get_schema_table(self, session, database_name: str, schema_name: str, table_name: str):
        return session.query(DatabaseTable).filter_by(database_name=database_name, database_schema_name=schema_name,
                                                      table_name=table_name).first().__dict__

    @__session_decorator
    def get_all_table_fields(self, session, database_name: str, schema_name: str, table_name: str):
        return [field.__dict__ for field in session.query(TableField).filter_by(database_name=database_name, database_schema_name=schema_name,
                                                   table_name=table_name).all()]

    @__session_decorator
    def get_table_field(self, session, database_name: str, schema_name: str, table_name: str, field_name: str):
        return session.query(TableField).filter_by(database_name=database_name, database_schema_name=schema_name,
                                                   table_name=table_name, field_name=field_name).first().__dict__

    @__session_decorator
    def get_field_type(self, session, field_type_id: int):
        return session.query(TableFieldType).filter_by(field_type_id=field_type_id).first().__dict__

    @__session_decorator
    def add_database(self, session, database: DBModel):
        session.add(Database(**database.dict()))

    @__session_decorator
    def add_database_schema(self, session, schema: DBSchemaModel):
        session.add(DatabaseSchema(**schema.dict()))

    @__session_decorator
    def add_schema_table(self, session, table: DBTableModel):
        session.add(DatabaseTable(**table.dict()))

    @__session_decorator
    def add_table_field(self, session, field: TableFieldModel):
        session.add(TableField(**field.dict()))

    @__session_decorator
    def update_database(self, session, database: DBModel):
        existing_database = session.query(Database).filter_by(database_name=database.database_name).first()
        if existing_database:
            existing_database.database_type = database.database_type
            existing_database.database_url = database.database_url
            existing_database.database_description = database.database_description
            session.commit()
            return existing_database
        else:
            return None

    @__session_decorator
    def update_database_schema(self, session, database_schema: DBSchemaModel):
        existing_schema = session.query(DatabaseSchema).filter_by(
            database_name=database_schema.database_name,
            database_schema_name=database_schema.database_schema_name
        ).first()
        if existing_schema:
            existing_schema.database_schema_description = database_schema.database_schema_description
            session.commit()
            return existing_schema
        else:
            return None

    @__session_decorator
    def update_schema_table(self, session, database_table: DBTableModel):
        existing_table = session.query(DatabaseTable).filter_by(
            database_name=database_table.database_name,
            database_schema_name=database_table.database_schema_name,
            table_name=database_table.table_name
        ).first()
        if existing_table:
            existing_table.table_description = database_table.table_description
            session.commit()
            return existing_table
        else:
            return None

    @__session_decorator
    def update_table_field(self, session, table_field: TableFieldModel):
        existing_field = session.query(TableField).filter_by(
            database_name=table_field.database_name,
            database_schema_name=table_field.database_schema_name,
            table_name=table_field.table_name,
            field_name=table_field.field_name
        ).first()
        if existing_field:
            existing_field.field_type_id = table_field.field_type_id
            existing_field.field_description = table_field.field_description
            session.commit()
            return existing_field
        else:
            return None

    @__session_decorator
    def delete_database(self, session, database_name: str):
        session.query(Database).filter_by(database_name=database_name).delete()
        session.commit()

    @__session_decorator
    def delete_database_schema(self, session, database_name: str, schema_name: str):
        session.query(DatabaseSchema).filter_by(database_name=database_name, database_schema_name=schema_name).delete()
        session.commit()

    @__session_decorator
    def delete_schema_table(self, session, database_name: str, schema_name: str, table_name: str):
        session.query(DatabaseTable).filter_by(database_name=database_name, database_schema_name=schema_name,
                                               table_name=table_name).delete()
        session.commit()

    @__session_decorator
    def delete_table_field(self, session, database_name: str, schema_name: str, table_name: str, field_name: str):
        session.query(TableField).filter_by(database_name=database_name, database_schema_name=schema_name,
                                            table_name=table_name, field_name=field_name).delete()
        session.commit()

