from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser
from config.tables import Database, DatabaseSchema, DatabaseTable, TableField
from config.sql import q_postgresql_get_all


config = ConfigParser()
config.read('sdc.conf')
backend_db_conn = config.get('DATABASE', 'BACKEND_DB_CONN')


def connect_to_backend_db():
    return create_engine(backend_db_conn)


class Extractor:

    def __init__(self, database_name):
        self.__backend_engine = connect_to_backend_db()

        session_maker = sessionmaker(bind=self.__backend_engine)
        session = session_maker()
        database = session.query(Database).filter_by(database_name=database_name).first()
        if not database:
            raise ValueError(f'No database with provided name was found: {database_name}')
        session.close()
        self.__db_engine = create_engine(database.database_url)
        self.__db_name = database.database_name
        self.__db_type = database.database_type
        if self.__db_type == 'postgresql':
            self.__q_get_all = q_postgresql_get_all

    def __get_backend_session(self):
        session_maker = sessionmaker(bind=self.__backend_engine)
        return session_maker()

    def __get_source_session(self):
        session_maker = sessionmaker(bind=self.__db_engine)
        return session_maker()

    def __extract_all(self):
        source_session = self.__get_source_session()
        results = source_session.execute(text(self.__q_get_all))
        source_session.close()
        return results

    def extract_and_add_to_backend(self):
        backend_session = self.__get_backend_session()
        results = self.__extract_all()
        with backend_session.no_autoflush:
            added_schemas = []
            added_tables = []
            added_fields = []
            for result in results:
                schema_name, table_name, column_name, data_type = result
                schema = backend_session.query(DatabaseSchema).filter_by(
                    database_name=self.__db_name, database_schema_name=schema_name
                ).first()
                if not schema and schema_name not in added_schemas:
                    schema = DatabaseSchema(database_name=self.__db_name, database_schema_name=schema_name)
                    backend_session.add(schema)
                    added_schemas.append(schema_name)

                table = backend_session.query(DatabaseTable).filter_by(
                    table_name=table_name, database_schema_name=schema_name, database_name=self.__db_name
                ).first()
                if not table and (schema_name, table_name) not in added_tables:
                    table = DatabaseTable(
                        database_name=self.__db_name, database_schema_name=schema_name, table_name=table_name
                    )
                    backend_session.add(table)
                    added_tables.append((schema_name, table_name))

                field_type_id = backend_session.execute(
                    text("""SELECT field_type_id FROM table_field_types 
                                WHERE database_type=:db_type AND type_name=:type_name"""),
                    {"db_type": self.__db_type, "type_name": data_type}
                ).scalar()

                field = backend_session.query(TableField).filter_by(
                    field_name=column_name, table_name=table_name,
                    database_schema_name=schema_name, database_name=self.__db_name
                ).first()
                if not field and (schema_name, table_name, column_name) not in added_fields:
                    field = TableField(
                        database_name=self.__db_name, database_schema_name=schema_name,
                        table_name=table_name, field_name=column_name, field_type_id=field_type_id
                    )
                    backend_session.add(field)
                    added_fields.append((schema_name, table_name, column_name))

        backend_session.commit()
        backend_session.close()


extractor = Extractor('dit_dwh')
extractor.extract_and_add_to_backend()
