/**
 * Artifact overview page.
 */
import {
  Container,
  Paper,
  Title,
  Text,
  List,
  ThemeIcon,
  Stack,
  Code,
  Anchor,
  Alert,
} from '@mantine/core';
import { IconCircleCheck, IconCode, IconLock, IconUser } from '@tabler/icons-react';

export default function PortfolioArtifact() {
  const dashboardQuickStartUrl =
    'https://github.com/mbly-snhu-portfolio/cs499-eportfolio/tree/main/grazioso-dashboard#quick-start';

  return (
    <Container size="lg" p={0}>
      <Stack gap="lg">
        <Paper withBorder radius="md" p="xl" shadow="xs">
          <Title order={1} size="h2" mb="lg">
            Artifact Overview
          </Title>

          <Stack gap="md">
            <div>
              <Title order={2} size="h3" mb="sm">
                What this artifact is
              </Title>
              <Text>
                This portfolio centers on the <strong>Grazioso Salvare Animal Shelter Dashboard</strong>, originally
                built as a Jupyter Notebook + Dash application (CS-340), and enhanced into a production-style
                three-tier web app.
              </Text>
            </div>

            <div>
              <Title order={2} size="h3" mb="sm">
                Original vs enhanced
              </Title>
              <List
                spacing="sm"
                icon={
                  <ThemeIcon color="blue" size={24} radius="xl">
                    <IconCircleCheck size={16} />
                  </ThemeIcon>
                }
              >
                <List.Item>
                  <strong>Original artifact:</strong> Notebook-based Dash UI with direct MongoDB access.
                </List.Item>
                <List.Item>
                  <strong>Enhanced artifact:</strong> FastAPI backend (auth, RBAC, audit logging, rate limiting),
                  React frontend (routing, state, charts/maps), caching + trie + fuzzy search, and database
                  indexing/aggregation.
                </List.Item>
              </List>
            </div>

            <div>
              <Title order={2} size="h3" mb="sm">
                Where to find everything
              </Title>
              <List spacing="sm">
                <List.Item>
                  <strong>Enhanced app:</strong> <Code>grazioso-dashboard/</Code>
                </List.Item>
                <List.Item>
                  <strong>Original reference:</strong> <Code>grazioso-dashboard/original/</Code>
                </List.Item>
                <List.Item>
                  <strong>Narratives & analysis:</strong> <Code>grazioso-dashboard/docs/</Code>
                </List.Item>
              </List>
            </div>

            <Alert
              variant="light"
              color="cyan"
              title="Try the dashboard (optional, local-only)"
              icon={<IconCode size={18} />}
              mt="md"
            >
              <Text size="sm" mb="xs">
                The dashboard requires running the backend locally (and typically MongoDB/Redis). The GitHub Pages site
                hosts the portfolio only.
              </Text>
              <Anchor href={dashboardQuickStartUrl} target="_blank" rel="noreferrer" size="sm">
                View local setup instructions (Quick Start)
              </Anchor>
              <Title order={4} size="h6" mb="xs">
                Demo credentials
              </Title>
              <List size="sm" spacing={4}>
                <List.Item icon={<IconUser size={14} />}>
                  <strong>Admin:</strong> admin / admin123
                </List.Item>
                <List.Item icon={<IconLock size={14} />}>
                  <strong>User:</strong> user / user123
                </List.Item>
              </List>
            </Alert>

            <div>
              <Title order={2} size="h3" mb="sm">
                Repository
              </Title>
              <Anchor
                href="https://github.com/mbly-snhu-portfolio/cs499-eportfolio"
                target="_blank"
                rel="noreferrer"
                size="sm"
              >
                View full source code on GitHub
              </Anchor>
            </div>
          </Stack>
        </Paper>
      </Stack>
    </Container>
  );
}
