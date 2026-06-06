import { create } from 'zustand'
import { persist } from 'zustand/middleware'

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
  customApiKey: string | null
  aiTrialCount: number
  setRepository: (repo: Repository | null) => void
  setNodes: (nodes: Node[]) => void
  setEdges: (edges: Edge[]) => void
  setSelectedNode: (node: Node | null) => void
  setLoading: (loading: boolean) => void
  setCustomApiKey: (key: string | null) => void
  incrementAiTrialCount: () => void
  clearData: () => void
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      currentRepository: null,
      nodes: [],
      edges: [],
      selectedNode: null,
      isLoading: false,
      customApiKey: null,
      aiTrialCount: 0,
      setRepository: (repo) => set({ currentRepository: repo }),
      setNodes: (nodes) => set({ nodes }),
      setEdges: (edges) => set({ edges }),
      setSelectedNode: (node) => set({ selectedNode: node }),
      setLoading: (loading) => set({ isLoading: loading }),
      setCustomApiKey: (key) => set({ customApiKey: key }),
      incrementAiTrialCount: () => set((state) => ({ aiTrialCount: state.aiTrialCount + 1 })),
      clearData: () => set({ currentRepository: null, nodes: [], edges: [], selectedNode: null }),
    }),
    {
      name: 'codexatlas-storage',
      partialize: (state) => ({ customApiKey: state.customApiKey, aiTrialCount: state.aiTrialCount }),
    }
  )
)
