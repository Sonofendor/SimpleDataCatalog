from db import BackendDBHook
from models import DBModel, DBSchemaModel, DBTableModel, TableFieldModel

# Create a new database
new_database = DBModel(
    database_name="new_database",
    database_type="postgresql",
    database_url="postgresql://username:password@localhost:5432/new_database",
    database_description="Description of the new database"
)

db_hook = BackendDBHook()
db_hook.add_database(new_database)

# Create a new schema in the database
new_schema = DBSchemaModel(
    database_name="new_database",
    database_schema_name="new_schema",
    database_schema_description="Description of the new schema"
)

db_hook.add_database_schema(new_schema)

# Create a new table in the schema
new_table = DBTableModel(
    database_name="new_database",
    database_schema_name="new_schema",
    table_name="new_table",
    table_description="Description of the new table"
)

db_hook.add_schema_table(new_table)

# Create new table fields in the table
new_field1 = TableFieldModel(
    database_name="new_database",
    database_schema_name="new_schema",
    table_name="new_table",
    field_name="field1",
    field_type_id=1,
    field_description="Description of field1"
)

new_field2 = TableFieldModel(
    database_name="new_database",
    database_schema_name="new_schema",
    table_name="new_table",
    field_name="field2",
    field_type_id=2,
    field_description="Description of field2"
)

db_hook.add_table_field(new_field1)
db_hook.add_table_field(new_field2)

updated_database = DBModel(
    database_name="new_database",
    database_type="mysql",
    database_url="mysql://username:password@localhost:3306/new_database",
    database_description="Updated description of the database"
)

# Update the schema
updated_schema = DBSchemaModel(
    database_name="new_database",
    database_schema_name="new_schema",
    database_schema_description="Updated description of the schema"
)

# Update the table
updated_table = DBTableModel(
    database_name="new_database",
    database_schema_name="new_schema",
    table_name="new_table",
    table_description="Updated description of the table"
)

# Update the table fields
updated_field1 = TableFieldModel(
    database_name="new_database",
    database_schema_name="new_schema",
    table_name="new_table",
    field_name="field1",
    field_type_id=3,
    field_description="Updated description of field1"
)

updated_field2 = TableFieldModel(
    database_name="new_database",
    database_schema_name="new_schema",
    table_name="new_table",
    field_name="field2",
    field_type_id=4,
    field_description="Updated description of field2"
)

# Update the objects
db_hook.update_database(updated_database)
db_hook.update_database_schema(updated_schema)
db_hook.update_schema_table(updated_table)
db_hook.update_table_field(updated_field1)
db_hook.update_table_field(updated_field2)

db_hook.delete_table_field("new_database", "new_schema", "new_table", "field1")
db_hook.delete_table_field("new_database", "new_schema", "new_table", "field2")
db_hook.delete_schema_table("new_database", "new_schema", "new_table")
db_hook.delete_schema_table("new_database", "new_schema", "new_table")
db_hook.delete_database("new_database")
