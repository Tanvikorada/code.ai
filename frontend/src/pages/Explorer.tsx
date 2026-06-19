// @ts-nocheck
import { useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  NodeTypes,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { useStore } from '../store/useStore'
import { apiService } from '../lib/api'
import { ArrowLeft } from 'lucide-react'

// Custom node component
const CustomNode = ({ data }: { data: any }) => {
  const getNodeColor = (type: string) => {
    const colors: Record<string, string> = {
      file: 'rgba(0, 240, 255, 0.2)', // aurora-cyan
      component: 'rgba(138, 43, 226, 0.2)', // aurora-purple
      function: 'rgba(255, 255, 255, 0.1)',
      api: 'rgba(0, 240, 255, 0.2)',
      database: 'rgba(138, 43, 226, 0.2)',
    }
    return colors[type] || 'rgba(255, 255, 255, 0.05)'
  }

  const getBorderColor = (type: string) => {
    const colors: Record<string, string> = {
      file: 'rgba(0, 240, 255, 0.5)',
      component: 'rgba(138, 43, 226, 0.5)',
      function: 'rgba(255, 255, 255, 0.2)',
      api: 'rgba(0, 240, 255, 0.5)',
      database: 'rgba(138, 43, 226, 0.5)',
    }
    return colors[type] || 'rgba(255, 255, 255, 0.1)'
  }

  return (
    <div
      className="px-5 py-3 rounded-2xl border backdrop-blur-md min-w-[160px] shadow-2xl transition-all hover:scale-105"
      style={{
        backgroundColor: getNodeColor(data.type),
        borderColor: getBorderColor(data.type),
        boxShadow: `0 8px 32px 0 ${getNodeColor(data.type)}`,
      }}
    >
      <div className="font-semibold text-white tracking-tight">{data.label}</div>
      {data.path && <div className="text-xs text-white/50 mt-1 font-medium truncate max-w-[200px]">{data.path}</div>}
    </div>
  )
}

const nodeTypes: NodeTypes = {
  custom: CustomNode,
}

const Explorer = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { setNodes, setEdges, isLoading } = useStore()
  const [nodes, setNodesState, onNodesChange] = useNodesState([])
  const [edges, setEdgesState, onEdgesChange] = useEdgesState([])

  useEffect(() => {
    if (id) {
      loadGraphData(id)
    }
  }, [id])

  const loadGraphData = async (repoId: string) => {
    try {
      const data = await apiService.getGraph(repoId)
      const flowNodes: Node[] = data.nodes.map((node: any) => ({
        id: node.id,
        type: 'custom',
        position: { x: Math.random() * 800, y: Math.random() * 600 },
        data: {
          label: node.name,
          type: node.type,
          path: node.path,
        },
      }))
      const flowEdges: Edge[] = data.edges.map((edge: any) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        type: 'smoothstep',
        animated: true,
        style: { stroke: 'rgba(255, 255, 255, 0.15)', strokeWidth: 2 },
      }))

      setNodesState(flowNodes)
      setEdgesState(flowEdges)
      setNodes(data.nodes)
      setEdges(data.edges)
    } catch (error) {
      console.error('Failed to load graph:', error)
    }
  }

  const onConnect = useCallback(
    (params: Connection) => setEdgesState((eds: Edge[]) => addEdge(params, eds)),
    [setEdgesState]
  )

  if (isLoading) {
    return (
      <div className="min-h-screen bg-obsidian flex items-center justify-center font-sans">
        <div className="text-center relative">
          <div className="absolute inset-0 bg-aurora-cyan/20 blur-[100px] rounded-full" />
          <div className="w-16 h-16 border-2 border-aurora-cyan border-t-transparent rounded-full animate-spin mx-auto mb-6 relative z-10" />
          <h2 className="text-2xl font-bold mb-2 relative z-10 tracking-tight">Mapping Dependencies</h2>
          <p className="text-white/50 font-medium relative z-10">Initializing graph renderer...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-obsidian flex flex-col font-sans relative">
      {/* Background ambient glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-[600px] bg-aurora-purple/5 blur-[150px] pointer-events-none rounded-full mix-blend-screen" />

      {/* Header */}
      <header className="glass-panel z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate(`/repository/${id}`)}
              className="flex items-center gap-2 text-white/50 hover:text-white transition-colors font-medium text-sm"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Repository
            </button>
            <div className="flex items-center gap-4">
              <h1 className="text-xl font-bold tracking-tight text-white hidden md:block">Dependency Explorer</h1>
              <button
                onClick={() => navigate(`/architecture/${id}`)}
                className="bg-white text-obsidian px-5 py-2.5 rounded-xl transition-colors text-sm font-semibold hover:bg-white/90 shadow-[0_0_15px_rgba(255,255,255,0.2)]"
              >
                Architecture View
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 relative">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
          className="bg-transparent"
        >
          <Background color="rgba(255, 255, 255, 0.05)" gap={24} size={2} />
          <Controls
            className="glass-card !border-white/10 !bg-obsidian/80 !fill-white"
            showZoom={true}
            showFitView={true}
            showInteractive={false}
          />
        </ReactFlow>

        {/* Legend */}
        <div className="absolute bottom-6 left-6 glass-card rounded-2xl p-6 pointer-events-none">
          <h3 className="font-bold mb-4 text-sm tracking-tight">Node Types</h3>
          <div className="space-y-3 text-sm font-medium text-white/70">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-aurora-cyan shadow-[0_0_10px_rgba(0,240,255,0.8)]" />
              <span>File / API</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-aurora-purple shadow-[0_0_10px_rgba(138,43,226,0.8)]" />
              <span>Component / DB</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-white/50" />
              <span>Function</span>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="absolute top-6 left-6 glass-card rounded-2xl p-5 pointer-events-none">
          <div className="flex items-center gap-6">
            <div>
              <div className="text-white/40 text-xs font-semibold uppercase tracking-wider mb-1">Nodes</div>
              <div className="text-2xl font-bold">{nodes.length}</div>
            </div>
            <div className="w-px h-10 bg-white/10" />
            <div>
              <div className="text-white/40 text-xs font-semibold uppercase tracking-wider mb-1">Edges</div>
              <div className="text-2xl font-bold">{edges.length}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Explorer
