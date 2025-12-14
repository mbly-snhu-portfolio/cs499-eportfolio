/**
 * Fetches a markdown file from the public/ directory.
 */
import { useEffect, useState } from 'react';

function buildAssetUrl(assetPath) {
  const base = import.meta.env.BASE_URL || '/';
  const normalizedBase = base.endsWith('/') ? base : `${base}/`;
  const normalizedPath = assetPath.startsWith('/') ? assetPath.slice(1) : assetPath;
  return `${normalizedBase}${normalizedPath}`;
}

export default function useMarkdownAsset(assetPath) {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setLoading(true);
        setError(null);

        const url = buildAssetUrl(assetPath);
        const res = await fetch(url, { cache: 'no-cache' });

        if (!res.ok) {
          throw new Error(`Failed to load ${assetPath} (${res.status})`);
        }

        const text = await res.text();
        if (!cancelled) {
          setContent(text);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e);
          setContent('');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    if (!assetPath) {
      setLoading(false);
      setError(new Error('No assetPath provided'));
      return () => {
        cancelled = true;
      };
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [assetPath]);

  return { content, loading, error };
}
