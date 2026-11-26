import { Building2 } from 'lucide-react';

/** dark: wersja na granatowe tło panelu bocznego */
export function Logo({ dark = false }: { dark?: boolean }) {
  return (
    <span className="inline-flex items-center gap-3">
      <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand text-white shadow-lg shadow-brand/25">
        <Building2 className="h-6 w-6" aria-hidden />
      </span>
      <span className={`text-2xl font-bold tracking-tight ${dark ? 'text-white' : 'text-navy'}`}>
        Build<span className={dark ? 'text-brand-light' : 'text-brand'}>ESG</span>
      </span>
    </span>
  );
}
