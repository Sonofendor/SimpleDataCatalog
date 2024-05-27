from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class DBModel(BaseModel):
    database_name: str
    database_type: str
    database_url: str
    database_description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DBModelFullType(BaseModel):
    database_name: str
    database_type_name: str
    database_url: str
    database_description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DBSchemaModel(BaseModel):
    database_schema_name: str
    database_name: str
    database_schema_description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DBTableModel(BaseModel):
    table_name: str
    database_schema_name: str
    database_name: str
    table_description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TableFieldModel(BaseModel):
    field_name: str
    table_name: str
    database_schema_name: str
    database_name: str
    field_type_id: int
    field_description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TableFieldModelFullType(BaseModel):
    field_name: str
    table_name: str
    database_schema_name: str
    database_name: str
    field_type: str
    field_description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)