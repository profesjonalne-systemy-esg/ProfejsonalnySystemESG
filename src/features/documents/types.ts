export interface DocumentItem {
  id: number;
  filename: string;
  status: 'uploaded' | 'processing' | 'processed' | 'failed';
  size_bytes: number | null;
  error: string | null;
  uploaded_at: string;
}

export const STATUS_LABELS: Record<DocumentItem['status'], string> = {
  uploaded: 'Wgrany',
  processing: 'Przetwarzanie',
  processed: 'Przetworzony',
  failed: 'Błąd',
};

export const ACCEPTED = ['.pdf', '.xlsx', '.docx', '.txt'];
