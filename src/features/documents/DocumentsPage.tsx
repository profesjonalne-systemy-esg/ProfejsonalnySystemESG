import { FileText } from 'lucide-react';
import { useState } from 'react';
import { useParams } from 'react-router';
import { useApi } from '../../api/useApi';
import { Dropzone } from './Dropzone';
import { STATUS_LABELS, type DocumentItem } from './types';
import { uploadFiles } from './upload';

function fileSize(bytes: number | null): string {
  if (bytes === null) return '';
  if (bytes < 1024) return `${bytes} B`;
  const kb = bytes / 1024;
  return kb < 1024 ? `${Math.round(kb)} KB` : `${(kb / 1024).toLocaleString('pl-PL', { maximumFractionDigits: 1 })} MB`;
}

export function DocumentsPage() {
  const { projectId = '' } = useParams();
  const { data, error: loadError, loading, reload } = useApi<DocumentItem[]>(`/projects/${projectId}/documents`);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFiles = async (files: File[]) => {
    setUploading(true);
    setError(null);
    try {
      await uploadFiles(projectId, files);
      reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Nie udało się wgrać plików.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mx-auto max-w-5xl p-6 md:p-10">
      <h1 className="text-3xl font-bold tracking-tight text-navy">Dokumenty źródłowe</h1>
      <p className="mt-2 mb-6 text-slate-500">Wgraj faktury, karty odpadów, statystyki BHP i dane kadrowe.</p>
      <Dropzone disabled={uploading} onFiles={handleFiles} />
      {(error ?? loadError) && (
        <p role="alert" className="mt-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
          {error ?? loadError}
        </p>
      )}
      <ul className="mt-6 divide-y divide-slate-100 rounded-xl border border-slate-200 bg-white">
        {loading && <li className="p-5 text-slate-500">Wczytywanie…</li>}
        {data?.length === 0 && <li className="p-5 text-slate-500">Nie ma jeszcze żadnych dokumentów.</li>}
        {data?.map((doc) => (
          <li key={doc.id} className="flex items-center gap-4 p-4">
            <FileText className="h-5 w-5 shrink-0 text-slate-400" aria-hidden />
            <span className="min-w-0 grow truncate font-medium">{doc.filename}</span>
            <span className="text-sm text-slate-500">{fileSize(doc.size_bytes)}</span>
            <span className="rounded-full bg-brand-soft px-3 py-1 text-xs font-bold text-brand-dark">
              {STATUS_LABELS[doc.status]}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
