from typing import List, Dict, Any, Set
from app.models.node import Node, Edge
import networkx as nx

class DependencyAnalyzer:
    """Analyze code dependencies and relationships"""
    
    def __init__(self):
        pass
    
    def find_circular_dependencies(self, nodes: List[Node], edges: List[Edge]) -> List[List[str]]:
        """Detect circular dependencies in the graph"""
        graph = nx.DiGraph()
        
        for edge in edges:
            graph.add_edge(edge.source, edge.target)
        
        cycles = list(nx.simple_cycles(graph))
        return cycles
    
    def find_unused_files(self, nodes: List[Node], edges: List[Edge]) -> List[str]:
        """Find files that are not imported by any other file"""
        imported_files = set()
        file_nodes = {node.id: node for node in nodes if node.node_type == 'file'}
        
        for edge in edges:
            if edge.relationship == 'imports' and edge.target in file_nodes:
                imported_files.add(edge.target)
        
        unused = [
            file_nodes[node_id].path 
            for node_id in file_nodes 
            if node_id not in imported_files
        ]
        
        return unused
    
    def find_dead_code(self, nodes: List[Node], edges: List[Edge]) -> Dict[str, List[str]]:
        """Find potentially dead code (unused functions, classes, components)"""
        called_functions = set()
        function_nodes = {node.id: node for node in nodes if node.node_type == 'function'}
        
        for edge in edges:
            if edge.relationship == 'calls' and edge.target in function_nodes:
                called_functions.add(edge.target)
        
        unused_functions = [
            function_nodes[node_id].name 
            for node_id in function_nodes 
            if node_id not in called_functions
        ]
        
        return {
            'unused_functions': unused_functions
        }
    
    def calculate_coupling(self, nodes: List[Node], edges: List[Edge]) -> Dict[str, float]:
        """Calculate coupling metrics"""
        file_nodes = [node for node in nodes if node.node_type == 'file']
        file_ids = {node.id for node in file_nodes}
        
        # Count dependencies between files
        file_dependencies = {}
        for edge in edges:
            if edge.source in file_ids and edge.target in file_ids:
                if edge.source not in file_dependencies:
                    file_dependencies[edge.source] = 0
                file_dependencies[edge.source] += 1
        
        avg_coupling = (
            sum(file_dependencies.values()) / len(file_dependencies) 
            if file_dependencies else 0
        )
        
        return {
            'average_coupling': avg_coupling,
            'max_coupling': max(file_dependencies.values()) if file_dependencies else 0
        }
    
    def analyze_impact(self, node_id: str, nodes: List[Node], edges: List[Edge]) -> Dict[str, Any]:
        """Analyze the impact of changing a specific node"""
        graph = nx.DiGraph()
        
        for edge in edges:
            graph.add_edge(edge.source, edge.target)
        
        # Find all downstream dependencies
        try:
            descendants = nx.descendants(graph, node_id)
        except:
            descendants = set()
        
        # Find all upstream dependents
        try:
            ancestors = nx.ancestors(graph, node_id)
        except:
            ancestors = set()
        
        return {
            'affected_downstream': list(descendants),
            'affected_upstream': list(ancestors),
            'total_impact': len(descendants) + len(ancestors)
        }
