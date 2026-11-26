import { Link, Outlet } from 'react-router';

/** Nagłówek i stopka stron publicznych. */
export function PublicLayout() {
  return (
    <div className="flex min-h-screen flex-col bg-slate-50 font-sans text-slate-900">
      <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
          <Link to="/" className="text-xl font-bold text-navy">
            Build<span className="text-brand">ESG</span>
          </Link>
          <nav className="flex items-center gap-6">
            <Link to="/" className="text-sm font-medium text-slate-600 transition hover:text-brand">
              Strona główna
            </Link>
            <Link to="/o-nas" className="text-sm font-medium text-slate-600 transition hover:text-brand">
              O projekcie
            </Link>
            <Link
              to="/login"
              className="rounded-lg bg-brand px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-brand-dark"
            >
              Zaloguj się
            </Link>
          </nav>
        </div>
      </header>
      <main className="grow">
        <Outlet />
      </main>
      <footer className="border-t border-slate-200 bg-white py-8 text-center text-sm text-slate-500">
        © {new Date().getFullYear()} Profesjonalne Systemy ESG
      </footer>
    </div>
  );
}
