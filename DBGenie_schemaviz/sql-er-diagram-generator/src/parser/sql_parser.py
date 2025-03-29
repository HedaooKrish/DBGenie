import sqlparse
from model_types.entities import Entity, Relationship

def parse_sql(sql_query):
    """Parse SQL CREATE TABLE statements and extract entities and relationships."""
    statements = sqlparse.parse(sql_query)
    entities = []
    relationships = []
    tables = {}

    # First pass: collect all tables and their columns
    for statement in statements:
        if statement.get_type() == 'CREATE':
            table_name = None
            columns = []
            for token in statement.tokens:
                if token.ttype is None and token.value.upper() == 'TABLE':
                    next_token = statement.token_next(statement.token_index(token))[1]
                    table_name = next_token.value.strip('`"')
                elif isinstance(token, sqlparse.sql.Parenthesis):
                    for item in token.value.strip('()').split(','):
                        item = item.strip()
                        if item.upper().startswith('FOREIGN KEY') or item.upper().startswith('PRIMARY KEY'):
                            continue
                        if item:
                            column_name = item.split()[0].strip('`"')
                            columns.append(column_name)
            if table_name:
                tables[table_name] = columns
                entities.append(Entity(name=table_name, columns=columns))

    # Second pass: collect relationships from foreign keys
    for statement in statements:
        if statement.get_type() == 'CREATE':
            source_table = None
            for token in statement.tokens:
                if token.ttype is None and token.value.upper() == 'TABLE':
                    next_token = statement.token_next(statement.token_index(token))[1]
                    source_table = next_token.value.strip('`"')
                elif isinstance(token, sqlparse.sql.Parenthesis):
                    for item in token.value.strip('()').split(','):
                        item = item.strip().upper()
                        if item.startswith('FOREIGN KEY'):
                            parts = item.split('REFERENCES')
                            if len(parts) == 2:
                                fk_col = parts[0].split('(')[1].split(')')[0].strip('`"').lower()
                                ref_table = parts[1].split('(')[0].strip().strip('`"').lower()
                                cardinality = "1:N"  # Default cardinality
                                relationships.append(
                                    Relationship(source=source_table, target=ref_table, label=f"{fk_col} ({cardinality})")
                                )

    return {
        'entities': entities,
        'relationships': relationships
    }
