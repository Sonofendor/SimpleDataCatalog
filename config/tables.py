from sqlalchemy import (
    Column, String, Integer, DateTime, ForeignKey,
    CheckConstraint, UniqueConstraint, PrimaryKeyConstraint, ForeignKeyConstraint,
    func
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DatabaseType(Base):
    __tablename__ = 'database_types'

    database_type = Column(String, primary_key=True)
    database_type_name = Column(String, nullable=False)


class Database(Base):
    __tablename__ = 'databases'

    database_name = Column(String, primary_key=True)
    database_type = Column(String, ForeignKey('database_types.database_type'))
    database_url = Column(String, nullable=False)
    database_description = Column(String)
    created_at = Column(DateTime, default=func.now(), server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("database_name NOT LIKE '% %'", name='no_spaces_in_database_name'),
    )


class DatabaseSchema(Base):
    __tablename__ = 'database_schemas'

    database_schema_name = Column(String)
    database_name = Column(String, ForeignKey('databases.database_name'), nullable=False)
    database_schema_description = Column(String)
    created_at = Column(DateTime, default=func.now(), server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        PrimaryKeyConstraint('database_schema_name', 'database_name'),
        CheckConstraint("database_schema_name NOT LIKE '% %'", name='no_spaces_in_database_name'),
    )


class DatabaseTable(Base):
    __tablename__ = 'database_tables'

    table_name = Column(String)
    database_schema_name = Column(String, nullable=False)
    database_name = Column(String, nullable=False)
    table_description = Column(String)
    created_at = Column(DateTime, default=func.now(), server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        PrimaryKeyConstraint('table_name', 'database_schema_name', 'database_name'),
        ForeignKeyConstraint(['database_schema_name', 'database_name'],
                             ['database_schemas.database_schema_name', 'database_schemas.database_name']),
        CheckConstraint("table_name NOT LIKE '% %'", name='no_spaces_in_table_name'),
        CheckConstraint("database_schema_name NOT LIKE '% %'", name='no_spaces_in_database_schema_name'),
    )


class TableFieldType(Base):
    __tablename__ = 'table_field_types'

    field_type_id = Column(Integer, primary_key=True, autoincrement=True)
    database_type = Column(String, ForeignKey('database_types.database_type'), nullable=False)
    type_name = Column(String, nullable=False)
    type_description = Column(String)

    __table_args__ = (
        UniqueConstraint('database_type', 'type_name', name='unique_database_type_type_name'),
    )


class TableField(Base):
    __tablename__ = 'table_fields'

    field_name = Column(String)
    table_name = Column(String, nullable=False)
    database_schema_name = Column(String, ForeignKey('database_schemas.database_schema_name'), nullable=False)
    database_name = Column(String,  nullable=False)
    field_type_id = Column(Integer, nullable=False)
    field_description = Column(String)
    created_at = Column(DateTime, default=func.now(), server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        PrimaryKeyConstraint('field_name', 'table_name', 'database_schema_name', 'database_name'),
        ForeignKeyConstraint(
            ['table_name', 'database_schema_name', 'database_name'],
            ['database_tables.table_name', 'database_tables.database_schema_name', 'database_tables.database_name']
        ),
        CheckConstraint("table_name NOT LIKE '% %'", name='no_spaces_in_table_name'),
        CheckConstraint("field_name NOT LIKE '% %'", name='no_spaces_in_field_name'),
    )
