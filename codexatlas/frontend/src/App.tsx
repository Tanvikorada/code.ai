import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import Repository from './pages/Repository'
import Explorer from './pages/Explorer'
import Architecture from './pages/Architecture'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/repository/:id" element={<Repository />} />
        <Route path="/explorer/:id" element={<Explorer />} />
        <Route path="/architecture/:id" element={<Architecture />} />
      </Routes>
    </Router>
  )
}

export default App
