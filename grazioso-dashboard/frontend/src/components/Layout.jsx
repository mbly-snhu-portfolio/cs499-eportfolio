/**
 * Layout component with header and logo.
 */
import './Layout.css';

const Layout = ({ user, onLogout, children }) => {
  return (
    <div className="layout">
      <header className="header">
        <div className="header-content">
          <a href="https://www.snhu.edu" target="_blank" rel="noopener noreferrer">
            <img
              src="/Grazioso Salvare Logo.png"
              alt="Grazioso Salvare Logo"
              className="logo"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
          </a>
          <div className="header-info">
            <h1>Grazioso Salvare Animal Shelter Dashboard</h1>
            <p className="user-info">
              {user?.username} ({user?.role})
              <button onClick={onLogout} className="logout-btn">Logout</button>
            </p>
          </div>
        </div>
      </header>
      <main className="main-content">{children}</main>
    </div>
  );
};

export default Layout;

