import { createContext, useContext } from 'react';
import type { User } from '../../api/types';

export interface AuthContextValue {
  status: 'loading' | 'guest' | 'user';
  user: User | null;
}

export const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth(): AuthContextValue {
  const value = useContext(AuthContext);
  if (!value) throw new Error('useAuth działa tylko wewnątrz AuthProvider');
  return value;
}
