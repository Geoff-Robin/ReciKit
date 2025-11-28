import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from '@/pages/landingpage.jsx'
import Login from './pages/login'

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={ <LandingPage /> } />
      <Route path="/login" element={ <Login />} />
    </Routes>
  </BrowserRouter>
)
