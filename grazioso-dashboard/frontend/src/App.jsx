/**
 * Main App component with routing.
 */
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import PortfolioLayout from './portfolio/PortfolioLayout';
import PortfolioHome from './portfolio/PortfolioHome';
import PortfolioArtifact from './portfolio/PortfolioArtifact';
import MarkdownPage from './portfolio/MarkdownPage';
import './App.css';

// Protected route component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  return isAuthenticated ? children : <Navigate to="/app/login" replace />;
};

function AppRoutes() {
  return (
    <Routes>
      <Route
        path="/app"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route path="/app/login" element={<Login />} />

      {/* Public ePortfolio (no login required) */}
      <Route path="/" element={<PortfolioLayout />}>
        <Route index element={<PortfolioHome />} />
        <Route path="artifact" element={<PortfolioArtifact />} />
        <Route
          path="enhancements/software"
          element={
            <MarkdownPage
              title="Enhancement Narrative: Software Design & Engineering"
              assetPath="portfolio/enhancement_narrative.md"
              pdfPath="portfolio/enhancement_narrative.pdf"
            />
          }
        />
        <Route
          path="enhancements/algorithms"
          element={
            <MarkdownPage
              title="Enhancement Narrative: Algorithms & Data Structures"
              assetPath="portfolio/enhancement_narrative_algorithms.md"
              pdfPath="portfolio/enhancement_narrative_algorithms.pdf"
            />
          }
        />
        <Route
          path="enhancements/databases"
          element={
            <MarkdownPage
              title="Enhancement Narrative: Databases"
              assetPath="portfolio/enhancement_narrative_databases.md"
            />
          }
        />
        <Route
          path="code-review"
          element={
            <MarkdownPage
              title="Informal Code Review (Written)"
              assetPath="portfolio/informal_code_review.md"
            />
          }
        />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <HashRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </HashRouter>
  );
}

export default App;
