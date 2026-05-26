import { useEffect, useState } from "react";

export type RequestState<T> = {
  data: T | null;
  loading: boolean;
  error: string | null;
  retryCount: number;
  reload: () => void;
};

export function useAsyncResource<T>(loader: () => Promise<T>): RequestState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [nonce, setNonce] = useState(0);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    let cancelled = false;

    setLoading(true);
    setError(null);

    loader()
      .then((value) => {
        if (!cancelled) setData(value);
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Request failed");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [nonce]);

  return {
    data,
    loading,
    error,
    retryCount,
    reload: () => {
      setRetryCount((count) => count + 1);
      setNonce((value) => value + 1);
    }
  };
}
