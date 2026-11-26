import { useCallback, useEffect, useState } from 'react';
import { api } from './client';

interface State<T> {
  path: string | null;
  data: T | null;
  error: string | null;
}

/** Pobiera dane z GET /api{path}. `null` oznacza: jeszcze nie pobieraj. */
export function useApi<T>(path: string | null) {
  const [state, setState] = useState<State<T>>({ path: null, data: null, error: null });
  const [version, setVersion] = useState(0);

  useEffect(() => {
    if (path === null) return;
    let active = true;
    api<T>(path)
      .then((data) => {
        if (active) setState({ path, data, error: null });
      })
      .catch((err: unknown) => {
        if (active) setState({ path, data: null, error: err instanceof Error ? err.message : 'Błąd' });
      });
    return () => {
      active = false;
    };
  }, [path, version]);

  const reload = useCallback(() => setVersion((v) => v + 1), []);
  const ready = path !== null && state.path === path;
  return { data: ready ? state.data : null, error: ready ? state.error : null, loading: path !== null && !ready, reload };
}
