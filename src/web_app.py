from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from python_analyzer.analyzer import PythonAnalyzer
from java_generator.generator import JavaGenerator
from pygments import highlight
from pygments.lexers import PythonLexer, JavaLexer
from pygments.formatters import HtmlFormatter
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """
    Translate Python code to Java and return the result with semantic differences.
    """
    try:
        data = request.get_json()
        python_code = data.get('python_code', '')

        # Initialize components
        analyzer = PythonAnalyzer()
        generator = JavaGenerator()

        # Analyze and translate
        ast = analyzer.analyze(python_code)
        java_code = generator.generate(ast)
        differences = analyzer.get_semantic_differences()

        # Highlight the code for better presentation
        highlighted_python = highlight(python_code, PythonLexer(), HtmlFormatter())
        highlighted_java = highlight(java_code, JavaLexer(), HtmlFormatter())

        return jsonify({
            'status': 'success',
            'java_code': java_code,
            'highlighted_python': highlighted_python,
            'highlighted_java': highlighted_java,
            'semantic_differences': differences
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 