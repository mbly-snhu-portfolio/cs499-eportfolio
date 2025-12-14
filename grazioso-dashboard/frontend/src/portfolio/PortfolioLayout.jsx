/**
 * Public ePortfolio layout (no login required).
 */
import { NavLink as RouterNavLink, Outlet } from 'react-router-dom';
import { AppShell, NavLink, Group, Title, Text, Button, Stack, Divider, Anchor } from '@mantine/core';
import {
  IconFileText,
  IconCode,
  IconChartBar,
  IconDatabase,
  IconLayout,
  IconChecklist,
  IconExternalLink,
} from '@tabler/icons-react';

function NavItem({ to, children, icon }) {
  return (
    <NavLink
      component={RouterNavLink}
      to={to}
      end
      label={children}
      leftSection={icon}
      styles={{
        root: {
          borderRadius: '8px',
          fontWeight: 500,
        },
      }}
    />
  );
}

export default function PortfolioLayout() {
  return (
    <AppShell
      header={{ height: 70 }}
      navbar={{ width: 300, breakpoint: 'sm' }}
      padding="xl"
      styles={{
        main: {
          background: 'var(--mantine-color-gray-0)',
        },
      }}
    >
      <AppShell.Header>
        <Group h="100%" px="xl" justify="space-between" wrap="nowrap">
          <div>
            <Title order={2} size="h3" mb={2}>
              CS 499 ePortfolio
            </Title>
            <Text size="sm" c="dimmed" style={{ lineHeight: 1.2 }}>
              Grazioso Salvare: Animal Shelter Dashboard
            </Text>
          </div>
          <Button component="a" href="#/app" variant="gradient" gradient={{ from: 'blue', to: 'cyan' }}>
            Open Dashboard App
          </Button>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <Stack gap="xs">
          <Text size="xs" tt="uppercase" fw={700} c="dimmed" mb="xs">
            Overview
          </Text>
          <NavItem to="/" icon={<IconFileText size={18} stroke={1.5} />}>
            Professional Self-Assessment
          </NavItem>
          <NavItem to="/artifact" icon={<IconLayout size={18} stroke={1.5} />}>
            Artifact Overview
          </NavItem>
          <NavItem to="/artifact-narrative" icon={<IconFileText size={18} stroke={1.5} />}>
            Artifact Narrative
          </NavItem>

          <Divider my="md" />

          <Text size="xs" tt="uppercase" fw={700} c="dimmed" mb="xs">
            Enhancements
          </Text>
          <NavItem to="/enhancements/software" icon={<IconCode size={18} stroke={1.5} />}>
            Software Design & Engineering
          </NavItem>
          <NavItem to="/enhancements/algorithms" icon={<IconChartBar size={18} stroke={1.5} />}>
            Algorithms & Data Structures
          </NavItem>
          <NavItem to="/enhancements/databases" icon={<IconDatabase size={18} stroke={1.5} />}>
            Databases
          </NavItem>

          <Divider my="md" />

          <Text size="xs" tt="uppercase" fw={700} c="dimmed" mb="xs">
            Documentation
          </Text>
          <NavItem to="/code-review" icon={<IconCode size={18} stroke={1.5} />}>
            Code Review (Written)
          </NavItem>
          <NavItem to="/rubric-evidence" icon={<IconChecklist size={18} stroke={1.5} />}>
            Rubric Evidence Map
          </NavItem>

          <Divider my="md" />

          <Anchor href="https://github.com/mbly-snhu-portfolio/cs499-eportfolio" target="_blank" rel="noreferrer" size="sm" c="dimmed">
            <Group gap={6}>
              View on GitHub
              <IconExternalLink size={14} stroke={1.5} />
            </Group>
          </Anchor>
        </Stack>
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
