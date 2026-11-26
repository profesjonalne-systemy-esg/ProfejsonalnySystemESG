import { CloudUpload } from 'lucide-react';
import { useRef, useState, type DragEvent } from 'react';
import { ACCEPTED } from './types';

interface Props {
  disabled: boolean;
  onFiles: (files: File[]) => void;
}

export function Dropzone({ disabled, onFiles }: Props) {
  const input = useRef<HTMLInputElement>(null);
  const [over, setOver] = useState(false);

  const send = (list: FileList | null) => {
    if (!disabled && list?.length) onFiles([...list]);
  };
  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setOver(false);
    send(e.dataTransfer.files);
  };

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setOver(true);
      }}
      onDragLeave={() => setOver(false)}
      onDrop={handleDrop}
      className={`flex flex-col items-center rounded-xl border-2 border-dashed px-6 py-12 text-center transition ${
        over ? 'border-brand bg-brand-soft' : 'border-slate-300 bg-white'
      }`}
    >
      <span className="flex h-14 w-14 items-center justify-center rounded-xl bg-brand-soft text-brand">
        <CloudUpload className="h-7 w-7" aria-hidden />
      </span>
      <p className="mt-4 font-semibold text-slate-800">Przeciągnij i upuść pliki tutaj</p>
      <p className="mt-1 text-sm text-slate-500">PDF, XLSX, DOCX, TXT, do 25 MB każdy. Możesz wybrać wiele plików.</p>
      <button
        type="button"
        disabled={disabled}
        onClick={() => input.current?.click()}
        className="mt-5 cursor-pointer rounded-lg bg-brand px-5 py-2.5 font-semibold text-white transition hover:bg-brand-dark disabled:cursor-wait disabled:opacity-60"
      >
        {disabled ? 'Wgrywanie…' : 'Wybierz pliki'}
      </button>
      <input
        ref={input}
        type="file"
        multiple
        hidden
        accept={ACCEPTED.join(',')}
        onChange={(e) => {
          send(e.target.files);
          e.target.value = '';
        }}
      />
    </div>
  );
}
