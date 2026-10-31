import { useCallback, useEffect, useState } from 'react';
import { createTask, getInfo, listTasks, removeTask, setDone } from './api.js';

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');
  const [info, setInfo] = useState(null);

  const refresh = useCallback(async () => {
    try {
      setTasks(await listTasks());
      setInfo(await getInfo());
      setError('');
    } catch (err) {
      setError(err.message);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function onSubmit(event) {
    event.preventDefault();
    if (!title.trim()) return;
    try {
      await createTask(title);
      setTitle('');
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="page">
      <h1>Tasks</h1>
      <p className="subtitle">React → FastAPI → PostgreSQL, running on Kubernetes</p>

      <form onSubmit={onSubmit} className="row">
        <input
          aria-label="New task"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs doing?"
        />
        <button type="submit">Add</button>
      </form>

      {error && <p role="alert" className="error">{error}</p>}

      <ul className="list">
        {tasks.map((task) => (
          <li key={task.id} className={task.done ? 'done' : ''}>
            <label>
              <input
                type="checkbox"
                checked={task.done}
                onChange={async () => {
                  await setDone(task.id, !task.done);
                  refresh();
                }}
              />
              <span>{task.title}</span>
            </label>
            <button
              className="ghost"
              aria-label={`Delete ${task.title}`}
              onClick={async () => {
                await removeTask(task.id);
                refresh();
              }}
            >
              ✕
            </button>
          </li>
        ))}
        {tasks.length === 0 && !error && <li className="empty">No tasks yet — add the first one.</li>}
      </ul>

      {info && (
        <footer>
          served by pod <code>{info.pod}</code> · version <code>{info.version}</code>
        </footer>
      )}
    </main>
  );
}
