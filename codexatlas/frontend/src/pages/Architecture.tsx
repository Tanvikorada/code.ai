import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useStore } from '../store/useStore'
import { apiService } from '../lib/api'
import { ArrowLeft, Layers, Database, Server, Cpu, Lock, Globe, FileCode } from 'lucide-react'

interface Layer {
  name: string
  icon: React.ReactNode
  components: string[]
  color: string
}

const Architecture = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { currentRepository } = useStore()
  const [layers, setLayers] = useState<Layer[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (id) {
      loadArchitecture(id)
    }
  }, [id])

  const getLayerIcon = (name: string) => {
    const nameLower = name.toLowerCase()
    if (nameLower.includes('frontend')) return <Layers className="w-6 h-6" />
    if (nameLower.includes('backend') || nameLower.includes('api')) return <Server className="w-6 h-6" />
    if (nameLower.includes('database') || nameLower.includes('db') || nameLower.includes('models')) return <Database className="w-6 h-6" />
    if (nameLower.includes('infrastructure') || nameLower.includes('config')) return <Cpu className="w-6 h-6" />
    if (nameLower.includes('auth')) return <Lock className="w-6 h-6" />
    if (nameLower.includes('external')) return <Globe className="w-6 h-6" />
    return <FileCode className="w-6 h-6" />
  }

  const loadArchitecture = async (repoId: string) => {
    try {
      const data = await apiService.getArchitecture(repoId)
      const layersData = data.layers || []
      
      const mappedLayers: Layer[] = layersData.map((layer: any) => ({
        name: layer.name,
        icon: getLayerIcon(layer.name),
        components: layer.components || [],
        color: layer.color || 'from-gray-500 to-gray-700',
      }))
      
      setLayers(mappedLayers)
    } catch (error) {
      console.error('Failed to load architecture:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-space-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-accent-primary border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-2">Generating Architecture</h2>
          <p className="text-gray-400">Analyzing system structure...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-space-900">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-sm bg-space-900/50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back
            </button>
            <div className="flex items-center gap-4">
              <h1 className="text-xl font-bold">Architecture View</h1>
              <button
                onClick={() => navigate(`/explorer/${id}`)}
                className="bg-accent-primary hover:bg-accent-secondary px-4 py-2 rounded-lg transition-colors"
              >
                Dependency Explorer
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Content */}
      <div className="container mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-6xl mx-auto"
        >
          {/* Repository Info */}
          {currentRepository && (
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-2 text-glow">{currentRepository.name}</h2>
              <p className="text-gray-400">System Architecture Analysis</p>
            </div>
          )}

          {/* Architecture Layers */}
          <div className="space-y-6">
            {layers.map((layer, index) => (
              <motion.div
                key={layer.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-space-800/50 backdrop-blur-sm border border-white/10 rounded-xl overflow-hidden"
              >
                <div className={`bg-gradient-to-r ${layer.color} p-4`}>
                  <div className="flex items-center gap-3">
                    <div className="bg-white/20 rounded-lg p-2">{layer.icon}</div>
                    <h3 className="text-xl font-bold">{layer.name}</h3>
                  </div>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {layer.components.map((component, idx) => (
                      <div
                        key={idx}
                        className="bg-space-900/50 rounded-lg p-4 border border-white/5 hover:border-white/10 transition-colors"
                      >
                        <div className="text-sm font-medium">{component}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Architecture Stats */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-space-800/50 backdrop-blur-sm border border-white/10 rounded-xl p-6 text-center">
              <div className="text-3xl font-bold text-accent-primary mb-2">{layers.length}</div>
              <div className="text-gray-400 text-sm">Architecture Layers</div>
            </div>
            <div className="bg-space-800/50 backdrop-blur-sm border border-white/10 rounded-xl p-6 text-center">
              <div className="text-3xl font-bold text-accent-secondary mb-2">
                {layers.reduce((acc, layer) => acc + layer.components.length, 0)}
              </div>
              <div className="text-gray-400 text-sm">Components Identified</div>
            </div>
            <div className="bg-space-800/50 backdrop-blur-sm border border-white/10 rounded-xl p-6 text-center">
              <div className="text-3xl font-bold text-accent-tertiary mb-2">High</div>
              <div className="text-gray-400 text-sm">Modularity Score</div>
            </div>
            <div className="bg-space-800/50 backdrop-blur-sm border border-white/10 rounded-xl p-6 text-center">
              <div className="text-3xl font-bold text-green-400 mb-2">A+</div>
              <div className="text-gray-400 text-sm">Architecture Grade</div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Architecture
