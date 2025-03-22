from graphviz import Digraph
from model_types.entities import Entity, Relationship

def generate_er_diagram(entities, relationships, output_path='er_diagram'):
    dot = Digraph(comment='ER Diagram')
    
    for entity in entities:
        dot.node(entity.name, entity.name)
    
    for relationship in relationships:
        dot.edge(relationship.source, relationship.target, label=relationship.label)
    
    dot.render(output_path, format='png')