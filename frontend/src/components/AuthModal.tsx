import { useState } from 'react';
import { apiService } from '../lib/api';

export default function AuthModal({ onClose, onLogin }: { onClose: () => void, onLogin: () => void }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      if (isLogin) {
        await apiService.login(username, password);
        onLogin();
      } else {
        await apiService.register(username, password, email);
        await apiService.login(username, password);
        onLogin();
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Authentication failed');
    }
  };

  return (
    <div className="fixed inset-0 bg-obsidian/80 backdrop-blur-md z-50 flex items-center justify-center font-sans">
      <div className="glass-panel p-10 rounded-3xl w-[400px] relative shadow-2xl overflow-hidden">
        {/* Subtle ambient glow inside modal */}
        <div className="absolute top-0 right-0 w-48 h-48 bg-aurora-cyan/10 blur-[50px] rounded-full pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-aurora-purple/10 blur-[50px] rounded-full pointer-events-none" />
        
        <button onClick={onClose} className="absolute top-5 right-5 text-white/40 hover:text-white transition-colors z-10">✕</button>
        
        <div className="relative z-10">
          <h2 className="text-3xl font-bold mb-8 tracking-tight text-white">{isLogin ? 'Welcome back' : 'Create account'}</h2>
          
          {error && <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-xl mb-6 text-sm font-medium">{error}</div>}
          
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              className="bg-white/[0.03] border border-white/[0.08] focus:border-aurora-cyan/50 focus:bg-white/[0.05] p-4 rounded-xl text-white placeholder-white/30 outline-none transition-all font-medium"
              required
            />
            {!isLogin && (
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="bg-white/[0.03] border border-white/[0.08] focus:border-aurora-cyan/50 focus:bg-white/[0.05] p-4 rounded-xl text-white placeholder-white/30 outline-none transition-all font-medium"
                required
              />
            )}
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="bg-white/[0.03] border border-white/[0.08] focus:border-aurora-cyan/50 focus:bg-white/[0.05] p-4 rounded-xl text-white placeholder-white/30 outline-none transition-all font-medium"
              required
            />
            <button type="submit" className="bg-white text-obsidian font-bold py-4 rounded-xl hover:bg-white/90 transition-colors mt-2 shadow-[0_0_20px_rgba(255,255,255,0.2)]">
              {isLogin ? 'Sign In' : 'Sign Up'}
            </button>
          </form>
          
          <p className="mt-6 text-center text-sm font-medium text-white/40">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button onClick={() => setIsLogin(!isLogin)} className="text-white hover:text-aurora-cyan transition-colors">
              {isLogin ? 'Sign up' : 'Sign in'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
