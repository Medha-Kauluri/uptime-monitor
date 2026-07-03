import { useCallback, useEffect, useState } from "react";
import { addUrl, fetchUrls } from "./api";
import "./App.css";

const REFRESH_INTERVAL_MS = 5000;

function StatusBadge({ status }) {
  const className = {
    UP: "badge badge-up",
    DOWN: "badge badge-down",
    UNKNOWN: "badge badge-unknown",
  }[status] || "badge badge-unknown";

  return <span className={className}>{status}</span>;
}

function formatCheckedAt(value) {
  if (!value) return "—";
  return new Date(value).toLocaleString();
}

function formatResponseTime(value) {
  if (value == null) return "—";
  return `${Math.round(value)} ms`;
}

function App() {
  const [urls, setUrls] = useState([]);
  const [inputUrl, setInputUrl] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const loadUrls = useCallback(async () => {
    try {
      const data = await fetchUrls();
      setUrls(data);
      setError("");
    } catch {
      setError("Failed to load monitored URLs. Is the API running on localhost:8000?");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUrls();
    const interval = setInterval(loadUrls, REFRESH_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [loadUrls]);

  async function handleSubmit(event) {
    event.preventDefault();
    const trimmed = inputUrl.trim();
    if (!trimmed) return;

    setSubmitting(true);
    setError("");

    try {
      await addUrl(trimmed);
      setInputUrl("");
      await loadUrls();
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (err.response?.status === 409) {
        setError("This URL is already being monitored.");
      } else if (Array.isArray(detail)) {
        setError(detail.map((item) => item.msg).join(", "));
      } else if (typeof detail === "string") {
        setError(detail);
      } else {
        setError("Failed to add URL. Please check the format and try again.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Uptime Monitor</h1>
        <p>Track URL availability with automatic health checks every minute.</p>
      </header>

      <main className="container">
        <section className="card">
          <form className="add-form" onSubmit={handleSubmit}>
            <input
              type="url"
              placeholder="https://example.com"
              value={inputUrl}
              onChange={(event) => setInputUrl(event.target.value)}
              disabled={submitting}
            />
            <button type="submit" disabled={submitting || !inputUrl.trim()}>
              {submitting ? "Adding…" : "Add URL"}
            </button>
          </form>
          {error && <p className="error">{error}</p>}
        </section>

        <section className="card">
          {loading ? (
            <p className="muted">Loading…</p>
          ) : urls.length === 0 ? (
            <p className="muted">No URLs monitored yet. Add one above to get started.</p>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>URL</th>
                    <th>Status</th>
                    <th>HTTP Status Code</th>
                    <th>Response Time (ms)</th>
                    <th>Last Checked</th>
                  </tr>
                </thead>
                <tbody>
                  {urls.map((item) => (
                    <tr key={item.id}>
                      <td className="url-cell">{item.url}</td>
                      <td>
                        <StatusBadge status={item.status} />
                      </td>
                      <td>{item.status_code ?? "—"}</td>
                      <td>{formatResponseTime(item.response_time_ms)}</td>
                      <td>{formatCheckedAt(item.checked_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
