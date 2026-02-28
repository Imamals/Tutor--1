import ast
import sys
import io
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mock lesson data
LESSONS = {
    'variables': {
        'title': 'Variables & Types',
        'content': 'Variables are containers for storing data values. In Python, you can create a variable by assigning a value to a name.',
        'instructions': 'Create a variable and assign it a value. Then print it.',
        'expected_output': None,  # Not used in concept_only mode
        'required_nodes': [ast.Assign, ast.Call],
        'concept_only': True
    }
}

def evaluate_code(code, expected_output, required_nodes, concept_only=False):
    # Capture stdout
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    success = False
    message = ""
    error = None

    try:
        # Check AST
        tree = ast.parse(code)
        found_nodes = list(ast.walk(tree))
        found_types = {type(node) for node in found_nodes}
        
        missing_concepts = []
        for req in required_nodes:
            if req not in found_types:
                missing_concepts.append(req.__name__)

        # Specific check for print call
        has_print = False
        if ast.Call in found_types:
            for node in found_nodes:
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
                    has_print = True
                    break
        
        if ast.Call in required_nodes and not has_print:
            missing_concepts.append("print statement")

        if missing_concepts:
            # Remove duplicates and clean up
            missing_concepts = list(set(missing_concepts))
            message = f"Concept check failed. Missing: {', '.join(missing_concepts)}"
        else:
            # Execute code to check for runtime errors
            exec(code, {})
            output = new_stdout.getvalue()
            
            if concept_only:
                success = True
                message = "Concept mastered! You successfully assigned a variable and printed it."
            else:
                if output == expected_output:
                    success = True
                    message = "Correct! Well done."
                else:
                    message = f"Output check failed. Expected '{expected_output.strip()}', got '{output.strip()}'"

    except Exception as e:
        error = str(e)
        message = f"Error during execution: {error}"
    finally:
        sys.stdout = old_stdout

    return success, message, error

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/editor/<lesson_id>')
def editor(lesson_id):
    lesson = LESSONS.get(lesson_id)
    if not lesson:
        return "Lesson not found", 404
    return render_template('editor.html', lesson=lesson, lesson_id=lesson_id)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    code = data.get('code', '')
    lesson_id = data.get('lesson_id')
    
    lesson = LESSONS.get(lesson_id)
    if not lesson:
        return jsonify({'success': False, 'message': 'Invalid lesson'}), 400
    
    success, message, error = evaluate_code(
        code, 
        lesson.get('expected_output'), 
        lesson['required_nodes'],
        concept_only=lesson.get('concept_only', False)
    )
    
    return jsonify({
        'success': success,
        'message': message,
        'error': error,
        'output': message if not error else error
    })

if __name__ == '__main__':
    app.run(debug=True)
