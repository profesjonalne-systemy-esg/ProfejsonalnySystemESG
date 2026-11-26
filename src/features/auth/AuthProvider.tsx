import { useEffect, useState, type ReactNode } from 'react';
import { api } from '../../api/client';
import type { User } from '../../api/types';
import { AuthContext, type AuthContextValue } from './context';

/** Baza: pyta backend, kim jesteśmy (w trybie demo to specjalista@demo.pl). Logowanie dodaje US 2.3. */
export function AuthProvider({ children }: { children: ReactNode }) {
  const [value, setValue] = useState<AuthContextValue>({ status: 'loading', user: null });

  useEffect(() => {
    let active = true;
    api<User>('/auth/me')
      .then((user) => {
        if (active) setValue({ status: 'user', user });
      })
      .catch(() => {
        if (active) setValue({ status: 'guest', user: null });
      });
    return () => {
      active = false;
    };
  }, []);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
