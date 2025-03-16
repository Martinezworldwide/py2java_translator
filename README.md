# Python to Java Translator

A web application that translates Python code to Java, highlighting semantic differences between the two languages.

## Features

- Converts Python code to equivalent Java code
- Highlights semantic differences between Python and Java
- Supports basic Python constructs including:
  - Functions with type hints
  - Variables and assignments
  - Control flow (if/else)
  - Loops (for/while)
  - Lists and dictionaries
  - Basic operators

## Local Development

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
export FLASK_APP=src/web_app.py
export FLASK_ENV=development
flask run
```

The application will be available at http://localhost:5000

## Deployment

This application can be deployed to Render.com:

1. Create a new account on Render.com
2. Connect your GitHub repository
3. Create a new Web Service
4. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.web_app:app`
   - Python Version: 3.9
   - Plan: Free

## API Endpoints

- `GET /`: Main page with the translator interface
- `POST /translate`: Translates Python code to Java
  - Request body: `{"python_code": "your_python_code_here"}`
  - Response: `{"java_code": "translated_java_code", "semantic_differences": []}` 