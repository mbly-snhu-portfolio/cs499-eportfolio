import { describe, it, afterEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import App from './App';
import { theme } from './theme';

describe('App', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('renders without crashing', async () => {
    // Avoid act() warnings by ensuring async markdown loads complete within the test.
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => ({
        ok: true,
        text: async () => '# Loaded\n\nTest content.',
      }))
    );

    render(
      <MantineProvider theme={theme} defaultColorScheme="auto">
        <App />
      </MantineProvider>
    );

    // Content comes from the markdown fetch above.
    await screen.findByText('Loaded');
  });
});

