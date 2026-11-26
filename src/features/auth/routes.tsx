import { Navigate, Outlet } from 'react-router';
import { useAuth } from './context';

/** Podstrony tylko dla zalogowanych. */
export function ProtectedRoute() {
  const { status } = useAuth();
  if (status === 'loading') return <p className="p-8 text-slate-500">Wczytywanie…</p>;
  return status === 'user' ? <Outlet /> : <Navigate to="/login" replace />;
}
