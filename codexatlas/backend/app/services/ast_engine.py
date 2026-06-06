import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import ast

class ASTEngine:
    """Parse and analyze code structure using AST"""
    
    def __init__(self):
        self.supported_languages = ['python', 'javascript', 'typescript', 'jsx', 'tsx']
        try:
            import tree_sitter_javascript as tsjavascript
            import tree_sitter_typescript as tstypescript
            from tree_sitter import Language, Parser
            
            self.JS_LANGUAGE = Language(tsjavascript.language())
            self.TS_LANGUAGE = Language(tstypescript.language_typescript())
            
            self.tree_sitter_ready = True
        except ImportError:
            self.tree_sitter_ready = False
            print("Tree-sitter languages not installed. Falling back to regex parser for JS/TS.")

    def parse_file(self, file_path: str, language: str) -> Dict[str, Any]:
        """Parse a single file and extract its structure"""
        if language == 'python':
            return self._parse_python(file_path)
        elif language in ['javascript', 'jsx']:
            return self._parse_tree_sitter(file_path, is_typescript=False)
        elif language in ['typescript', 'tsx']:
            return self._parse_tree_sitter(file_path, is_typescript=True)
        else:
            return self._parse_generic(file_path)

    def _parse_python(self, file_path: str) -> Dict[str, Any]:
        """Parse Python file using AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=file_path)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            return {
                'language': 'python',
                'functions': functions,
                'classes': classes,
                'components': [],
                'imports': list(set(imports)),
                'exports': [],
                'complexity': len(functions) + len(classes)
            }
        except Exception as e:
            return {'error': str(e), 'language': 'python'}

    def _parse_tree_sitter(self, file_path: str, is_typescript: bool) -> Dict[str, Any]:
        """Parse JavaScript/TypeScript using official Tree-Sitter AST"""
        if not self.tree_sitter_ready:
            return self._parse_javascript_regex_fallback(file_path)
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            from tree_sitter import Parser
            parser = Parser()
            parser.set_language(self.TS_LANGUAGE if is_typescript else self.JS_LANGUAGE)
            tree = parser.parse(bytes(content, "utf8"))
            
            functions = []
            classes = []
            imports = []
            exports = []
            components = []
            
            def traverse(node):
                if node.type in ['function_declaration', 'arrow_function', 'method_definition']:
                    name_node = node.child_by_field_name('name')
                    if name_node:
                        name = content[name_node.start_byte:name_node.end_byte]
                        functions.append(name)
                        if name and name[0].isupper():
                            components.append(name)
                elif node.type == 'class_declaration':
                    name_node = node.child_by_field_name('name')
                    if name_node:
                        name = content[name_node.start_byte:name_node.end_byte]
                        classes.append(name)
                        if name and name[0].isupper():
                            components.append(name)
                elif node.type == 'import_statement':
                    source_node = node.child_by_field_name('source')
                    if source_node:
                        source = content[source_node.start_byte:source_node.end_byte].strip('\'"')
                        imports.append(source)
                elif node.type == 'export_statement':
                    declaration = node.child_by_field_name('declaration')
                    if declaration and declaration.type in ['function_declaration', 'class_declaration']:
                        name_node = declaration.child_by_field_name('name')
                        if name_node:
                            exports.append(content[name_node.start_byte:name_node.end_byte])
                
                for child in node.children:
                    traverse(child)
            
            traverse(tree.root_node)
            
            return {
                'language': 'typescript' if is_typescript else 'javascript',
                'functions': functions,
                'classes': classes,
                'components': components,
                'imports': list(set(imports)),
                'exports': exports,
                'complexity': len(functions) + len(classes)
            }
        except Exception as e:
            return {'error': str(e), 'language': 'typescript' if is_typescript else 'javascript'}

    def _parse_javascript_regex_fallback(self, file_path: str) -> Dict[str, Any]:
        """Parse JavaScript/TypeScript file (basic regex-based fallback)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            functions = re.findall(r'(?:function\s+|const\s+|let\s+|var\s+)(\w+)\s*(?:=|:\s*function|:\s*async\s*function|\()', content)
            classes = re.findall(r'class\s+(\w+)', content)
            imports = re.findall(r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]', content)
            exports = re.findall(r'export\s+(?:default\s+)?(?:const|function|class|let|var)\s+(\w+)', content)
            
            components = []
            for cls in classes:
                if cls[0].isupper():
                    components.append(cls)
            
            return {
                'language': 'javascript' if file_path.endswith('.js') or file_path.endswith('.jsx') else 'typescript',
                'functions': functions,
                'classes': classes,
                'components': components,
                'imports': imports,
                'exports': exports,
                'complexity': len(functions) + len(classes)
            }
        except Exception as e:
            return {'error': str(e), 'language': 'javascript'}

    def _parse_generic(self, file_path: str) -> Dict[str, Any]:
        """Basic parsing for unsupported languages"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'language': 'unknown',
                'line_count': len(content.splitlines()),
                'size': len(content)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_complexity(self, functions: List, classes: List) -> int:
        """Calculate cyclomatic complexity estimate"""
        return len(functions) + len(classes) * 2
    
    def _get_decorator_name(self, decorator) -> str:
        """Extract decorator name"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            return self._get_name(decorator.func)
        return 'unknown'
    
    def _get_name(self, node) -> str:
        """Extract name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return 'unknown'
