import { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useStore } from '../store/useStore'
import { apiService } from '../lib/api'
import { ArrowLeft, Loader2, CheckCircle, AlertCircle } from 'lucide-react'

const Repository = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { currentRepository, isLoading, setRepository, setLoading, setNodes, setEdges } = useStore()

  useEffect(() => {
    if (id) {
      loadRepositoryData(id)
    }
  }, [id])

  const loadRepositoryData = async (repoId: string) => {
    // Note: the repository is already loaded into the store by scanRepository in Landing.tsx
    // However, if a user directly navigates here, we might need to fetch it.
    // For now, if currentRepository exists and matches id, we just use it.
    if (!currentRepository || currentRepository.id !== repoId) {
       // Just set loading false if we can't find it to show not found
       setLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-obsidian flex items-center justify-center font-sans">
        <div className="text-center relative">
          <div className="absolute inset-0 bg-aurora-cyan/20 blur-[100px] rounded-full" />
          <Loader2 className="w-16 h-16 text-aurora-cyan mx-auto mb-6 animate-spin relative z-10" />
          <h2 className="text-3xl font-bold mb-2 tracking-tight relative z-10">Analyzing Structure</h2>
          <p className="text-white/50 font-medium relative z-10">Constructing spatial knowledge graph...</p>
        </div>
      </div>
    )
  }

  if (!currentRepository) {
    return (
      <div className="min-h-screen bg-obsidian flex items-center justify-center font-sans">
        <div className="text-center">
          <AlertCircle className="w-16 h-16 text-red-400 mx-auto mb-6" />
          <h2 className="text-3xl font-bold mb-2 tracking-tight">Repository Not Found</h2>
          <button
            onClick={() => navigate('/')}
            className="mt-6 bg-white text-obsidian font-bold px-8 py-3 rounded-xl transition-colors hover:bg-white/90"
          >
            Go Back
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-obsidian font-sans relative">
      {/* Background Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[300px] bg-aurora-purple/10 blur-[120px] pointer-events-none rounded-full mix-blend-screen" />
      
      {/* Header */}
      <header className="glass-panel sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-2 text-white/50 hover:text-white transition-colors font-medium text-sm"
            >
              <ArrowLeft className="w-4 h-4" />
              Overview
            </button>
            <div className="flex items-center gap-4">
              <button 
                onClick={() => navigate(`/explorer/${id}`)}
                className="glass-card hover:bg-white/10 px-5 py-2.5 rounded-xl transition-colors text-sm font-semibold"
              >
                Explore Graph
              </button>
              <button 
                onClick={() => navigate(`/architecture/${id}`)}
                className="bg-white text-obsidian px-5 py-2.5 rounded-xl transition-colors text-sm font-semibold hover:bg-white/90 shadow-[0_0_15px_rgba(255,255,255,0.2)]"
              >
                Architecture
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Content */}
      <div className="container mx-auto px-6 py-16 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl mx-auto"
        >
          {/* Repository Info */}
          <div className="glass-card rounded-3xl p-10 mb-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-aurora-cyan/5 blur-[80px] rounded-full pointer-events-none" />
            
            <div className="flex items-start justify-between relative z-10">
              <div>
                <h1 className="text-4xl md:text-5xl font-bold mb-3 tracking-tight">{currentRepository.name}</h1>
                <a href={currentRepository.url} target="_blank" rel="noopener noreferrer" className="text-aurora-cyan hover:text-white transition-colors font-medium">
                  {currentRepository.url}
                </a>
              </div>
              <div className="flex items-center gap-2 text-aurora-cyan bg-aurora-cyan/10 px-4 py-2 rounded-full text-sm font-semibold border border-aurora-cyan/20">
                <CheckCircle className="w-4 h-4" />
                <span>Indexed</span>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12 relative z-10">
              <div className="bg-white/[0.02] border border-white/[0.05] rounded-2xl p-5">
                <div className="text-white/40 text-sm mb-1 font-medium">Framework</div>
                <div className="text-xl font-semibold tracking-tight">{currentRepository.framework}</div>
              </div>
              <div className="bg-white/[0.02] border border-white/[0.05] rounded-2xl p-5">
                <div className="text-white/40 text-sm mb-1 font-medium">Language</div>
                <div className="text-xl font-semibold tracking-tight">{currentRepository.language}</div>
              </div>
            </div>
          </div>

          {/* Analysis Summary */}
          <div className="glass-card rounded-3xl p-10 relative overflow-hidden">
             <div className="absolute bottom-0 left-0 w-64 h-64 bg-aurora-purple/5 blur-[80px] rounded-full pointer-events-none" />
            
            <h2 className="text-2xl font-bold mb-8 tracking-tight relative z-10">Health Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-10">
              <div className="text-center bg-white/[0.02] border border-white/[0.05] rounded-2xl p-6">
                <div className="text-5xl font-bold text-aurora-cyan mb-3 tracking-tighter">{currentRepository.health?.overall_score ?? '—'}</div>
                <div className="text-white/50 text-sm font-medium">Code Quality</div>
              </div>
              <div className="text-center bg-white/[0.02] border border-white/[0.05] rounded-2xl p-6">
                <div className="text-5xl font-bold text-white mb-3 tracking-tighter">{currentRepository.health?.maintainability ?? '—'}</div>
                <div className="text-white/50 text-sm font-medium">Maintainability</div>
              </div>
              <div className="text-center bg-white/[0.02] border border-white/[0.05] rounded-2xl p-6">
                <div className="text-5xl font-bold text-aurora-purple mb-3 tracking-tighter">{currentRepository.health?.documentation ?? '—'}</div>
                <div className="text-white/50 text-sm font-medium">Documentation</div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Repository
