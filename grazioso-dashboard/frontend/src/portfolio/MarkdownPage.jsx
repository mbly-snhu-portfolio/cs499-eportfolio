/**
 * Markdown-backed portfolio page.
 *
 * Markdown files are served from frontend/public/ (GitHub Pages friendly).
 */
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Alert, Button, Code, Group, Paper, ScrollArea, Text, Title } from '@mantine/core';

import useMarkdownAsset from './useMarkdownAsset';
import './PortfolioLayout.css';

function CodeBlock({ inline, children, ...props }) {
  if (inline) {
    return <Code {...props}>{children}</Code>;
  }

  return (
    <ScrollArea type="auto" offsetScrollbars>
      <pre className="portfolio-codeBlock">
        <code {...props}>{children}</code>
      </pre>
    </ScrollArea>
  );
}

export default function MarkdownPage({ title, assetPath, pdfPath }) {
  const { content, loading, error } = useMarkdownAsset(assetPath);

  return (
    <Paper withBorder radius="md" p="md">
      <Group justify="space-between" align="flex-start" mb="sm">
        <Title order={2} m={0}>
          {title}
        </Title>
        {pdfPath ? (
          <Button component="a" href={pdfPath} target="_blank" rel="noreferrer" variant="light">
            Open PDF
          </Button>
        ) : null}
      </Group>

      {loading ? <Text c="dimmed">Loading…</Text> : null}

      {error ? (
        <Alert color="red" title="Could not load portfolio content">
          {String(error?.message || error)}
        </Alert>
      ) : null}

      {!loading && !error ? (
        <div className="portfolio-markdown">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              code: CodeBlock,
              a({ children, ...props }) {
                return (
                  <a {...props} target="_blank" rel="noreferrer">
                    {children}
                  </a>
                );
              },
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      ) : null}
    </Paper>
  );
}
