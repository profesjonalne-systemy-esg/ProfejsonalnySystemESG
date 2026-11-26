import { ApiError, tokenStore } from '../../api/client';
import type { DocumentItem } from './types';

export async function uploadFiles(projectId: string, files: File[]): Promise<DocumentItem[]> {
  const form = new FormData();
  files.forEach((file) => form.append('files', file));
  const token = tokenStore.get();
  const response = await fetch(`/api/projects/${projectId}/documents`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    body: form,
  }).catch(() => {
    throw new ApiError(0, 'Brak połączenia z serwerem.');
  });
  const body = (await response.json().catch(() => null)) as { detail?: unknown } | DocumentItem[] | null;
  if (response.ok) return body as DocumentItem[];
  const detail = body && !Array.isArray(body) ? body.detail : null;
  throw new ApiError(response.status, typeof detail === 'string' ? detail : 'Nie udało się wgrać plików.');
}
