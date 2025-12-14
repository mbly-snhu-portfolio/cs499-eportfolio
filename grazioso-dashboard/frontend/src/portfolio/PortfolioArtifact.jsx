/**
 * Artifact overview page.
 */
import './PortfolioLayout.css';

export default function PortfolioArtifact() {
  return (
    <div className="portfolio-doc">
      <div className="portfolio-docHeader">
        <h1 className="portfolio-title">Artifact Overview</h1>
      </div>

      <div className="portfolio-markdown">
        <h2>What this artifact is</h2>
        <p>
          This portfolio centers on the <strong>Grazioso Salvare Animal Shelter Dashboard</strong>, originally built as a
          Jupyter Notebook + Dash application (CS-340), and enhanced into a production-style three-tier web app.
        </p>

        <h2>Original vs enhanced</h2>
        <ul>
          <li>
            <strong>Original artifact:</strong> Notebook-based Dash UI with direct MongoDB access.
          </li>
          <li>
            <strong>Enhanced artifact:</strong> FastAPI backend (auth, RBAC, audit logging, rate limiting), React frontend
            (routing, state, charts/maps), caching + trie + fuzzy search, and database indexing/aggregation.
          </li>
        </ul>

        <h2>Where to find everything</h2>
        <ul>
          <li>
            <strong>Enhanced app:</strong> <code>grazioso-dashboard/</code>
          </li>
          <li>
            <strong>Original reference:</strong> <code>grazioso-dashboard/original/</code>
          </li>
          <li>
            <strong>Narratives & analysis:</strong> <code>grazioso-dashboard/docs/</code>
          </li>
        </ul>

        <h2>Try the dashboard (optional)</h2>
        <p>
          You can open the authenticated dashboard from the header link. The portfolio itself is public and does not
          require login.
        </p>

        <h3>Demo credentials</h3>
        <ul>
          <li>
            <strong>Admin:</strong> admin / admin123
          </li>
          <li>
            <strong>User:</strong> user / user123
          </li>
        </ul>
      </div>
    </div>
  );
}
