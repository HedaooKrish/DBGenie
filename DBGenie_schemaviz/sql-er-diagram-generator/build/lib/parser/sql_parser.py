import sqlparse

def parse_sql(sql_query):
    parsed = sqlparse.parse(sql_query)
    # Extract tables, columns, and relationships from parsed SQL
    # For now, just return the parsed object
    return parsed