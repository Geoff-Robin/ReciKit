import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from '@/pages/landingpage'
import Login from '@/pages/login'
import SignUp from '@/pages/signup.jsx'
import './index.css'

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={ <LandingPage /> } />
      <Route path="/login" element={ <Login />} />
      <Route path="/signup" element={ <SignUp />} />
    </Routes>
  </BrowserRouter>
)
