/**
 * Public ePortfolio layout (no login required).
 */
import { NavLink, Outlet } from 'react-router-dom';
import { AppShell, Group, Title, Text, Button, Stack, Divider } from '@mantine/core';
import './PortfolioLayout.css';

function NavItem({ to, children }) {
  return (
    <NavLink
      to={to}
      end
      className={({ isActive }) => `portfolio-navLink ${isActive ? 'is-active' : ''}`}
    >
      {children}
    </NavLink>
  );
}

export default function PortfolioLayout() {
  return (
    <AppShell
      header={{ height: 72 }}
      navbar={{ width: 320, breakpoint: 'sm' }}
      padding="md"
    >
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <div>
            <Title order={3}>CS 499 ePortfolio</Title>
            <Text size="sm" c="dimmed">
              Grazioso Salvare: Animal Shelter Dashboard (Enhanced)
            </Text>
          </div>
          <Button component="a" href="#/app" variant="light">
            Open Dashboard App
          </Button>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <Stack gap="xs">
          <Text size="xs" tt="uppercase" fw={700} c="dimmed">
            Portfolio
          </Text>
          <NavItem to="/">Professional Self-Assessment</NavItem>
          <NavItem to="/artifact">Artifact Overview</NavItem>
          <NavItem to="/code-review">Informal Code Review</NavItem>
          <NavItem to="/artifact-narrative">Artifact Narrative (Overall)</NavItem>
          <NavItem to="/rubric-evidence">Rubric Evidence Map</NavItem>

          <Divider my="sm" />

          <Text size="xs" tt="uppercase" fw={700} c="dimmed">
            Enhancement Narratives
          </Text>
          <NavItem to="/enhancements/software">Software Design & Engineering</NavItem>
          <NavItem to="/enhancements/algorithms">Algorithms & Data Structures</NavItem>
          <NavItem to="/enhancements/databases">Databases</NavItem>

          <Divider my="sm" />

          <Text size="xs" tt="uppercase" fw={700} c="dimmed">
            Repository
          </Text>
          <Button component="a" href="./" target="_blank" rel="noreferrer" variant="subtle" justify="flex-start" p={0}>
            View Site Root
          </Button>
        </Stack>
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
