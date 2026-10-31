import { render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';
import App from '../App.jsx';

afterEach(() => vi.restoreAllMocks());

test('renders tasks returned by the API and the serving pod', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn((url) =>
      Promise.resolve({
        ok: true,
        status: 200,
        json: () =>
          Promise.resolve(
            url === '/api/info'
              ? { pod: 'tasks-api-abc12', version: '1.2.3' }
              : [{ id: 1, title: 'learn kubernetes', done: false, created_at: '2026-01-01T00:00:00Z' }]
          ),
      })
    )
  );

  render(<App />);

  await waitFor(() => expect(screen.getByText('learn kubernetes')).toBeTruthy());
  expect(screen.getByText('tasks-api-abc12')).toBeTruthy();
});

test('shows an error message when the API is unreachable', async () => {
  vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({ ok: false, status: 503, json: () => Promise.resolve({}) })));

  render(<App />);

  await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('503'));
});
