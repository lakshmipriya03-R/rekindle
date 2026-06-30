import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/layout/ProtectedRoute'
import Sidebar from './components/layout/Sidebar'

import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Journal from './pages/Journal'
import JournalEntry from './pages/JournalEntry'
import Chat from './pages/Chat'
import Timeline from './pages/Timeline'
import EmotionDashboard from './pages/EmotionDashboard'
import Settings from './pages/Settings'

function AppLayout({ children }) {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        {children}
      </main>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={
              <AppLayout><Dashboard /></AppLayout>
            } />
            <Route path="/journals" element={
              <AppLayout><Journal /></AppLayout>
            } />
            <Route path="/journals/new" element={
              <AppLayout><JournalEntry /></AppLayout>
            } />
            <Route path="/journals/:id" element={
              <AppLayout><JournalEntry /></AppLayout>
            } />
            <Route path="/chat" element={
              <AppLayout><Chat /></AppLayout>
            } />
            <Route path="/chat/:sessionId" element={
              <AppLayout><Chat /></AppLayout>
            } />
            <Route path="/timeline" element={
              <AppLayout><Timeline /></AppLayout>
            } />
            <Route path="/emotions" element={
              <AppLayout><EmotionDashboard /></AppLayout>
            } />
            <Route path="/settings" element={
              <AppLayout><Settings /></AppLayout>
            } />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
