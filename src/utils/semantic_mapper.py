from typing import Dict, List, Optional, Tuple

class SemanticMapper:
    """
    Maps Python language constructs to their Java equivalents and
    provides explanations of semantic differences.
    """
    
    @staticmethod
    def get_type_mapping() -> Dict[str, str]:
        """
        Returns a mapping of Python types to Java types.
        
        Returns:
            Dictionary mapping Python type names to Java type names
        """
        return {
            'int': 'int',
            'float': 'double',
            'str': 'String',
            'bool': 'boolean',
            'list': 'ArrayList',
            'dict': 'HashMap',
            'set': 'HashSet',
            'tuple': 'List',
            'None': 'void',
            'Any': 'Object',
        }
    
    @staticmethod
    def get_builtin_method_mapping() -> Dict[str, Tuple[str, str]]:
        """
        Returns a mapping of Python builtin methods to Java equivalents.
        
        Returns:
            Dictionary mapping Python method names to (Java method, Required import)
        """
        return {
            'len': ('size()', None),
            'print': ('System.out.println', None),
            'str': ('String.valueOf', None),
            'int': ('Integer.parseInt', None),
            'float': ('Double.parseDouble', None),
            'list': ('new ArrayList', 'java.util.ArrayList'),
            'dict': ('new HashMap', 'java.util.HashMap'),
            'set': ('new HashSet', 'java.util.HashSet'),
            'sum': ('stream().mapToInt(Integer::intValue).sum()', 'java.util.stream.Collectors'),
            'max': ('Collections.max', 'java.util.Collections'),
            'min': ('Collections.min', 'java.util.Collections'),
            'sorted': ('stream().sorted().collect(Collectors.toList())', 'java.util.stream.Collectors'),
        }
    
    @staticmethod
    def get_semantic_differences() -> List[Dict[str, str]]:
        """
        Returns a list of key semantic differences between Python and Java.
        
        Returns:
            List of dictionaries containing feature differences
        """
        return [
            {
                "feature": "Type System",
                "python": "Dynamic typing with type hints",
                "java": "Static typing with explicit type declarations",
                "example_python": "x = 42  # x can be reassigned to any type",
                "example_java": "int x = 42;  // x must remain an integer"
            },
            {
                "feature": "Inheritance",
                "python": "Multiple inheritance through class hierarchies",
                "java": "Single inheritance with multiple interface implementation",
                "example_python": "class Child(Parent1, Parent2): pass",
                "example_java": "class Child extends Parent1 implements Interface2"
            },
            {
                "feature": "Memory Management",
                "python": "Automatic garbage collection with reference counting",
                "java": "Automatic garbage collection with mark-and-sweep",
                "example_python": "# Objects automatically cleaned up",
                "example_java": "// Objects cleaned up by JVM garbage collector"
            },
            {
                "feature": "Exception Handling",
                "python": "Unified exception hierarchy, optional exception specification",
                "java": "Checked vs unchecked exceptions, mandatory exception declaration",
                "example_python": "def func(): raise ValueError()",
                "example_java": "void func() throws Exception { throw new IllegalArgumentException(); }"
            },
            {
                "feature": "Package Management",
                "python": "Module-based with import statements",
                "java": "Package-based with fully qualified names",
                "example_python": "from module import Class",
                "example_java": "import com.package.Class;"
            }
        ]
    
    @staticmethod
    def get_collection_operations() -> Dict[str, Dict[str, str]]:
        """
        Returns mappings for common collection operations between Python and Java.
        
        Returns:
            Dictionary mapping Python operations to Java equivalents
        """
        return {
            "list": {
                "append": "add",
                "extend": "addAll",
                "insert": "add",
                "remove": "remove",
                "pop": "remove",
                "clear": "clear",
                "index": "indexOf",
                "count": "frequency",  # Requires Collections.frequency
                "sort": "sort",
                "reverse": "Collections.reverse",  # Requires Collections
            },
            "dict": {
                "get": "get",
                "keys": "keySet",
                "values": "values",
                "items": "entrySet",
                "clear": "clear",
                "pop": "remove",
                "update": "putAll",
            },
            "set": {
                "add": "add",
                "remove": "remove",
                "clear": "clear",
                "union": "addAll",
                "intersection": "retainAll",
                "difference": "removeAll",
            }
        } 