
q_postgresql_get_all = """
SELECT
    table_schema AS schema_name,
    table_name,
    column_name,
    lower(trim(replace(data_type, 'without time zone', ''))) as data_type
FROM 
    information_schema.columns
WHERE
    table_schema NOT IN ('information_schema', 'pg_catalog')
    AND concat_ws('.', table_schema, table_name)::regclass not in (
        SELECT inhrelid::regclass FROM pg_catalog.pg_inherits
    )
ORDER BY 
    table_schema,
    table_name,
    ordinal_position
"""
