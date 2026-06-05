import { create } from 'zustand'

export interface Node {
  id: string
  type: 'file' | 'component' | 'function' | 'api' | 'database' | 'service' | 'hook' | 'class'
  name: string
  path?: string
  complexity?: number
  x?: number
  y?: number
}

export interface Edge {
  id: string
  source: string
  target: string
  relationship: 'imports' | 'calls' | 'returns' | 'creates' | 'updates' | 'reads' | 'writes' | 'depends_on'
}

export interface Repository {
  id: string
  name: string
  url: string
  framework: string
  language: string
  createdAt?: string
  health?: any
}

interface AppState {
  currentRepository: Repository | null
  nodes: Node[]
  edges: Edge[]
  selectedNode: Node | null
  isLoading: boolean
  setRepository: (repo: Repository | null) => void
  setNodes: (nodes: Node[]) => void
  setEdges: (edges: Edge[]) => void
  setSelectedNode: (node: Node | null) => void
  setLoading: (loading: boolean) => void
  clearData: () => void
}

export const useStore = create<AppState>((set) => ({
  currentRepository: null,
  nodes: [],
  edges: [],
  selectedNode: null,
  isLoading: false,
  setRepository: (repo) => set({ currentRepository: repo }),
  setNodes: (nodes) => set({ nodes }),
  setEdges: (edges) => set({ edges }),
  setSelectedNode: (node) => set({ selectedNode: node }),
  setLoading: (loading) => set({ isLoading: loading }),
  clearData: () => set({ currentRepository: null, nodes: [], edges: [], selectedNode: null }),
}))
