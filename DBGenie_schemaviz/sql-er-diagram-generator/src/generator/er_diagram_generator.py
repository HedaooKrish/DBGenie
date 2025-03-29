from graphviz import Digraph 

def generate_er_diagram(entities, relationships, output_path='er_diagram'):
    dot = Digraph(comment='ER Diagram')
    
    # Add entities and their attributes
    for entity in entities:
        entity_shape = 'rectangle'  # Use rectangle for all entities
        dot.node(entity.name, shape=entity_shape, label=entity.name)
        
        for attribute in entity.columns:
            # Ensure attribute is treated as an object with a 'name' key
            attribute_node = f"{entity.name}_{attribute['name']}"
            dot.node(attribute_node, label=attribute['name'], shape='ellipse')  # Use ellipse for attributes
            dot.edge(entity.name, attribute_node)  # Connect entity to attribute

    # Add relationships with cardinality
    for relationship in relationships:
        dot.edge(relationship.source, relationship.target, label=relationship.label)

    dot.render(output_path, format='png')
