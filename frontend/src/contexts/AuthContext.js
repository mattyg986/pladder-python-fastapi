import React, { createContext, useContext, useState, useEffect } from 'react';
import { supabase } from '../services/supabase';

// Create a context for authentication
const AuthContext = createContext({
  user: null,
  session: null,
  loading: true,
  error: null,
  signIn: async () => {},
  signInWithEmail: async () => {},
  signOut: async () => {},
  getToken: () => {},
});

// Custom hook to use the auth context
export const useAuth = () => useContext(AuthContext);

// Helper to store token in localStorage
const storeToken = (token) => {
  localStorage.setItem('sb-access-token', token);
};

// Helper to retrieve token from localStorage
const getStoredToken = () => {
  return localStorage.getItem('sb-access-token');
};

// Helper to remove token from localStorage
const removeToken = () => {
  localStorage.removeItem('sb-access-token');
};

// Provider component to wrap the app
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    // Check current session
    const checkSession = async () => {
      try {
        // First try to get session from Supabase
        const { data: { session: currentSession } } = await supabase.auth.getSession();
        
        if (currentSession) {
          setUser(currentSession.user);
          setSession(currentSession);
          storeToken(currentSession.access_token);
        } else {
          // If no active session but token exists in storage, try to use it
          const storedToken = getStoredToken();
          if (storedToken) {
            try {
              // Try to get user with stored token
              const { data: { user: tokenUser } } = await supabase.auth.getUser(storedToken);
              if (tokenUser) {
                const refreshedSession = { access_token: storedToken, user: tokenUser };
                setUser(tokenUser);
                setSession(refreshedSession);
              } else {
                // Token is invalid, remove it
                removeToken();
                setUser(null);
                setSession(null);
              }
            } catch (err) {
              // Token validation failed
              removeToken();
              setUser(null);
              setSession(null);
            }
          } else {
            setUser(null);
            setSession(null);
          }
        }
      } catch (err) {
        console.error('Error checking session:', err);
        setError('Failed to check authentication status');
        setUser(null);
        setSession(null);
      } finally {
        setLoading(false);
      }
    };
    
    checkSession();
    
    // Subscribe to auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, newSession) => {
      setUser(newSession?.user ?? null);
      setSession(newSession);
      
      if (newSession) {
        storeToken(newSession.access_token);
      } else if (event === 'SIGNED_OUT') {
        removeToken();
      }
      
      setLoading(false);
    });
    
    return () => {
      subscription.unsubscribe();
    };
  }, []);
  
  // Sign in with OAuth provider
  const signIn = async (provider) => {
    try {
      setError(null);
      const { data, error: signInError } = await supabase.auth.signInWithOAuth({
        provider,
        options: {
          redirectTo: window.location.origin,
        },
      });
      
      if (signInError) throw signInError;
      return { data, error: null };
    } catch (error) {
      console.error('Error signing in:', error);
      setError(error.message || 'Failed to sign in');
      return { data: null, error };
    }
  };
  
  // Sign in with email/password
  const signInWithEmail = async (email, password) => {
    try {
      setError(null);
      const { data, error: signInError } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      
      if (signInError) throw signInError;
      return { data, error: null };
    } catch (error) {
      console.error('Error signing in with email:', error);
      setError(error.message || 'Failed to sign in');
      return { data: null, error };
    }
  };
  
  // Sign out function
  const signOut = async () => {
    try {
      await supabase.auth.signOut();
      removeToken();
      setUser(null);
      setSession(null);
      return { error: null };
    } catch (error) {
      console.error('Error signing out:', error);
      setError('Failed to sign out');
      return { error };
    }
  };
  
  // Get current token for API requests
  const getToken = () => {
    return session?.access_token || getStoredToken() || null;
  };

  // Context value
  const value = {
    user,
    session,
    loading,
    error,
    signIn,
    signInWithEmail,
    signOut,
    getToken,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 