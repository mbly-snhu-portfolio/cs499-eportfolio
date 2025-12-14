/**
 * Markdown-backed portfolio page.
 *
 * Markdown files are served from frontend/public/ (GitHub Pages friendly).
 */
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  Alert,
  Button,
  Code,
  Container,
  Group,
  Paper,
  ScrollArea,
  Stack,
  Text,
  Title,
  TypographyStylesProvider,
} from '@mantine/core';
import { IconFileTypePdf } from '@tabler/icons-react';

import useMarkdownAsset from './useMarkdownAsset';

function CodeBlock({ inline, children, ...props }) {
  if (inline) {
    return <Code {...props}>{children}</Code>;
  }

  return (
    <ScrollArea type="auto" offsetScrollbars>
      <Paper 
        withBorder 
        radius="md" 
        p="sm" 
        style={{ 
          marginTop: '0.75rem', 
          marginBottom: '0.75rem',
          backgroundColor: 'light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))',
        }}
      >
        <code
          style={{
            fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
            fontSize: '0.9rem',
            color: 'light-dark(var(--mantine-color-gray-9), var(--mantine-color-gray-1))',
            display: 'block',
            whiteSpace: 'pre',
          }}
          {...props}
        >
          {children}
        </code>
      </Paper>
    </ScrollArea>
  );
}

export default function MarkdownPage({ title, assetPath, pdfPath }) {
  const { content, loading, error } = useMarkdownAsset(assetPath);

  return (
    <Container size="lg" p={0}>
      <Stack gap="lg">
        <Paper withBorder radius="md" p="xl" shadow="xs">
          <Group justify="space-between" align="flex-start" mb="lg" wrap="nowrap">
            <Title order={1} size="h2">
              {title}
            </Title>
            {pdfPath ? (
              <Button
                component="a"
                href={pdfPath}
                target="_blank"
                rel="noreferrer"
                variant="light"
                leftSection={<IconFileTypePdf size={18} />}
              >
                Open PDF
              </Button>
            ) : null}
          </Group>

          {loading ? <Text c="dimmed">Loading content...</Text> : null}

          {error ? (
            <Alert color="red" title="Could not load portfolio content" variant="light">
              {String(error?.message || error)}
            </Alert>
          ) : null}

          {!loading && !error ? (
            <TypographyStylesProvider
              styles={{
                root: {
                  '& p': {
                    marginTop: '0.75rem',
                    marginBottom: '0.75rem',
                    lineHeight: 1.6,
                  },
                  '& p:first-of-type': { 
                    marginTop: 0 
                  },
                  '& p:last-of-type': { 
                    marginBottom: 0 
                  },
                  '& h1, & h2, & h3, & h4, & h5, & h6': {
                    marginTop: '1.5rem',
                    marginBottom: '0.75rem',
                  },
                  '& h1:first-of-type, & h2:first-of-type, & h3:first-of-type': {
                    marginTop: 0,
                  },
                  '& ul, & ol': {
                    marginTop: '0.75rem',
                    marginBottom: '0.75rem',
                  },
                  '& li': {
                    marginTop: '0.25rem',
                    marginBottom: '0.25rem',
                  },
                },
              }}
            >
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code: CodeBlock,
                  a({ children, href, ...props }) {
                    return (
                      <a href={href} target="_blank" rel="noreferrer" {...props}>
                        {children}
                      </a>
                    );
                  },
                }}
              >
                {content}
              </ReactMarkdown>
            </TypographyStylesProvider>
          ) : null}
        </Paper>
      </Stack>
    </Container>
  );
}
