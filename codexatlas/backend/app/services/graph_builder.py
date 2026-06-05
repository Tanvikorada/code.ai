import networkx as nx
from typing import List, Dict, Any, Optional
from app.models.node import Node, Edge
import uuid

class GraphBuilder:
    """Build knowledge graphs from parsed code"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def build_graph(self, files: List[Dict], repo_id: str) -> tuple[List[Node], List[Edge]]:
        """Build knowledge graph from parsed files"""
        nodes: List[Node] = []
        edges: List[Edge] = []
        
        # Create file nodes
        for file_data in files:
            if 'error' in file_data:
                continue
            
            file_path = file_data.get('path', '')
            language = file_data.get('language', 'unknown')
            
            # Create file node
            file_node = Node(
                id=str(uuid.uuid4()),
                repo_id=repo_id,
                node_type='file',
                name=file_path.split('/')[-1],
                path=file_path,
                complexity=file_data.get('complexity', 0)
            )
            nodes.append(file_node)
            
            # Create function nodes
            for func in file_data.get('functions', []):
                if isinstance(func, dict):
                    func_name = func.get('name', '')
                else:
                    func_name = func
                
                func_node = Node(
                    id=str(uuid.uuid4()),
                    repo_id=repo_id,
                    node_type='function',
                    name=func_name,
                    path=file_path,
                    complexity=1
                )
                nodes.append(func_node)
                
                # Create edge: file -> function
                edges.append(Edge(
                    id=str(uuid.uuid4()),
                    source=file_node.id,
                    target=func_node.id,
                    relationship='creates'
                ))
            
            # Create class nodes
            for cls in file_data.get('classes', []):
                if isinstance(cls, dict):
                    class_name = cls.get('name', '')
                    methods = cls.get('methods', [])
                else:
                    class_name = cls
                    methods = []
                
                class_node = Node(
                    id=str(uuid.uuid4()),
                    repo_id=repo_id,
                    node_type='class',
                    name=class_name,
                    path=file_path,
                    complexity=len(methods)
                )
                nodes.append(class_node)
                
                # Create edge: file -> class
                edges.append(Edge(
                    id=str(uuid.uuid4()),
                    source=file_node.id,
                    target=class_node.id,
                    relationship='creates'
                ))
                
                # Create method nodes
                for method in methods:
                    method_node = Node(
                        id=str(uuid.uuid4()),
                        repo_id=repo_id,
                        node_type='function',
                        name=f"{class_name}.{method}",
                        path=file_path,
                        complexity=1
                    )
                    nodes.append(method_node)
                    
                    edges.append(Edge(
                        id=str(uuid.uuid4()),
                        source=class_node.id,
                        target=method_node.id,
                        relationship='creates'
                    ))
            
            # Create component nodes for React/JSX
            for comp in file_data.get('components', []):
                comp_node = Node(
                    id=str(uuid.uuid4()),
                    repo_id=repo_id,
                    node_type='component',
                    name=comp,
                    path=file_path,
                    complexity=1
                )
                nodes.append(comp_node)
                
                edges.append(Edge(
                    id=str(uuid.uuid4()),
                    source=file_node.id,
                    target=comp_node.id,
                    relationship='creates'
                ))
        
        # Create import relationships
        for file_data in files:
            if 'error' in file_data:
                continue
            
            file_path = file_data.get('path', '')
            imports = file_data.get('imports', [])
            
            # Find the file node
            file_node = next((n for n in nodes if n.path == file_path and n.node_type == 'file'), None)
            if not file_node:
                continue
            
            # Find imported files/components
            for imp in imports:
                # Try to find matching node
                target_nodes = []
                
                # Look for file with matching name
                for node in nodes:
                    if node.node_type in ['file', 'component', 'class']:
                        if imp in node.name or node.name in imp:
                            target_nodes.append(node)
                
                for target in target_nodes:
                    if target.id != file_node.id:
                        edges.append(Edge(
                            id=str(uuid.uuid4()),
                            source=file_node.id,
                            target=target.id,
                            relationship='imports'
                        ))
        
        return nodes, edges
    
    def analyze_dependencies(self, nodes: List[Node], edges: List[Edge]) -> Dict[str, Any]:
        """Analyze dependency patterns"""
        dependency_count = {}
        
        for edge in edges:
            if edge.relationship == 'imports':
                source = edge.source
                if source not in dependency_count:
                    dependency_count[source] = 0
                dependency_count[source] += 1
        
        # Find highly dependent nodes
        highly_dependent = sorted(dependency_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total_dependencies': len(edges),
            'highly_dependent': highly_dependent,
            'average_dependencies': sum(dependency_count.values()) / len(dependency_count) if dependency_count else 0
        }
