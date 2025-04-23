import { MantineProvider, AppShell, Button, Group, Title, Container, Image, Paper, Text, Progress, rem } from '@mantine/core';
import { Dropzone } from '@mantine/dropzone';
import { IconUpload, IconPhoto, IconX, IconCheck } from '@tabler/icons-react';
import { useState, useRef } from 'react';
import classes from './App.module.css';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (files: File[]) => {
    const uploadedFile = files[0];
    setFile(uploadedFile);
    const url = URL.createObjectURL(uploadedFile);
    setPreviewUrl(url);
    setResults(null);
    
    // Simulate upload progress
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      setUploadProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
        setTimeout(() => setUploadProgress(0), 500);
      }
    }, 100);
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setAnalyzing(true);
    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error analyzing image:', error);
      setResults({ error: 'Failed to analyze image' });
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <MantineProvider>
      <AppShell
        header={{ height: 60 }}
        padding="md"
      >
        <AppShell.Header style={{ background: '#1a1b1e' }}>
          <Container size="lg" h="100%">
            <Group justify="space-between" h="100%">
              <Title order={1} size="h3" c="white">
                Medical Image Analysis System
              </Title>
              <Button
                variant="filled"
                color="blue"
                leftSection={<IconUpload style={{ width: rem(16), height: rem(16) }} />}
                onClick={() => fileInputRef.current?.click()}
              >
                Scan Report
              </Button>
            </Group>
          </Container>
        </AppShell.Header>

        <AppShell.Main>
          <Container size="lg">
            <Paper shadow="sm" p="xl" withBorder>
              <input 
                type="file"
                ref={fileInputRef}
                className={classes.hiddenInput}
                onChange={(e) => e.target.files && handleDrop([e.target.files[0]])}
                accept="image/*,.dcm"
                aria-label="Upload medical image"
                title="Upload medical image"
              />
              <Dropzone
                onDrop={handleDrop}
                accept={['image/*', '.dcm']}
                maxSize={5 * 1024 * 1024}
                multiple={false}
                styles={{
                  root: { minHeight: previewUrl ? 'auto' : 200 }
                }}
              >
                <Group justify="center" gap="xl" style={{ minHeight: 100, pointerEvents: 'none' }}>
                  {!previewUrl ? (
                    <>
                      <Dropzone.Accept>
                        <IconCheck style={{ width: rem(52), height: rem(52) }} stroke="1.5" />
                      </Dropzone.Accept>
                      <Dropzone.Reject>
                        <IconX style={{ width: rem(52), height: rem(52) }} stroke="1.5" />
                      </Dropzone.Reject>
                      <Dropzone.Idle>
                        <IconUpload style={{ width: rem(52), height: rem(52) }} stroke="1.5" />
                      </Dropzone.Idle>
                      <div>
                        <Text size="xl">
                          Drag medical images here or click to select
                        </Text>
                        <Text size="sm" c="dimmed" mt={7}>
                          Attach one file up to 5MB in size
                        </Text>
                      </div>
                    </>
                  ) : (
                    <Text size="sm" c="dimmed">
                      Drop a new image to replace the current one
                    </Text>
                  )}
                </Group>
              </Dropzone>

              {uploadProgress > 0 && uploadProgress < 100 && (
                <Progress 
                  value={uploadProgress} 
                  mt="md"
                  size="sm"
                  radius="xl"
                  animated
                />
              )}

              {previewUrl && (
                <Paper shadow="sm" p="md" mt="md" withBorder>
                  <Image
                    src={previewUrl}
                    alt="Preview"
                    fit="contain"
                    h={400}
                  />
                  <Group justify="center" mt="md">
                    <Button
                      onClick={handleAnalyze}
                      loading={analyzing}
                      leftSection={<IconPhoto style={{ width: rem(16), height: rem(16) }} />}
                      variant="filled"
                      color="blue"
                    >
                      {analyzing ? 'Analyzing...' : 'Analyze Image'}
                    </Button>
                  </Group>
                </Paper>
              )}

              {results && (
                <Paper shadow="sm" p="md" mt="md" withBorder className={classes.results}>
                  <Title order={2} size="h4" mb="md">Analysis Results</Title>
                  <pre>
                    {JSON.stringify(results, null, 2)}
                  </pre>
                </Paper>
              )}
            </Paper>
          </Container>
        </AppShell.Main>
      </AppShell>
    </MantineProvider>
  );
}

export default App;
