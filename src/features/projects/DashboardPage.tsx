import { Link } from 'react-router';
import { useApi } from '../../api/useApi';
import type { Project } from '../../api/types';

/** Baza: prosta lista. Kafelki i tworzenie projektu dodaje US 2.4. */
export function DashboardPage() {
  const { data, error, loading } = useApi<Project[]>('/projects');
  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold tracking-tight text-navy">Projekty raportowe</h1>
      {loading && <p className="mt-4 text-slate-500">Wczytywanie…</p>}
      {error && <p className="mt-4 text-red-600">{error}</p>}
      <ul className="mt-6 space-y-2">
        {data?.map((project) => (
          <li key={project.id}>
            <Link to={`/projects/${project.id}/documents`} className="font-semibold text-brand hover:text-brand-dark">
              {project.name}
            </Link>{' '}
            <span className="text-slate-500">
              {project.company_name}, {project.year}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
