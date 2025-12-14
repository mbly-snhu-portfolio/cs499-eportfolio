/**
 * Centralized Mantine theme configuration.
 * Ensures consistent styling and proper light/dark mode support across the portfolio.
 */
import { createTheme } from '@mantine/core';

export const theme = createTheme({
  primaryColor: 'blue',
  defaultRadius: 'md',
  
  components: {
    Paper: {
      defaultProps: {
        // Don't force white background, let theme handle it
        bg: undefined,
      },
    },
    
    TypographyStylesProvider: {
      styles: () => ({
        root: {
          '& p': {
            marginTop: '0.75rem',
            marginBottom: '0.75rem',
            lineHeight: 1.6,
          },
          // Remove first/last paragraph extra margin
          '& p:first-of-type': {
            marginTop: 0,
          },
          '& p:last-of-type': {
            marginBottom: 0,
          },
          // Ensure proper spacing for other elements
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
      }),
    },
  },
});
