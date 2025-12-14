/**
 * Public ePortfolio layout (no login required).
 */
import { NavLink, Outlet } from 'react-router-dom';
import './PortfolioLayout.css';

function NavItem({ to, children }) {
  return (
    <NavLink
      to={to}
      end
      className={({ isActive }) => `portfolio-navLink ${isActive ? 'is-active' : ''}`}
    >
      {children}
    </NavLink>
  );
}

export default function PortfolioLayout() {
  return (
    <div className="portfolio-shell">
      <header className="portfolio-topbar">
        <div className="portfolio-topbarInner">
          <div className="portfolio-brand">
            <div className="portfolio-brandTitle">CS 499 ePortfolio</div>
            <div className="portfolio-brandSubtitle">Grazioso Salvare: Animal Shelter Dashboard (Enhanced)</div>
          </div>
          <div className="portfolio-topbarLinks">
            <a className="portfolio-toplink" href="#/app">Open Dashboard App</a>
          </div>
        </div>
      </header>

      <div className="portfolio-body">
        <aside className="portfolio-nav">
          <div className="portfolio-navGroup">
            <div className="portfolio-navHeading">Portfolio</div>
            <NavItem to="/">Professional Self-Assessment</NavItem>
            <NavItem to="/artifact">Artifact Overview</NavItem>
            <NavItem to="/code-review">Informal Code Review</NavItem>
          </div>

          <div className="portfolio-navGroup">
            <div className="portfolio-navHeading">Enhancement Narratives</div>
            <NavItem to="/enhancements/software">Software Design & Engineering</NavItem>
            <NavItem to="/enhancements/algorithms">Algorithms & Data Structures</NavItem>
            <NavItem to="/enhancements/databases">Databases</NavItem>
          </div>

          <div className="portfolio-navGroup">
            <div className="portfolio-navHeading">Repository</div>
            <a className="portfolio-navLink" href="./" target="_blank" rel="noreferrer">
              View Site Root
            </a>
          </div>
        </aside>

        <main className="portfolio-content">
          <Outlet />
        </main>
      </div>

      <footer className="portfolio-footer">
        <div className="portfolio-footerInner">
          <span>Focus: Technical Leadership (architecture decisions, trade-offs, security mindset)</span>
        </div>
      </footer>
    </div>
  );
}
