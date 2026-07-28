import { Navigate, Route, Routes } from "react-router-dom";
import ErrorBoundary from "./components/common/ErrorBoundary";
import AppLayout from "./components/layout/AppLayout";
import Automations from "./pages/Automations";
import Dashboard from "./pages/Dashboard";
import Help from "./pages/Help";
import Services from "./pages/Services";
import Settings from "./pages/Settings";
import States from "./pages/States";
import Tools from "./pages/Tools";

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
  );
}
