import { Routes, Route } from 'react-router';
import { AppShell } from './components/AppShell';
import { PublicLayout } from './components/PublicLayout';
import { LoginPage } from './features/auth/LoginPage';
import { RegisterPage } from './features/auth/RegisterPage';
import { ProtectedRoute } from './features/auth/routes';
import { DocumentsPage } from './features/documents/DocumentsPage';
import { EditorPage } from './features/editor/EditorPage';
import { KnowledgePage } from './features/knowledge/KnowledgePage';
import { MetricsPage } from './features/metrics/MetricsPage';
import { DashboardPage } from './features/projects/DashboardPage';
import { AboutPage } from './pages/AboutPage';
import { HomePage } from './pages/HomePage';

/** Wszystkie trasy są już wpisane. Epiki zmieniają tylko swoje strony w src/features. */
function App() {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/o-nas" element={<AboutPage />} />
      </Route>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<AppShell />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/knowledge" element={<KnowledgePage />} />
          <Route path="/projects/:projectId/documents" element={<DocumentsPage />} />
          <Route path="/projects/:projectId/metrics" element={<MetricsPage />} />
          <Route path="/projects/:projectId/report" element={<EditorPage />} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
