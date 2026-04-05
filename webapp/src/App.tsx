import { Routes, Route, Navigate } from 'react-router-dom'
import AppLayout from './components/layout/AppLayout'
import ErrorBoundary from './components/common/ErrorBoundary'
import Dashboard from './pages/Dashboard'
import States from './pages/States'
import Services from './pages/Services'
import Automations from './pages/Automations'
import Settings from './pages/Settings'
import Help from './pages/Help'
import Tools from './pages/Tools'

export default function App() {
  return (
    <ErrorBoundary>
      <AppLayout>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/states" element={<States />} />
          <Route path="/services" element={<Services />} />
          <Route path="/automations" element={<Automations />} />
          <Route path="/tools" element={<Tools />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/help" element={<Help />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AppLayout>
    </ErrorBoundary>
  )
}
