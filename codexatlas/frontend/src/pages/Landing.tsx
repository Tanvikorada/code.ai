import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { useStore } from '../store/useStore'
import { apiService } from '../lib/api'
import { Github, Zap, Network, FileCode, ArrowRight, Brain, Shield, Clock } from 'lucide-react'
import AuthModal from '../components/AuthModal'
import { TypewriterText } from '../components/TypewriterText'

const Landing = () => {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [statusMsg, setStatusMsg] = useState('')
  const [showAuth, setShowAuth] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  const navigate = useNavigate()
  const setRepository = useStore((state) => state.setRepository)
  const setLoadingStore = useStore((state) => state.setLoading)

  useEffect(() => {
    setIsAuthenticated(apiService.isAuthenticated())
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!url) return

    if (!isAuthenticated) {
      setShowAuth(true)
      return
    }

    setLoading(true)
    setLoadingStore(true)
    setStatusMsg('Initiating AI scan...')

    try {
      const result = await apiService.scanRepository(url, (status) => {
        setStatusMsg(status)
      })
      setRepository(result)
      navigate(`/repository/${result.id}`)
    } catch (error) {
      console.error('Failed to scan repository:', error)
      alert('Failed to scan repository. Please check the URL and try again.')
    } finally {
      setLoading(false)
      setLoadingStore(false)
      setStatusMsg('')
    }
  }

  const handleLogout = () => {
    apiService.logout()
    setIsAuthenticated(false)
  }

  const features = [
    {
      icon: <Network className="w-5 h-5 text-aurora-cyan" />,
      title: 'Visual Knowledge Graph',
      description: 'Transform codebases into interactive dependency maps instantly.',
    },
    {
      icon: <Zap className="w-5 h-5 text-aurora-purple" />,
      title: 'Story Mode',
      description: 'Trace business logic through cinematic data flow animations.',
    },
    {
      icon: <Brain className="w-5 h-5 text-white" />,
      title: 'AI Architect',
      description: 'Ask repository-aware questions with context-aware AI.',
    },
    {
      icon: <Shield className="w-5 h-5 text-aurora-cyan" />,
      title: 'Health Scanner',
      description: 'Detect dead code, circular dependencies, and code smells.',
    },
    {
      icon: <Clock className="w-5 h-5 text-aurora-purple" />,
      title: 'Timeline Explorer',
      description: 'Visual evolution of your software architecture over time.',
    },
    {
      icon: <FileCode className="w-5 h-5 text-white" />,
      title: 'Auto Documentation',
      description: 'Generate comprehensive docs automatically from code structure.',
    },
  ]

  return (
    <div className="min-h-screen bg-obsidian relative overflow-hidden font-sans">
      {showAuth && (
        <AuthModal 
          onClose={() => setShowAuth(false)} 
          onLogin={() => {
            setIsAuthenticated(true)
            setShowAuth(false)
          }} 
        />
      )}
      
      {/* Aurora Background Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute w-[600px] h-[600px] bg-aurora-purple/20 rounded-full blur-[120px] top-[-10%] left-[-10%] mix-blend-screen animate-blob" />
        <div className="absolute w-[600px] h-[600px] bg-aurora-cyan/10 rounded-full blur-[120px] bottom-[-10%] right-[-10%] mix-blend-screen animate-blob" style={{ animationDelay: '2s' }} />
        <div className="absolute w-[800px] h-[800px] bg-aurora-indigo/20 rounded-full blur-[150px] top-[20%] left-[30%] mix-blend-screen animate-blob" style={{ animationDelay: '4s' }} />
      </div>

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <header className="glass-panel sticky top-0 z-50">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-aurora-cyan to-aurora-purple flex items-center justify-center shadow-[0_0_20px_rgba(0,240,255,0.4)]">
                  <div className="w-3 h-3 bg-white rounded-full" />
                </div>
                <span className="text-xl font-bold tracking-tight text-white">CodexAtlas</span>
              </div>
              <nav className="hidden md:flex items-center gap-8">
                <a href="#features" className="text-sm font-medium text-white/60 hover:text-white transition-colors">Features</a>
                <a href="#demo" className="text-sm font-medium text-white/60 hover:text-white transition-colors">Demo</a>
                {isAuthenticated ? (
                  <button onClick={handleLogout} className="text-sm font-medium text-white/60 hover:text-red-400 transition-colors">
                    Logout
                  </button>
                ) : (
                  <button onClick={() => setShowAuth(true)} className="glass-card px-5 py-2 rounded-full text-sm font-medium text-white hover:bg-white/10 transition-colors">
                    Sign In
                  </button>
                )}
              </nav>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="container mx-auto px-6 pt-32 pb-24 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="max-w-4xl mx-auto"
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full glass-card text-xs font-medium text-aurora-cyan mb-8 border-aurora-cyan/20">
              <span className="w-2 h-2 rounded-full bg-aurora-cyan animate-pulse" />
              CodexAtlas v2.0 is live
            </div>
            
            <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold mb-8 tracking-tighter leading-[1.1]">
              <TypewriterText text="Visualize your " delay={60} />
              <br/>
              <motion.span 
                className="text-gradient inline-block"
                initial={{ opacity: 0, filter: 'blur(10px)' }}
                animate={{ opacity: 1, filter: 'blur(0px)' }}
                transition={{ delay: 1.5, duration: 1 }}
              >
                software universe.
              </motion.span>
            </h1>
            
            <motion.p 
              className="text-lg md:text-xl text-white/50 mb-12 max-w-2xl mx-auto leading-relaxed font-medium"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 2.2, duration: 0.8 }}
            >
              Transform any GitHub repository into an interactive, spatial map. Understand complex architectures instantly with our AI-powered intelligence layer.
            </motion.p>

            {/* URL Input */}
            <motion.form 
              onSubmit={handleSubmit} 
              className="max-w-2xl mx-auto mb-16"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 2.8, duration: 0.6, type: 'spring' }}
            >
              <div className="glass-card rounded-2xl p-2 flex items-center shadow-2xl relative overflow-hidden group border-white/20 hover:border-white/40 transition-colors">
                <div className="absolute inset-0 bg-gradient-to-r from-aurora-cyan/10 to-aurora-purple/10 opacity-0 group-hover:opacity-100 transition-opacity" />
                <Github className="w-6 h-6 text-white/40 ml-4 relative z-10" />
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="Paste GitHub repository URL..."
                  className="flex-1 bg-transparent border-none outline-none px-4 py-4 text-white placeholder-white/30 text-lg relative z-10"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={loading || !url}
                  className="relative z-10 bg-white text-obsidian disabled:opacity-50 disabled:cursor-not-allowed px-8 py-3 rounded-xl flex items-center gap-2 font-semibold hover:bg-white/90 transition-colors"
                >
                  {loading ? 'Scanning...' : 'Analyze'}
                  {!loading && <ArrowRight className="w-4 h-4" />}
                </button>
              </div>
              {loading && (
                <div className="mt-4 flex items-center justify-center gap-2 text-aurora-cyan text-sm font-medium">
                  <div className="w-4 h-4 border-2 border-aurora-cyan border-t-transparent rounded-full animate-spin" />
                  {statusMsg}
                </div>
              )}
            </motion.form>
          </motion.div>
        </section>

        {/* Features Section */}
        <section id="features" className="container mx-auto px-6 py-24 relative">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">Spatial Intelligence</h2>
            <p className="text-white/50 text-lg">Everything you need to decode complex codebases.</p>
          </div>
          
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={{
              visible: {
                transition: {
                  staggerChildren: 0.15
                }
              },
              hidden: {}
            }}
          >
            {features.map((feature, index) => (
              <motion.div
                key={index}
                variants={{
                  hidden: { opacity: 0, y: 30, scale: 0.95 },
                  visible: { opacity: 1, y: 0, scale: 1, transition: { type: 'spring', stiffness: 100 } }
                }}
                className="glass-card glass-card-hover rounded-2xl p-8 group relative overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-white/[0.05] to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="w-12 h-12 rounded-xl bg-white/[0.05] border border-white/10 flex items-center justify-center mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3 tracking-tight">{feature.title}</h3>
                <p className="text-white/50 leading-relaxed font-medium text-sm">{feature.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </section>
        
        {/* Footer */}
        <footer className="border-t border-white/[0.05] py-12 mt-20 relative z-10">
          <div className="container mx-auto px-6 text-center">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-aurora-cyan to-aurora-purple flex items-center justify-center mx-auto mb-6 opacity-80">
              <div className="w-2 h-2 bg-white rounded-full" />
            </div>
            <p className="text-white/40 text-sm font-medium">
              CodexAtlas &copy; 2026. The Spatial Intelligence Layer.
            </p>
          </div>
        </footer>
      </div>
    </div>
  )
}

export default Landing
