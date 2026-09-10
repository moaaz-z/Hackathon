function numeric(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

function pick(obj, keys, fallback = 0) {
  for (const key of keys) {
    if (obj?.[key] !== undefined && obj?.[key] !== null) return obj[key];
  }
  return fallback;
}

function getLanguageRows(staticAnalysis) {
  const raw =
    staticAnalysis?.languages ||
    staticAnalysis?.language_stats ||
    staticAnalysis?.statistics?.languages ||
    {};

  if (Array.isArray(raw)) {
    return raw
      .map((item) => ({
        name: item?.name || item?.language || "Other",
        value: numeric(item?.lines ?? item?.files ?? item?.count ?? item?.percentage),
      }))
      .filter((item) => item.value > 0);
  }

  if (raw && typeof raw === "object") {
    return Object.entries(raw)
      .map(([name, data]) => ({
        name,
        value:
          typeof data === "number"
            ? data
            : numeric(data?.lines ?? data?.files ?? data?.count ?? data?.percentage),
      }))
      .filter((item) => item.value > 0);
  }

  return [];
}

export default function RepositoryVisuals({ staticAnalysis = {} }) {
  const stats = staticAnalysis?.statistics || staticAnalysis || {};

  const metrics = [
    { label: "Files", value: pick(stats, ["files", "file_count", "total_files"]) },
    { label: "Lines", value: pick(stats, ["lines", "line_count", "total_lines", "loc"]) },
    { label: "Functions", value: pick(stats, ["functions", "function_count", "total_functions"]) },
    { label: "Classes", value: pick(stats, ["classes", "class_count", "total_classes"]) },
  ];

  const languages = getLanguageRows(staticAnalysis)
    .sort((a, b) => b.value - a.value)
    .slice(0, 6);

  const total = languages.reduce((sum, item) => sum + item.value, 0);

  return (
    <section className="panel repository-visuals wide-panel">
      <div className="section-heading visual-heading">
        <div>
          <span className="eyebrow">Repository at a glance</span>
          <h2>Codebase footprint</h2>
        </div>
        <p>Static signals extracted directly from the repository.</p>
      </div>

      <div className="metric-row">
        {metrics.map((metric) => (
          <div className="metric-card" key={metric.label}>
            <span>{metric.label}</span>
            <strong>{Number(metric.value || 0).toLocaleString()}</strong>
          </div>
        ))}
      </div>

      {languages.length > 0 && (
        <div className="language-visual">
          <div className="language-title">
            <strong>Language distribution</strong>
            <span>Top {languages.length}</span>
          </div>

          <div className="language-bars">
            {languages.map((language) => {
              const percent = total ? (language.value / total) * 100 : 0;

              return (
                <div className="language-row" key={language.name}>
                  <div className="language-meta">
                    <span>{language.name}</span>
                    <span>{Math.round(percent)}%</span>
                  </div>
                  <div className="language-track">
                    <div
                      className="language-fill"
                      style={{ width: `${Math.max(percent, 3)}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </section>
  );
}