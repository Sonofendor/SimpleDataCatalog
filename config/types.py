
database_types = {
    'postgresql': 'PostgreSQL',
}

field_types = {
    'postgresql': {
        "array": "array of values",
        "bigint": "signed eight-byte integer",
        "bigserial": "autoincrementing eight-byte integer",
        "bit": "fixed-length bit string",
        "bit varying": "variable-length bit string",
        "boolean": "logical Boolean",
        "box": "rectangular box on a plane",
        "bytea": "binary data",
        "character": "fixed-length character string",
        "character varying": "variable-length character string",
        "cidr": "IPv4 or IPv6 network address",
        "circle": "circle on a plane",
        "date": "calendar date",
        "double precision": "double precision floating-point number",
        "inet": "IPv4 or IPv6 host address",
        "integer": "signed four-byte integer",
        "interval": "time span",
        "json": "textual JSON data",
        "jsonb": "binary JSON data, decomposed",
        "line": "infinite line on a plane",
        "lseg": "line segment on a plane",
        "macaddr": "MAC address",
        "macaddr8": "MAC address",
        "money": "currency amount",
        "numeric": "exact numeric of selectable precision",
        "path": "geometric path on a plane",
        "pg_lsn": "PostgreSQL Log Sequence Number",
        "pg_snapshot": "user-level transaction ID snapshot",
        "point": "geometric point on a plane",
        "polygon": "closed geometric path on a plane",
        "real": "single precision floating-point number",
        "smallint": "signed two-byte integer",
        "smallserial": "autoincrementing two-byte integer",
        "serial": "autoincrementing four-byte integer",
        "text": "variable-length character string",
        "time": "time of day",
        "timetz": "time of day, including time zone",
        "timestamp": "date and time",
        "timestamptz": "date and time, including time zone",
        "tsquery": "text search query",
        "tsvector": "text search document",
        "txid_snapshot": "user-level transaction ID snapshot",
        "uuid": "universally unique identifier",
        "xml": "XML data"
    }
}
