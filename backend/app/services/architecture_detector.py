from typing import List, Dict, Any
from app.models.node import Node

class ArchitectureDetector:
    """Detect architectural layers based on file paths and types."""
    
    def detect_layers(self, nodes: List[Node]) -> Dict[str, Any]:
        """Categorize nodes into logical architecture layers."""
        
        layers_dict = {
            "Frontend Layer": {
                "components": set(),
                "color": "from-accent-primary to-accent-secondary",
                "keywords": ["src/components", "src/pages", "src/views", "frontend", "client", ".tsx", ".jsx", "app.tsx", "index.tsx"]
            },
            "Backend API Layer": {
                "components": set(),
                "color": "from-accent-secondary to-accent-tertiary",
                "keywords": ["api/", "routes/", "controllers/", "endpoints", "router.py", "main.py"]
            },
            "Business Logic / Services": {
                "components": set(),
                "color": "from-blue-500 to-purple-500",
                "keywords": ["services/", "logic/", "core/", "utils/", "helpers/"]
            },
            "Database Layer": {
                "components": set(),
                "color": "from-accent-tertiary to-green-500",
                "keywords": ["models/", "database/", "schema", "migrations", "db/", "repository", "store"]
            },
            "Infrastructure / Config": {
                "components": set(),
                "color": "from-green-500 to-blue-500",
                "keywords": ["docker", "config", "setup", "settings", "package.json", "requirements.txt", "vite.config", "tsconfig"]
            }
        }
        
        # Categorize nodes
        for node in nodes:
            if node.node_type == 'file':
                path_lower = node.path.lower()
                assigned = False
                
                for layer_name, layer_data in layers_dict.items():
                    if any(keyword in path_lower for keyword in layer_data["keywords"]):
                        layer_data["components"].add(node.name)
                        assigned = True
                        break
                
                # Default bucket
                if not assigned:
                    if "Other" not in layers_dict:
                        layers_dict["Other"] = {
                            "components": set(),
                            "color": "from-gray-500 to-gray-700",
                            "keywords": []
                        }
                    layers_dict["Other"]["components"].add(node.name)

        # Format output
        formatted_layers = []
        for name, data in layers_dict.items():
            if data["components"]:
                # Limit components to top 10 to avoid huge lists
                comp_list = list(data["components"])[:10]
                if len(data["components"]) > 10:
                    comp_list.append(f"... and {len(data['components']) - 10} more")
                
                formatted_layers.append({
                    "name": name,
                    "components": comp_list,
                    "color": data["color"]
                })
        
        # Ensure there is at least one layer to prevent frontend crashes
        if not formatted_layers:
             formatted_layers.append({
                    "name": "General Project",
                    "components": ["Source Files"],
                    "color": "from-gray-500 to-gray-700"
                })

        metrics = {
            "layer_count": len(formatted_layers),
            "component_count": sum(len(layer["components"]) for layer in formatted_layers),
            "modularity_score": min(1.0, len(formatted_layers) * 0.2), # Rough heuristic
            "architecture_grade": "A" if len(formatted_layers) >= 3 else ("B" if len(formatted_layers) == 2 else "C")
        }
        
        return {
            "layers": formatted_layers,
            "metrics": metrics
        }
