import { describe, it } from 'vitest';
import { render } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import App from './App';

describe('App', () => {
  it('renders without crashing', () => {
    render(
      <MantineProvider defaultColorScheme="auto">
        <App />
      </MantineProvider>
    );
  });
});

