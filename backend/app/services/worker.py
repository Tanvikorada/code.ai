from app.services import RepositoryScanner, ASTEngine, GraphBuilder, DependencyAnalyzer, ArchitectureDetector
from app.models.orm import ScanResult
from sqlalchemy.orm import Session
from app.database import SessionLocal

def process_repository(repo_id: str, url: str):
    db: Session = SessionLocal()
    scan_result = db.query(ScanResult).filter(ScanResult.id == repo_id).first()
    if not scan_result:
        db.close()
        return

    scanner = RepositoryScanner()
    ast_engine = ASTEngine()
    graph_builder = GraphBuilder()
    dependency_analyzer = DependencyAnalyzer()
    architecture_detector = ArchitectureDetector()

    try:
        # 1. Clone repository
        repo_path = scanner.clone_repository(url)
        
        # 2. Detect basic info
        language = scanner.detect_language(repo_path)
        framework = scanner.detect_framework(repo_path, language)
        
        # 3. Get file structure and parse AST
        raw_files = scanner.get_file_structure(repo_path)
        parsed_files = []
        for file_info in raw_files:
            parsed = ast_engine.parse_file(file_info['absolute_path'], file_info['language'])
            file_info.update(parsed)
            parsed_files.append(file_info)
            
        # 4. Build Graph
        nodes, edges = graph_builder.build_graph(parsed_files, repo_id)
        
        # 5. Analyze Health
        circular_deps = dependency_analyzer.find_circular_dependencies(nodes, edges)
        unused_files = dependency_analyzer.find_unused_files(nodes, edges)
        dead_code = dependency_analyzer.find_dead_code(nodes, edges)
        coupling = dependency_analyzer.calculate_coupling(nodes, edges)
        
        issues = []
        if circular_deps:
            issues.append({"severity": "high", "message": f"Found {len(circular_deps)} circular dependencies"})
        if unused_files:
            issues.append({"severity": "medium", "message": f"Found {len(unused_files)} unused files"})
        if dead_code.get("unused_functions"):
            issues.append({"severity": "low", "message": f"Found {len(dead_code['unused_functions'])} unused functions"})
            
        health_score = max(0, 100 - (len(circular_deps) * 10) - (len(unused_files) * 2) - (len(dead_code.get("unused_functions", []))))
        
        # 6. Detect Architecture
        architecture_data = architecture_detector.detect_layers(nodes)
        
        # 7. Update DB
        scan_result.data = {
            "graph": {
                "nodes": [n.dict() for n in nodes],
                "edges": [e.dict() for e in edges]
            },
            "architecture": architecture_data,
            "health": {
                "overall_score": health_score,
                "maintainability": max(0, 100 - len(unused_files) * 2),
                "scalability": max(0, 100 - int(coupling.get('average_coupling', 0) * 5)),
                "complexity": int(min(100, sum(n.complexity for n in nodes if hasattr(n, 'complexity')) / max(1, len(nodes)) * 10)),
                "coupling": int(min(100, coupling.get('max_coupling', 0) * 10)),
                "documentation": 80,
                "issues": issues if issues else [{"severity": "low", "message": "No major issues found. Good job!"}]
            },
            "metadata": {
                "name": url.split('/')[-1].replace('.git', ''),
                "url": url,
                "framework": framework,
                "language": language
            }
        }
        scan_result.status = "completed"
        db.commit()
        
    except Exception as e:
        scan_result.status = "failed"
        scan_result.data = {"error": str(e)}
        db.commit()
    finally:
        # 8. Cleanup
        try:
            scanner.cleanup(repo_path)
        except:
            pass
        db.close()
