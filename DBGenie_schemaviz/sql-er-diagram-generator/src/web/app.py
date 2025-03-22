from flask import Flask, render_template, request, send_file
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.parser.sql_parser import parse_sql
from src.generator.er_diagram_generator import generate_er_diagram
from src.model_types.entities import Entity, Relationship

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    sql_query = request.form.get('sql_query', '')
    if not sql_query:
        return 'No SQL query provided', 400

    try:
        # Parse the SQL and generate entities/relationships
        parsed_data = parse_sql(sql_query)
        
        # Generate the diagram
        output_path = os.path.join(app.static_folder, 'er_diagram')
        generate_er_diagram(parsed_data['entities'], parsed_data['relationships'], output_path)
        
        return {'success': True, 'image_url': '/static/er_diagram.png'}
    except Exception as e:
        return {'success': False, 'error': str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True) 