import ast
from typing import Any, Dict, List, Optional

class PythonAnalyzer:
    """
    Analyzes Python code and creates an intermediate representation
    that can be used to generate Java code.
    """
    
    def __init__(self):
        self.semantic_differences: List[Dict[str, str]] = []
        
    def analyze(self, python_code: str) -> ast.AST:
        """
        Analyzes Python code and returns its AST representation.
        
        Args:
            python_code: String containing Python source code
            
        Returns:
            The AST representation of the code
        """
        try:
            tree = ast.parse(python_code)
            self._analyze_semantic_differences(tree)
            return tree
        except SyntaxError as e:
            raise ValueError(f"Invalid Python code: {str(e)}")
            
    def _analyze_semantic_differences(self, tree: ast.AST) -> None:
        """
        Analyzes the AST for semantic differences between Python and Java.
        
        Args:
            tree: The AST to analyze
        """
        for node in ast.walk(tree):
            # Check for Python-specific features
            if isinstance(node, ast.List):
                self.semantic_differences.append({
                    "feature": "List Implementation",
                    "python": "Dynamic typing and resizable lists",
                    "java": "Static typing with ArrayList<T> or fixed-size arrays"
                })
            elif isinstance(node, ast.Dict):
                self.semantic_differences.append({
                    "feature": "Dictionary/Map Implementation",
                    "python": "Dynamic hash table with any hashable type as key",
                    "java": "HashMap<K,V> with specific type parameters"
                })
            elif isinstance(node, ast.With):
                self.semantic_differences.append({
                    "feature": "Resource Management",
                    "python": "with statement for context management",
                    "java": "try-with-resources statement"
                })
            elif isinstance(node, ast.ListComp):
                self.semantic_differences.append({
                    "feature": "List Comprehension",
                    "python": "Concise list comprehension syntax",
                    "java": "Stream API or explicit loops"
                })
            elif isinstance(node, ast.Lambda):
                self.semantic_differences.append({
                    "feature": "Lambda Functions",
                    "python": "Simple lambda expressions",
                    "java": "More verbose lambda syntax with functional interfaces"
                })
                
    def get_semantic_differences(self) -> List[Dict[str, str]]:
        """
        Returns the list of semantic differences found during analysis.
        
        Returns:
            List of dictionaries containing semantic differences
        """
        return self.semantic_differences 