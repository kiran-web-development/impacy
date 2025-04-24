import {
  Container,
  Group,
  ActionIcon,
  rem,
  Text,
  Stack,
  SimpleGrid,
  Title,
} from '@mantine/core';
import {
  IconBrandTwitter,
  IconBrandLinkedin,
  IconBrandInstagram,
  IconBrandFacebook,
  IconMail,
  IconPhone,
  IconMapPin,
} from '@tabler/icons-react';
import classes from './Footer.module.css';

const socialLinks = [
  { icon: IconBrandTwitter, link: 'https://twitter.com/medscan_ai' },
  { icon: IconBrandLinkedin, link: 'https://linkedin.com/company/medscan-ai' },
  { icon: IconBrandInstagram, link: 'https://instagram.com/medscan.ai' },
  { icon: IconBrandFacebook, link: 'https://facebook.com/medscanai' },
];

const quickLinks = [
  { label: 'About Us', link: '/about' },
  { label: 'Services', link: '/services' },
  { label: 'Resources', link: '/resources' },
  { label: 'Contact', link: '/contact' },
  { label: 'Privacy Policy', link: '/privacy' },
  { label: 'Terms of Service', link: '/terms' },
];

export function Footer() {
  return (
    <footer className={classes.footer}>
      <Container size="lg" py="xl">
        <SimpleGrid cols={{ base: 1, sm: 2, md: 4 }} spacing={50}>
          {/* Company Info */}
          <Stack gap="xs">
            <Title order={4} className={classes.title}>MedScan.AI</Title>
            <Text size="sm" c="dimmed">
              Revolutionizing medical diagnostics through advanced AI technology and image analysis.
            </Text>
            <Group gap="xs" mt="md">
              {socialLinks.map((link, index) => (
                <ActionIcon
                  key={index}
                  size="lg"
                  variant="subtle"
                  color="blue"
                  component="a"
                  href={link.link}
                  target="_blank"
                >
                  <link.icon style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
                </ActionIcon>
              ))}
            </Group>
          </Stack>

          {/* Quick Links */}
          <Stack gap="xs">
            <Title order={4} className={classes.title}>Quick Links</Title>
            {quickLinks.map((link, index) => (
              <Text
                key={index}
                component="a"
                href={link.link}
                className={classes.link}
              >
                {link.label}
              </Text>
            ))}
          </Stack>

          {/* Contact Info */}
          <Stack gap="xs">
            <Title order={4} className={classes.title}>Contact Us</Title>
            <Group gap="xs">
              <IconMail size={16} />
              <Text size="sm">contact@medscan.ai</Text>
            </Group>
            <Group gap="xs">
              <IconPhone size={16} />
              <Text size="sm">+1 (555) 123-4567</Text>
            </Group>
            <Group gap="xs">
              <IconMapPin size={16} />
              <Text size="sm">123 Medical Center Drive<br />Silicon Valley, CA 94025</Text>
            </Group>
          </Stack>

          {/* Newsletter */}
          <Stack gap="xs">
            <Title order={4} className={classes.title}>Newsletter</Title>
            <Text size="sm" c="dimmed">
              Subscribe to our newsletter to stay updated with the latest innovations in medical AI.
            </Text>
            <form className={classes.form}>
              <input
                type="email"
                placeholder="Your email"
                className={classes.input}
                aria-label="Newsletter subscription input"
              />
              <button type="submit" className={classes.button}>
                Subscribe
              </button>
            </form>
          </Stack>
        </SimpleGrid>

        <div className={classes.afterFooter}>
          <Text c="dimmed" size="sm">
            © 2025 MedScan.AI. All rights reserved.
          </Text>
          <Text c="dimmed" size="sm">
            Made with ❤️ for better healthcare
          </Text>
        </div>
      </Container>
    </footer>
  );
}