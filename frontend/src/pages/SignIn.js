import React from 'react';
import { Auth as SupabaseAuth } from '@supabase/auth-ui-react';
import { ThemeSupa } from '@supabase/auth-ui-shared';
import { supabase } from '../services/supabase';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function SignIn() {
  const { user } = useAuth();

  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column',
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh',
      backgroundColor: '#663399' 
    }}>
      <div style={{
        textAlign: 'center',
        color: 'white',
        marginBottom: '2rem'
      }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>
          Purple Ladder AI Agents Platform
        </h1>
        <p style={{ fontSize: '1.2rem' }}>
          Welcome to the future of talent acquisition
        </p>
      </div>
      <div style={{ 
        width: '100%', 
        maxWidth: '400px',
        padding: '2rem',
        backgroundColor: 'white',
        borderRadius: '8px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
      }}>
        <h2 style={{ textAlign: 'center', marginBottom: '2rem', color: '#663399' }}>Sign In</h2>
        <SupabaseAuth
          supabaseClient={supabase}
          appearance={{ 
            theme: ThemeSupa,
            variables: {
              default: {
                colors: {
                  brand: '#663399',
                  brandAccent: '#553399'
                }
              }
            }
          }}
          providers={[]}
          redirectTo={window.location.origin + '/dashboard'}
        />
      </div>
    </div>
  );
} 