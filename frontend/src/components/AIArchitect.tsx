import { useState } from 'react'
import { Send, Brain, Key, Loader2, AlertCircle } from 'lucide-react'
import { motion } from 'framer-motion'
import { useStore } from '../store/useStore'
import { apiService } from '../lib/api'

export const AIArchitect = ({ repoId }: { repoId: string }) => {
  const { customApiKey, setCustomApiKey, aiTrialCount, incrementAiTrialCount } = useStore()
  const [messages, setMessages] = useState<{role: 'user'|'assistant', content: string}[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showKeyInput, setShowKeyInput] = useState(false)
  const [tempKey, setTempKey] = useState('')

  const isTrialEnded = aiTrialCount >= 3 && !customApiKey

  const handleAsk = async () => {
    if (!input.trim() || isLoading) return
    if (isTrialEnded) {
      setShowKeyInput(true)
      return
    }

    const userMsg = input
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMsg }])
    setIsLoading(true)

    try {
      const response = await apiService.askAI(repoId, userMsg, customApiKey || undefined)
      setMessages(prev => [...prev, { role: 'assistant', content: response.answer }])
      
      if (!customApiKey) {
        incrementAiTrialCount()
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error analyzing the repository. Please ensure your API key is correct or try again." }])
    } finally {
      setIsLoading(false)
    }
  }

  const saveKey = () => {
    if (tempKey.trim()) {
      setCustomApiKey(tempKey.trim())
      setShowKeyInput(false)
    }
  }

  return (
    <div className="glass-card rounded-3xl overflow-hidden flex flex-col h-[500px]">
      {/* Header */}
      <div className="p-4 border-b border-white/[0.05] flex items-center justify-between bg-white/[0.02] relative">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-aurora-purple/20 flex items-center justify-center">
            <Brain className="w-4 h-4 text-aurora-purple" />
          </div>
          <div>
            <h3 className="font-semibold tracking-tight text-white">AI Architect</h3>
            <div className="text-xs text-white/50">
              {customApiKey ? 'Using Custom API Key' : `Trial: ${3 - aiTrialCount} questions remaining`}
            </div>
          </div>
        </div>
        {!customApiKey && (
          <button 
            onClick={() => setShowKeyInput(!showKeyInput)}
            className="text-xs bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded-full transition-colors flex items-center gap-1"
          >
            <Key className="w-3 h-3" />
            Add Key
          </button>
        )}
      </div>

      {/* API Key Modal / Overlay */}
      {showKeyInput && (
        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute inset-x-4 top-20 z-10 bg-obsidian p-4 rounded-xl border border-aurora-purple/30 shadow-xl"
        >
          <div className="flex items-start gap-3 mb-3">
            <AlertCircle className="w-5 h-5 text-aurora-purple shrink-0 mt-0.5" />
            <div className="text-sm text-white/80">
              {isTrialEnded 
                ? "Your free trial has ended. Please enter your Gemini or Groq API key to continue exploring the codebase."
                : "Enter your Gemini or Groq API key to unlock unlimited questions."}
            </div>
          </div>
          <div className="flex gap-2">
            <input 
              type="password"
              placeholder="API Key (gsk_... or AIza...)"
              value={tempKey}
              onChange={(e) => setTempKey(e.target.value)}
              className="flex-1 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-aurora-purple"
            />
            <button 
              onClick={saveKey}
              className="bg-aurora-purple text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-aurora-purple/90 transition-colors"
            >
              Save
            </button>
            <button 
              onClick={() => setShowKeyInput(false)}
              className="bg-white/10 text-white hover:bg-white/20 px-4 py-2 rounded-lg text-sm transition-colors"
            >
              Cancel
            </button>
          </div>
        </motion.div>
      )}

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center text-white/40 px-4">
            <Brain className="w-12 h-12 mb-4 opacity-20" />
            <p className="text-sm">Ask me to explain the architecture, find where authentication happens, or analyze code health.</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm ${
              msg.role === 'user' 
                ? 'bg-aurora-purple text-white rounded-br-none' 
                : 'bg-white/5 border border-white/10 rounded-bl-none text-white/90'
            }`}>
              <div className="whitespace-pre-wrap">{msg.content}</div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white/5 border border-white/10 rounded-2xl rounded-bl-none px-4 py-3">
              <Loader2 className="w-4 h-4 animate-spin text-aurora-purple" />
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-white/[0.05] bg-white/[0.01]">
        <form 
          onSubmit={(e) => { e.preventDefault(); handleAsk(); }}
          className="relative"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading || showKeyInput}
            placeholder={isTrialEnded ? "Trial ended. Add API key to continue." : "Ask about the codebase..."}
            className="w-full bg-white/5 text-white border border-white/10 rounded-xl pl-4 pr-12 py-3 text-sm focus:outline-none focus:border-aurora-purple/50 disabled:opacity-50 transition-colors"
          />
          <button
            type="submit"
            aria-label="Send message"
            disabled={!input.trim() || isLoading || showKeyInput}
            className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 flex items-center justify-center bg-aurora-purple/20 text-aurora-purple rounded-lg hover:bg-aurora-purple/30 disabled:opacity-50 disabled:hover:bg-aurora-purple/20 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  )
}
