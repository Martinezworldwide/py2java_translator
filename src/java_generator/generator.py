import ast
from typing import Dict, List, Optional, Set

class JavaGenerator:
    """
    Generates Java code from Python AST.
    """
    
    def __init__(self):
        self.indent_level = 0
        self.java_imports: Set[str] = set()
        self.type_map = {
            'int': 'int',
            'float': 'double',
            'str': 'String',
            'bool': 'boolean',
            'list': 'ArrayList',
            'dict': 'HashMap',
            'set': 'HashSet',
            'tuple': 'List',
        }
        
    def generate(self, tree: ast.AST, class_name: str = "PythonTranslated") -> str:
        """
        Generates Java code from a Python AST.
        
        Args:
            tree: The Python AST to convert
            class_name: Name of the Java class to generate
            
        Returns:
            String containing the equivalent Java code
        """
        self.java_imports.add("import java.util.*;")
        self.java_imports.add("import java.util.Arrays;")
        
        # Generate the Java class wrapper
        java_code = self._generate_imports()
        java_code += f"\npublic class {class_name} {{\n"
        self.indent_level += 1
        
        # Convert the Python AST to Java code
        for node in ast.iter_child_nodes(tree):
            java_code += self._generate_from_ast(node)
        
        self.indent_level -= 1
        java_code += "}\n"
        return java_code
        
    def _generate_imports(self) -> str:
        """
        Generates the import statements for the Java code.
        
        Returns:
            String containing all necessary import statements
        """
        return "\n".join(sorted(self.java_imports)) + "\n"
        
    def _generate_from_ast(self, node: ast.AST) -> str:
        """
        Recursively generates Java code from a Python AST node.
        
        Args:
            node: The AST node to convert
            
        Returns:
            String containing the equivalent Java code
        """
        if isinstance(node, ast.FunctionDef):
            return self._generate_function(node)
        elif isinstance(node, ast.ClassDef):
            return self._generate_class(node)
        elif isinstance(node, ast.Assign):
            return self._generate_assignment(node)
        elif isinstance(node, ast.If):
            return self._generate_if_statement(node)
        elif isinstance(node, ast.For):
            return self._generate_for_loop(node)
        elif isinstance(node, ast.While):
            return self._generate_while_loop(node)
        return ""
        
    def _generate_function(self, node: ast.FunctionDef) -> str:
        """
        Converts a Python function to Java method.
        
        Args:
            node: The function definition node
            
        Returns:
            String containing the Java method
        """
        # Extract return type annotation if available
        return_type = "void"
        if node.returns:
            if isinstance(node.returns, ast.Name):
                return_type = self.type_map.get(node.returns.id, "Object")
        
        # Build method signature
        params = []
        for arg in node.args.args:
            arg_type = "Object"  # Default type
            if arg.annotation and isinstance(arg.annotation, ast.Name):
                arg_type = self.type_map.get(arg.annotation.id, "Object")
            params.append(f"{arg_type} {arg.arg}")
        
        java_code = f"{self._indent()}public {return_type} {node.name}({', '.join(params)}) {{\n"
        self.indent_level += 1
        
        # Convert function body
        for stmt in node.body:
            java_code += self._generate_from_ast(stmt)
        
        self.indent_level -= 1
        java_code += f"{self._indent()}}}\n"
        return java_code
        
    def _generate_if_statement(self, node: ast.If) -> str:
        """
        Converts a Python if statement to Java if statement.
        
        Args:
            node: The if statement node
            
        Returns:
            String containing the Java if statement
        """
        java_code = f"{self._indent()}if ({self._generate_expression(node.test)}) {{\n"
        self.indent_level += 1
        
        for stmt in node.body:
            java_code += self._generate_from_ast(stmt)
        
        self.indent_level -= 1
        
        if node.orelse:
            java_code += f"{self._indent()}" + "} else {\n"
            self.indent_level += 1
            for stmt in node.orelse:
                java_code += self._generate_from_ast(stmt)
            self.indent_level -= 1
        
        java_code += f"{self._indent()}}}\n"
        return java_code
        
    def _generate_expression(self, node: ast.AST) -> str:
        """
        Converts a Python expression to Java expression.
        
        Args:
            node: The expression node
            
        Returns:
            String containing the Java expression
        """
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Num):
            return str(node.n)
        elif isinstance(node, ast.Str):
            return f'"{node.s}"'
        elif isinstance(node, ast.List):
            elements = [self._generate_expression(elt) for elt in node.elts]
            self.java_imports.add("import java.util.ArrayList;")
            return f"new ArrayList<>(Arrays.asList({', '.join(elements)}))"
        elif isinstance(node, ast.Dict):
            self.java_imports.add("import java.util.HashMap;")
            java_code = "new HashMap<>() {{\n"
            for key, value in zip(node.keys, node.values):
                java_code += f"{self._indent()}    put({self._generate_expression(key)}, {self._generate_expression(value)});\n"
            java_code += f"{self._indent()}}}"
            return java_code
        elif isinstance(node, ast.Compare):
            # Handle comparison operators
            ops = {
                ast.Eq: "==",
                ast.NotEq: "!=",
                ast.Lt: "<",
                ast.LtE: "<=",
                ast.Gt: ">",
                ast.GtE: ">=",
            }
            op = ops.get(type(node.ops[0]), "==")
            return f"{self._generate_expression(node.left)} {op} {self._generate_expression(node.comparators[0])}"
        elif isinstance(node, ast.BinOp):
            # Handle binary operators
            ops = {
                ast.Add: "+",
                ast.Sub: "-",
                ast.Mult: "*",
                ast.Div: "/",
                ast.Mod: "%",
            }
            op = ops.get(type(node.op), "+")
            return f"{self._generate_expression(node.left)} {op} {self._generate_expression(node.right)}"
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            elif isinstance(node.value, bool):
                return str(node.value).lower()
            return str(node.value)
        return "null"
        
    def _generate_assignment(self, node: ast.Assign) -> str:
        """
        Converts a Python assignment statement to Java.
        
        Args:
            node: The assignment node
            
        Returns:
            String containing the Java assignment
        """
        java_code = ""
        for target in node.targets:
            if isinstance(target, ast.Name):
                # Try to infer type from the value
                value_type = "Object"
                if isinstance(node.value, ast.Num):
                    if isinstance(node.value.n, int):
                        value_type = "int"
                    else:
                        value_type = "double"
                elif isinstance(node.value, ast.Str):
                    value_type = "String"
                elif isinstance(node.value, ast.List):
                    value_type = "ArrayList<Object>"
                    self.java_imports.add("import java.util.ArrayList;")
                elif isinstance(node.value, ast.Dict):
                    value_type = "HashMap<Object, Object>"
                    self.java_imports.add("import java.util.HashMap;")
                
                java_code += f"{self._indent()}{value_type} {target.id} = {self._generate_expression(node.value)};\n"
        return java_code
        
    def _indent(self) -> str:
        """
        Returns the current indentation string.
        
        Returns:
            String with appropriate number of spaces
        """
        return "    " * self.indent_level 

    def _generate_for_loop(self, node: ast.For) -> str:
        """
        Converts a Python for loop to Java for-each loop.
        
        Args:
            node: The for loop node
            
        Returns:
            String containing the Java for loop
        """
        # Handle for-each loop
        if isinstance(node.target, ast.Name):
            # Try to infer the type of the iterator elements
            iter_type = "Object"
            if isinstance(node.iter, ast.Name):
                # If iterating over a known variable, try to use its type
                if node.iter.id in self.type_map:
                    iter_type = self.type_map[node.iter.id]
            
            java_code = f"{self._indent()}for ({iter_type} {node.target.id} : {self._generate_expression(node.iter)}) {{\n"
            self.indent_level += 1
            
            for stmt in node.body:
                java_code += self._generate_from_ast(stmt)
            
            self.indent_level -= 1
            java_code += f"{self._indent()}}}\n"
            return java_code
        return ""

    def _generate_while_loop(self, node: ast.While) -> str:
        """
        Converts a Python while loop to Java while loop.
        
        Args:
            node: The while loop node
            
        Returns:
            String containing the Java while loop
        """
        java_code = f"{self._indent()}while ({self._generate_expression(node.test)}) {{\n"
        self.indent_level += 1
        
        for stmt in node.body:
            java_code += self._generate_from_ast(stmt)
        
        self.indent_level -= 1
        java_code += f"{self._indent()}}}\n"
        return java_code

    def _generate_class(self, node: ast.ClassDef) -> str:
        """
        Converts a Python class to Java class.
        
        Args:
            node: The class definition node
            
        Returns:
            String containing the Java class
        """
        # Handle inheritance
        extends = []
        implements = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                extends.append(base.id)
        
        # Build class declaration
        java_code = f"{self._indent()}public class {node.name}"
        if extends:
            # In Java, we can only extend one class, so we'll use the first one
            java_code += f" extends {extends[0]}"
            # Any additional bases become interfaces
            if len(extends) > 1:
                implements.extend(extends[1:])
        if implements:
            java_code += f" implements {', '.join(implements)}"
        java_code += " {\n"
        
        self.indent_level += 1
        
        # Track instance variables for constructor
        instance_vars = {}
        
        # First pass: collect instance variables and methods
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                var_type = "Object"
                if isinstance(item.annotation, ast.Name):
                    var_type = self.type_map.get(item.annotation.id, "Object")
                instance_vars[item.target.id] = var_type
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        instance_vars[target.id] = "Object"  # Default type if not annotated
        
        # Generate constructor if __init__ is present
        init_method = None
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                init_method = item
                break
        
        if init_method:
            # Generate constructor
            params = []
            for arg in init_method.args.args[1:]:  # Skip 'self'
                arg_type = "Object"
                if arg.annotation and isinstance(arg.annotation, ast.Name):
                    arg_type = self.type_map.get(arg.annotation.id, "Object")
                params.append(f"{arg_type} {arg.arg}")
            
            java_code += f"{self._indent()}public {node.name}({', '.join(params)}) {{\n"
            self.indent_level += 1
            
            # Add constructor body
            for stmt in init_method.body:
                if isinstance(stmt, ast.Assign):
                    if isinstance(stmt.targets[0], ast.Attribute):
                        if isinstance(stmt.targets[0].value, ast.Name) and stmt.targets[0].value.id == "self":
                            # Convert self.attr = value to this.attr = value
                            attr_name = stmt.targets[0].attr
                            java_code += f"{self._indent()}this.{attr_name} = {self._generate_expression(stmt.value)};\n"
            
            self.indent_level -= 1
            java_code += f"{self._indent()}}}\n\n"
        
        # Generate other methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name != "__init__":
                # Handle special methods
                if item.name == "__str__":
                    item.name = "toString"
                elif item.name == "__eq__":
                    item.name = "equals"
                elif item.name == "__len__":
                    item.name = "size"
                
                java_code += self._generate_function(item)
        
        self.indent_level -= 1
        java_code += f"{self._indent()}}}\n"
        return java_code 