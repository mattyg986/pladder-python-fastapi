import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Layout.css';

/**
 * Main layout component for authenticated pages only
 * This component should only be used for protected routes
 */
const Layout = ({ children }) => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  
  // Handle logout click
  const handleLogout = async () => {
    await signOut();
    navigate('/login');
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo">
          <h1>Purple Ladder AI</h1>
        </div>
        <nav className="main-nav">
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/dashboard">Dashboard</Link>
            </li>
          </ul>
        </nav>
        <div className="user-section">
          {user && (
            <>
              <span className="user-email">{user.email}</span>
              <button className="logout-button" onClick={handleLogout}>
                Sign Out
              </button>
            </>
          )}
        </div>
      </header>
      <main className="content-area">
        {children}
      </main>
      <footer className="app-footer">
        <p>&copy; {new Date().getFullYear()} Purple Ladder AI</p>
      </footer>
    </div>
  );
};

export default Layout; 