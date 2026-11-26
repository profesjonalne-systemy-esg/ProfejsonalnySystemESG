/** Wspólne typy odpowiedzi API. Typy jednego epiku trzymaj w jego katalogu. */

export type ProjectStatus = 'draft' | 'in_review' | 'changes_requested' | 'approved';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'specialist' | 'manager' | 'admin';
}

export interface Project {
  id: number;
  name: string;
  company_name: string;
  year: number;
  status: ProjectStatus;
  owner_id: number;
  updated_at: string;
}
