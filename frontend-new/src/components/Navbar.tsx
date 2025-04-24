import { useState, useEffect } from 'react';
import { 
  Group, 
  Button, 
  Text, 
  UnstyledButton,
  Box,
  rem,
  Container
} from '@mantine/core';
import { IconUpload, IconUserCircle } from '@tabler/icons-react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import classes from './Navbar.module.css';

const HEADER_HEIGHT = 60;

export function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      const offset = window.scrollY;
      setIsScrolled(offset > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const isActive = (path: string) => location.pathname === path;

  return (
    <Box 
      className={`${classes.navbar} ${isScrolled ? classes.scrolled : ''}`}
      h={HEADER_HEIGHT}
    >
      <Container size="lg">
        <Group justify="space-between" h="100%">
          {/* Logo */}
          <UnstyledButton 
            component={Link}
            to="/"
            className={classes.logo}
            aria-label="Home"
          >
            <img 
              src="/images/WhatsApp Image 2025-04-23 at 16.56.54_a520af8a.jpg" 
              alt="AI Health Logo" 
              height={40}
            />
          </UnstyledButton>

          {/* Navigation Links */}
          <Group gap={40} visibleFrom="xs" className={classes.links}>
            <Text 
              component={Link} 
              to="/" 
              className={`${classes.link} ${isActive('/') ? classes.activeLink : ''}`}
            >
              Home
            </Text>
            <Text 
              component={Link} 
              to="/about" 
              className={`${classes.link} ${isActive('/about') ? classes.activeLink : ''}`}
            >
              About Us
            </Text>
            <Text 
              component={Link} 
              to="/services" 
              className={`${classes.link} ${isActive('/services') ? classes.activeLink : ''}`}
            >
              Services
            </Text>
            <Text 
              component={Link} 
              to="/resources" 
              className={`${classes.link} ${isActive('/resources') ? classes.activeLink : ''}`}
            >
              Resources
            </Text>
          </Group>

          {/* Action Buttons */}
          <Group gap={10}>
            <Button 
              variant="gradient" 
              gradient={{ from: '#00acee', to: '#37B9F1' }}
              className={`${classes.actionButton} ${classes.scanButton}`}
              leftSection={<IconUpload style={{ width: rem(16), height: rem(16) }} />}
              onClick={() => navigate('/scan')}
            >
              Scan Reports
            </Button>
            <Button 
              variant="gradient" 
              gradient={{ from: '#1C7ED6', to: '#4DABF7' }}
              className={`${classes.actionButton} ${classes.loginButton}`}
              leftSection={<IconUserCircle style={{ width: rem(16), height: rem(16) }} />}
              onClick={() => navigate('/login')}
            >
              Login
            </Button>
          </Group>
        </Group>
      </Container>
    </Box>
  );
}