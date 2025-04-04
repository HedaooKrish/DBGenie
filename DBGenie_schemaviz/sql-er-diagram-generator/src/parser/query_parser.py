import re
from typing import List, Dict, Tuple
from model_types.entities import Relationship

class QueryParser:
    @staticmethod
    def parse_join_query(query: str) -> List[Dict]:
        """
        Parse SQL JOIN queries to extract table relationships
        Returns a list of dictionaries containing source and target tables
        """
        # Convert query to lowercase for easier parsing
        query = query.lower()
        
        # Remove comments and extra whitespace
        query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        query = ' '.join(query.split())
        
        # Extract table names from JOIN clauses
        join_pattern = r'from\s+(\w+)\s+(?:inner|left|right|full)?\s*join\s+(\w+)'
        joins = re.finditer(join_pattern, query)
        
        relationships = []
        for join in joins:
            relationships.append({
                'source': join.group(1),
                'target': join.group(2),
                'type': 'join'
            })
        
        return relationships

    @staticmethod
    def parse_subquery(query: str) -> List[Dict]:
        """
        Parse SQL subqueries to extract potential relationships
        """
        query = query.lower()
        
        # Remove comments and extra whitespace
        query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        query = ' '.join(query.split())
        
        # Extract table names from subqueries
        subquery_pattern = r'from\s+(\w+)\s+where\s+.*?in\s*\(\s*select\s+.*?\s+from\s+(\w+)'
        subqueries = re.finditer(subquery_pattern, query)
        
        relationships = []
        for subquery in subqueries:
            relationships.append({
                'source': subquery.group(1),
                'target': subquery.group(2),
                'type': 'subquery'
            })
        
        return relationships

    @staticmethod
    def parse_union_query(query: str) -> List[Dict]:
        """
        Parse SQL UNION queries to extract potential relationships
        """
        query = query.lower()
        
        # Remove comments and extra whitespace
        query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        query = ' '.join(query.split())
        
        # Extract table names from UNION clauses
        union_pattern = r'from\s+(\w+)\s+union\s+.*?from\s+(\w+)'
        unions = re.finditer(union_pattern, query)
        
        relationships = []
        for union in unions:
            relationships.append({
                'source': union.group(1),
                'target': union.group(2),
                'type': 'union'
            })
        
        return relationships

    @staticmethod
    def parse_query(query: str) -> list[dict]:
        """Parse a query and extract relationships with attributes."""
        relationships = []
    
        # Check if the query contains "FROM" and "JOIN"
        if "FROM" not in query.upper() or "JOIN" not in query.upper():
            print(f"Skipping invalid query: {query}")
            return relationships  # Return an empty list for invalid queries
    
        try:
             # Parse the query to extract source and target entities
             parts = query.upper().split("FROM")
             source_part = parts[1].strip().split()[0]  # Extract the source table
             join_part = query.upper().split("JOIN")[1].strip().split()[0]  # Extract the target table
        
             # Add the relationship
             relationships.append({
                'source': source_part.lower(),
                'target': join_part.lower(),
                'type': 'join'
        })
        except (IndexError, ValueError) as e:
            print(f"Error parsing query: {query}. Error: {e}")
    
        return relationships
