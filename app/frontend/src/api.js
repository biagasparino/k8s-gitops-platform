// All calls use relative URLs: in Kubernetes the Ingress routes /api to the backend,
// and in local dev Vite proxies /api to FastAPI. No hard-coded hosts, so the same
// image runs unchanged in dev, staging and prod.
async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`Request failed (${response.status})`);
  }
  return response.status === 204 ? null : response.json();
}

export const listTasks = () => request('/api/tasks');
export const createTask = (title) =>
  request('/api/tasks', { method: 'POST', body: JSON.stringify({ title }) });
export const setDone = (id, done) =>
  request(`/api/tasks/${id}`, { method: 'PATCH', body: JSON.stringify({ done }) });
export const removeTask = (id) => request(`/api/tasks/${id}`, { method: 'DELETE' });
export const getInfo = () => request('/api/info');
