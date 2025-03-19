import React from 'react';
import { Auth as SupabaseAuth } from '@supabase/auth-ui-react';
import { ThemeSupa } from '@supabase/auth-ui-shared';
import { supabase } from '../services/supabase';
import { useLocation, Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Auth.css';

export default function Auth() {
  const location = useLocation();
  const { user } = useAuth();
  const from = location.state?.from?.pathname || '/';

  // If user is already authenticated, redirect to home
  if (user) {
    return <Navigate to={from} replace />;
  }

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h1>Purple Ladder AI</h1>
        <p>Sign in to access your account</p>
        
        <SupabaseAuth
          supabaseClient={supabase}
          appearance={{ 
            theme: ThemeSupa,
            style: {
              container: { width: '100%' },
              anchor: { color: '#6B46C1' },
              button: { 
                background: '#6B46C1',
                color: 'white',
                borderRadius: '4px'
              },
              input: {
                borderRadius: '4px'
              }
            }
          }}
          providers={[]}
          redirectTo={window.location.origin + from}
        />
      </div>
    </div>
  );
} 