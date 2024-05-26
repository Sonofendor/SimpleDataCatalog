from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import app_config
from config.types import database_types, field_types
from tables import Base, DatabaseType, TableFieldType


backend_db_conn = app_config.get('DATABASE', 'BACKEND_DB_CONN')
engine = create_engine(backend_db_conn, echo=True)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

for database_type, database_type_name in database_types.items():
    new_db_type = DatabaseType(
        database_type=database_type,
        database_type_name=database_type_name
    )
    session.add(new_db_type)

for database_type, types in field_types.items():
    for type_name, type_description in types.items():
        new_field_type = TableFieldType(
            database_type=database_type,
            type_name=type_name,
            type_description=type_description
        )
        session.add(new_field_type)

session.commit()
session.close()
