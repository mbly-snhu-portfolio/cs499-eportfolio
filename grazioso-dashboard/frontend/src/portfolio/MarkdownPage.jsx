/**
 * Markdown-backed portfolio page.
 *
 * Markdown files are served from frontend/public/ (GitHub Pages friendly).
 */
import useMarkdownAsset from './useMarkdownAsset';
import './PortfolioLayout.css';

function escapeHtml(text) {
  return text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function markdownToHtml(md) {
  // Intentionally minimal: headings, paragraphs, lists, code fences.
  // This avoids bringing in a new dependency just to render portfolio content.
  const lines = md.split(/\r?\n/);
  let html = '';
  let inCode = false;
  let inList = false;

  for (const rawLine of lines) {
    const line = rawLine ?? '';

    if (line.startsWith('```')) {
      if (!inCode) {
        if (inList) {
          html += '</ul>';
          inList = false;
        }
        inCode = true;
        html += '<pre><code>';
      } else {
        inCode = false;
        html += '</code></pre>';
      }
      continue;
    }

    if (inCode) {
      html += `${escapeHtml(line)}\n`;
      continue;
    }

    const h3 = line.match(/^###\s+(.+)$/);
    const h2 = line.match(/^##\s+(.+)$/);
    const h1 = line.match(/^#\s+(.+)$/);
    const li = line.match(/^-\s+(.+)$/);

    if (h3) {
      if (inList) {
        html += '</ul>';
        inList = false;
      }
      html += `<h3>${escapeHtml(h3[1])}</h3>`;
      continue;
    }

    if (h2) {
      if (inList) {
        html += '</ul>';
        inList = false;
      }
      html += `<h2>${escapeHtml(h2[1])}</h2>`;
      continue;
    }

    if (h1) {
      if (inList) {
        html += '</ul>';
        inList = false;
      }
      html += `<h1>${escapeHtml(h1[1])}</h1>`;
      continue;
    }

    if (li) {
      if (!inList) {
        html += '<ul>';
        inList = true;
      }
      html += `<li>${escapeHtml(li[1])}</li>`;
      continue;
    }

    if (line.trim() === '') {
      if (inList) {
        html += '</ul>';
        inList = false;
      }
      continue;
    }

    if (inList) {
      html += '</ul>';
      inList = false;
    }

    html += `<p>${escapeHtml(line)}</p>`;
  }

  if (inList) {
    html += '</ul>';
  }

  if (inCode) {
    html += '</code></pre>';
  }

  return html;
}

export default function MarkdownPage({ title, assetPath, pdfPath }) {
  const { content, loading, error } = useMarkdownAsset(assetPath);

  return (
    <div className="portfolio-doc">
      <div className="portfolio-docHeader">
        <h1 className="portfolio-title">{title}</h1>
        <div className="portfolio-actions">
          {pdfPath && (
            <a className="portfolio-btn" href={pdfPath} target="_blank" rel="noreferrer">
              Open PDF
            </a>
          )}
        </div>
      </div>

      {loading && <div className="portfolio-note">Loading…</div>}

      {error && (
        <div className="portfolio-error">
          Could not load portfolio content. {String(error?.message || error)}
        </div>
      )}

      {!loading && !error && (
        <div
          className="portfolio-markdown"
          // Portfolio content is authored by you and served locally.
          // We still escape HTML and render a limited markdown subset.
          dangerouslySetInnerHTML={{ __html: markdownToHtml(content) }}
        />
      )}
    </div>
  );
}
