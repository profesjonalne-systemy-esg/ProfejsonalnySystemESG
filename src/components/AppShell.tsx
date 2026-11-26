import { BookOpen, ClipboardCheck, CloudUpload, FileText, LayoutDashboard } from 'lucide-react';
import { NavLink, Outlet, useParams } from 'react-router';
import { useApi } from '../api/useApi';
import type { Project } from '../api/types';
import { useAuth } from '../features/auth/context';
import { Logo } from './Logo';

const ROLES = { specialist: 'Specjalista ESG', manager: 'Kierownik', admin: 'Administrator' };

export function AppShell() {
  const { user } = useAuth();
  const { projectId } = useParams();
  const { data: projects } = useApi<Project[]>('/projects');
  const current = projects?.find((p) => String(p.id) === projectId) ?? projects?.[0];
  const base = current ? `/projects/${current.id}` : null;

  const links = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    ...(base
      ? [
          { to: `${base}/documents`, label: 'Dokumenty', icon: CloudUpload },
          { to: `${base}/metrics`, label: 'Weryfikacja', icon: ClipboardCheck },
          { to: `${base}/report`, label: 'Raport GRI', icon: FileText },
        ]
      : []),
    { to: '/knowledge', label: 'Baza wiedzy ESG', icon: BookOpen },
  ];

  return (
    <div className="flex min-h-screen flex-col bg-slate-50 font-sans text-slate-900 md:flex-row">
      <aside className="flex shrink-0 flex-col bg-navy px-4 py-6 text-slate-400 md:sticky md:top-0 md:h-screen md:w-64">
        <div className="px-2">
          <Logo dark />
        </div>
        <p className="mt-8 px-3 text-xs font-bold tracking-[0.16em] uppercase">Obszar roboczy</p>
        <nav className="mt-3 flex flex-wrap gap-1 md:flex-col">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 font-semibold transition ${
                  isActive ? 'bg-brand/25 text-brand-light' : 'hover:bg-white/5 hover:text-white'
                }`
              }
            >
              <Icon className="h-5 w-5" aria-hidden />
              {label}
            </NavLink>
          ))}
        </nav>
        {user && (
          <div className="mt-auto hidden border-t border-white/10 px-3 pt-5 md:block">
            <p className="font-semibold text-white">{user.full_name}</p>
            <p className="text-sm">{ROLES[user.role]}</p>
          </div>
        )}
      </aside>
      <main className="min-w-0 grow">
        <Outlet />
      </main>
    </div>
  );
}
