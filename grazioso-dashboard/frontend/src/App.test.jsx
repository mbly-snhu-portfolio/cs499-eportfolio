import { describe, it } from 'vitest';
import { render } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import App from './App';
import { theme } from './theme';

describe('App', () => {
  it('renders without crashing', () => {
    render(
      <MantineProvider theme={theme} defaultColorScheme="auto">
        <App />
      </MantineProvider>
    );
  });
});

