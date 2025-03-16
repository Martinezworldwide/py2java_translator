# Python to Java Translator
Created by University student Sebastian Martinez - Digital Electronics & Computer Architecture class


A modern web application that translates Python code to Java with intelligent semantic analysis, syntax highlighting, and a beautiful carbon-fiber themed UI.

## Features

### Translation Capabilities
- Converts Python code to equivalent Java code with semantic awareness
- Handles complex Python constructs:
  - Functions with type hints and decorators
  - Classes with inheritance and special methods
  - Control flow (if/else, match/case)
  - Loops (for/while) with Python-specific features
  - Data structures (lists, dictionaries, sets)
  - Exception handling and context managers
  - File operations and I/O
  - Type inference and coercion

### User Interface
- Modern carbon-fiber themed dark interface
- Real-time syntax highlighting using CodeMirror
- Side-by-side code editors for Python and Java
- Semantic analysis display
- Pre-built code samples demonstrating language differences
- Mobile-responsive design
- Interactive code editing with IDE features

### Code Analysis
- Detailed semantic difference analysis
- Type system comparisons
- Control flow analysis
- Object-oriented feature mapping
- Standard library usage differences
- Error handling patterns
- Best practices recommendations

## Technologies Used

### Frontend
- HTML5/CSS3 with CSS Grid and Flexbox
- JavaScript (ES6+)
- CodeMirror 5.65.2 for code editing
  - Python and Java syntax highlighting
  - Theme: Dracula
  - Bracket matching and auto-closing
- Font Awesome 6.0.0 for icons
- Responsive design with media queries

### Backend
- Python 3.9.18
- Flask 2.3.3 web framework
- Flask-CORS 4.0.0 for cross-origin support
- Gunicorn 21.2.0 WSGI server
- AST (Abstract Syntax Tree) module for Python parsing
- Pygments 2.16.1 for code highlighting
- Astroid 2.15.0 for Python code analysis

### Development Tools
- Virtual environment (venv)
- Git version control
- setuptools for package management
- Requirements.txt for dependency management

### Deployment
- Render.com for cloud hosting
- GitHub integration for CI/CD
- Environment variables for configuration
- Docker containerization

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/Martinezworldwide/py2java_translator.git
cd py2java_translator
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export FLASK_APP=src/web_app.py
export FLASK_ENV=development
export PORT=5000  # Optional, defaults to 5000
```

5. Run the development server:
```bash
flask run
```

The application will be available at http://localhost:5000

## Project Structure
```
py2java_translator/
├── src/
│   ├── __init__.py
│   ├── web_app.py              # Flask application
│   │   ├── __init__.py
│   │   └── web_app.py
│   ├── python_analyzer/        # Python code analysis
│   │   ├── __init__.py
│   │   └── analyzer.py
│   ├── java_generator/         # Java code generation
│   │   ├── __init__.py
│   │   └── generator.py
│   └── templates/              # HTML templates
│       └── index.html
├── requirements.txt            # Python dependencies
├── setup.py                   # Package configuration
├── render.yaml                # Render.com configuration
└── README.md
```

## Deployment

This application is deployed on Render.com. To deploy your own instance:

1. Fork this repository to your GitHub account
2. Create a new account on Render.com
3. Connect your GitHub repository
4. Create a new Web Service with these settings:
   - Name: py2java-translator
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.web_app:app`
   - Python Version: 3.9.18
   - Environment: Python
   - Plan: Free
   - Environment Variables:
     - PYTHON_VERSION: 3.9.18
     - PORT: 10000

The application will be available at `https://your-service-name.onrender.com`

## API Endpoints

### Main Interface
- `GET /`: Web interface for the translator

### Translation API
- `POST /translate`
  - Request body: `{"python_code": "your_python_code_here"}`
  - Response: 
    ```json
    {
      "status": "success",
      "java_code": "translated_java_code",
      "semantic_differences": [
        {
          "feature": "feature_name",
          "python": "python_behavior",
          "java": "java_behavior"
        }
      ]
    }
    ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
