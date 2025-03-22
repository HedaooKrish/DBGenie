from graphviz import Digraph
from types.entities import Entity, Relationship

def generate_er_diagram(entities, relationships):
    dot = Digraph(comment='ER Diagram')
    
    for entity in entities:
        dot.node(entity.name, entity.name)
    
    for relationship in relationships:
        dot.edge(relationship.source, relationship.target, label=relationship.label)
    
    dot.render('er_diagram', format='png')