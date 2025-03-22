from database.mysql_connector import MySQLConnector
from parser.sql_parser import parse_sql
from parser.query_parser import QueryParser
from generator.er_diagram_generator import generate_er_diagram
from model_types.entities import Entity, Relationship
import getpass

def get_database_metadata(connector: MySQLConnector, database_name: str) -> tuple[list[Entity], list[Relationship]]:
    """Extract entities and relationships from database metadata"""
    if not connector.use_database(database_name):
        return [], []
    
    entities = []
    relationships = []
    
    # Get all tables
    tables = connector.get_tables()
    
    # Process each table
    for table in tables:
        # Get columns
        columns = connector.get_table_columns(table)
        column_names = [col['name'] for col in columns]
        
        # Create entity
        entities.append(Entity(name=table, columns=column_names))
        
        # Get foreign keys
        foreign_keys = connector.get_foreign_keys(table)
        for fk in foreign_keys:
            relationships.append(Relationship(
                source=table,
                target=fk['referenced_table'],
                label=fk['column']
            ))
    
    return entities, relationships

def get_application_relationships(queries: list[str]) -> list[Relationship]:
    """Extract relationships from application-level queries"""
    relationships = []
    query_parser = QueryParser()
    
    for query in queries:
        parsed_relationships = query_parser.parse_query(query)
        for rel in parsed_relationships:
            relationships.append(Relationship(
                source=rel['source'],
                target=rel['target'],
                label=f"app_level_{rel['type']}"
            ))
    
    return relationships

def main():
    # Get MySQL connection details
    print("MySQL Connection Details:")
    host = input("Host (default: localhost): ").strip() or "localhost"
    user = input("Username (default: root): ").strip() or "root"
    password = getpass.getpass("Password: ").strip()
    
    # Connect to MySQL
    connector = MySQLConnector(host=host, user=user, password=password)
    if not connector.connect():
        print("Failed to connect to MySQL")
        return
    
    try:
        # Get available databases
        databases = connector.get_databases()
        if not databases:
            print("No databases found")
            return
        
        print("\nAvailable databases:")
        for i, db in enumerate(databases, 1):
            print(f"{i}. {db}")
        
        # Let user select database
        while True:
            try:
                db_index = int(input("\nSelect database number: ")) - 1
                if 0 <= db_index < len(databases):
                    break
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        selected_db = databases[db_index]
        
        # Get database-level entities and relationships
        entities, db_relationships = get_database_metadata(connector, selected_db)
        
        # First generate ER diagram with just database relationships
        print("\nGenerating ER diagram based on database structure...")
        generate_er_diagram(entities, db_relationships)
        print("Database ER diagram generated successfully!")
        
        # Ask if user wants to add application-level relationships
        add_app_relationships = input("\nWould you like to add application-level relationships? (y/n): ").lower().strip()
        
        if add_app_relationships == 'y':
            # Get application-level relationships
            print("\nEnter application-level queries (one per line, empty line to finish):")
            queries = []
            while True:
                query = input().strip()
                if not query:
                    break
                queries.append(query)
            
            app_relationships = get_application_relationships(queries)
            
            # Generate new ER diagram with both types of relationships
            if app_relationships:
                print("\nGenerating updated ER diagram with application-level relationships...")
                all_relationships = db_relationships + app_relationships
                generate_er_diagram(entities, all_relationships)
                print("Updated ER diagram generated successfully!")
            else:
                print("No valid application-level relationships found.")
        
    finally:
        connector.close()

if __name__ == "__main__":
    main()