/**
 * Artifact overview page.
 */
import { Paper, Title, Text, List, Anchor, Divider } from '@mantine/core';

export default function PortfolioArtifact() {
  return (
    <Paper withBorder radius="md" p="md">
      <Title order={2} m={0}>
        Artifact Overview
      </Title>
      <Text c="dimmed" mt={4}>
        One artifact enhanced across software engineering, algorithms/data structures, and databases.
      </Text>

      <Divider my="md" />

      <Title order={3}>What this artifact is</Title>
      <Text>
        This portfolio centers on the <strong>Grazioso Salvare Animal Shelter Dashboard</strong>, originally built as a
        Jupyter Notebook + Dash application (CS-340), and enhanced into a production-style three-tier web app.
      </Text>

      <Title order={3} mt="md">
        Original vs enhanced
      </Title>
      <List>
        <List.Item>
          <strong>Original artifact:</strong> Notebook-based Dash UI with direct MongoDB access.
        </List.Item>
        <List.Item>
          <strong>Enhanced artifact:</strong> FastAPI backend (auth, RBAC, audit logging, rate limiting), React frontend
          (routing, state, charts/maps), caching + trie + fuzzy search, and database indexing/aggregation.
        </List.Item>
      </List>

      <Title order={3} mt="md">
        Where to find everything
      </Title>
      <List>
        <List.Item>
          <strong>Enhanced app:</strong> <code>grazioso-dashboard/</code>
        </List.Item>
        <List.Item>
          <strong>Original reference:</strong> <code>grazioso-dashboard/original/</code>
        </List.Item>
        <List.Item>
          <strong>Narratives & analysis:</strong> <code>grazioso-dashboard/docs/</code>
        </List.Item>
      </List>

      <Title order={3} mt="md">
        Try the dashboard (optional)
      </Title>
      <Text>
        You can open the authenticated dashboard from the header link. The portfolio itself is public and does not
        require login.
      </Text>
      <Text mt="xs">
        <Anchor href="#/app">Open Dashboard App</Anchor>
      </Text>

      <Title order={4} mt="md">
        Demo credentials
      </Title>
      <List>
        <List.Item>
          <strong>Admin:</strong> admin / admin123
        </List.Item>
        <List.Item>
          <strong>User:</strong> user / user123
        </List.Item>
      </List>
    </Paper>
  );
}
