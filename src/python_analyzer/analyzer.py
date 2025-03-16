import ast
from typing import Any, Dict, List, Optional, Set

class PythonAnalyzer:
    """
    Analyzes Python code and creates an intermediate representation
    that can be used to generate Java code.
    """
    
    def __init__(self):
        self.semantic_differences: List[Dict[str, str]] = []
        self._seen_features: Set[str] = set()
        
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
            self.semantic_differences = []  # Reset differences for new analysis
            self._seen_features = set()    # Reset seen features
            self._analyze_semantic_differences(tree)
            return tree
        except SyntaxError as e:
            raise ValueError(f"Invalid Python code: {str(e)}")
            
    def _add_difference(self, feature: str, python: str, java: str) -> None:
        """Add a semantic difference if not already seen."""
        if feature not in self._seen_features:
            self.semantic_differences.append({
                "feature": feature,
                "python": python,
                "java": java
            })
            self._seen_features.add(feature)
            
    def _analyze_semantic_differences(self, tree: ast.AST) -> None:
        """
        Analyzes the AST for semantic differences between Python and Java.
        
        Args:
            tree: The AST to analyze
        """
        for node in ast.walk(tree):
            # Type System Differences
            if isinstance(node, ast.AnnAssign):
                self._add_difference(
                    "Type Annotations",
                    "Optional type hints that don't affect runtime behavior",
                    "Mandatory static type declarations"
                )
            
            # Data Structures
            elif isinstance(node, ast.List):
                self._add_difference(
                    "List Implementation",
                    "Dynamic, resizable lists with mixed types",
                    "ArrayList<T> with fixed type or arrays with fixed size"
                )
            elif isinstance(node, ast.Dict):
                self._add_difference(
                    "Dictionary/Map Implementation",
                    "Dynamic dict with any hashable type as key",
                    "HashMap<K,V> with specific type parameters"
                )
            elif isinstance(node, ast.Set):
                self._add_difference(
                    "Set Implementation",
                    "Built-in set type with dynamic sizing",
                    "HashSet<T> with specific type parameter"
                )
            elif isinstance(node, ast.Tuple):
                self._add_difference(
                    "Tuple Implementation",
                    "Immutable tuple type with mixed types",
                    "No direct equivalent; requires custom class or array"
                )
                
            # Control Flow
            elif isinstance(node, ast.For):
                self._add_difference(
                    "For Loop Syntax",
                    "for item in iterable syntax",
                    "for(Type item : iterable) or traditional for loop"
                )
            elif isinstance(node, ast.With):
                self._add_difference(
                    "Resource Management",
                    "with statement for context management",
                    "try-with-resources statement"
                )
                
            # Functional Features
            elif isinstance(node, ast.ListComp):
                self._add_difference(
                    "List Comprehension",
                    "Concise list comprehension syntax",
                    "Stream API or explicit loops"
                )
            elif isinstance(node, ast.Lambda):
                self._add_difference(
                    "Lambda Functions",
                    "Simple lambda expressions",
                    "Lambda expressions with functional interfaces"
                )
            elif isinstance(node, ast.comprehension):
                self._add_difference(
                    "Comprehensions",
                    "List, set, and dictionary comprehensions",
                    "Stream API with map, filter, and collect"
                )
                
            # Exception Handling
            elif isinstance(node, ast.Try):
                self._add_difference(
                    "Exception Handling",
                    "try/except blocks with optional type checking",
                    "try/catch blocks with mandatory exception types"
                )
            elif isinstance(node, ast.Raise):
                self._add_difference(
                    "Exception Throwing",
                    "raise statement with any exception type",
                    "throw statement with Exception class hierarchy"
                )
                
            # OOP Features
            elif isinstance(node, ast.ClassDef):
                self._analyze_class_differences(node)
                
            # Function Features
            elif isinstance(node, ast.FunctionDef):
                self._analyze_function_differences(node)
                
    def _analyze_class_differences(self, node: ast.ClassDef) -> None:
        """Analyze class-specific differences."""
        # Check for multiple inheritance
        if len(node.bases) > 1:
            self._add_difference(
                "Multiple Inheritance",
                "Supports multiple inheritance directly",
                "Only supports single inheritance with interfaces"
            )
            
        # Check for special methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if item.name.startswith('__') and item.name.endswith('__'):
                    self._add_difference(
                        "Special Methods",
                        "Magic methods for operator overloading and behavior customization",
                        "Limited operator overloading through specific method names"
                    )
                    break
                    
    def _analyze_function_differences(self, node: ast.FunctionDef) -> None:
        """Analyze function-specific differences."""
        # Check for default arguments
        if any(isinstance(d, ast.AST) for d in node.args.defaults):
            self._add_difference(
                "Default Arguments",
                "Supports default argument values",
                "Requires method overloading for default values"
            )
            
        # Check for *args and **kwargs
        if node.args.vararg or node.args.kwarg:
            self._add_difference(
                "Variable Arguments",
                "*args and **kwargs for variable arguments",
                "varargs and no direct equivalent for kwargs"
            )
            
        # Check for type annotations
        if node.returns or any(a.annotation for a in node.args.args):
            self._add_difference(
                "Function Type Hints",
                "Optional type hints with -> return annotation",
                "Mandatory return and parameter types"
            )
                
    def get_semantic_differences(self) -> List[Dict[str, str]]:
        """
        Returns the list of semantic differences found during analysis.
        
        Returns:
            List of dictionaries containing semantic differences
        """
        return self.semantic_differences 