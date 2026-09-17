import { Braces, FileCode2, Files, Rows3 } from "lucide-react";
import useCountUp from "../hooks/useCountUp.js";

function MetricCard({ label, value, icon: Icon }) {
  const animated = useCountUp(value, 800);

  return (
    <div className="metric-card metric-card-animated">
      <div className="metric-icon">
        <Icon size={16} />
      </div>
      <span>{label}</span>
      <strong>{Math.round(animated).toLocaleString()}</strong>
    </div>
  );
}

export default function RepositoryVisuals({ staticAnalysis = {} }) {
  const statistics = staticAnalysis?.statistics || {};
  const python = staticAnalysis?.python || {};

  const files = statistics?.total_files ?? 0;
  const lines = statistics?.total_loc ?? 0;
  const functions = Array.isArray(python?.functions) ? python.functions.length : 0;
  const classes = Array.isArray(python?.classes) ? python.classes.length : 0;

  const languages = statistics?.languages || staticAnalysis?.languages || {};
  const entries = Object.entries(languages)
    .map(([name, data]) => ({ name, loc: Number(data?.loc || 0) }))
    .sort((a, b) => b.loc - a.loc);

  const totalLoc = entries.reduce((sum, item) => sum + item.loc, 0);

  return (
    <section className="panel repository-visuals interactive-panel">
      <div className="visuals-heading-row">
        <div className="section-heading">
          <span className="eyebrow">Repository at a glance</span>
          <h2>Codebase footprint</h2>
          <p className="muted">Static signals extracted directly from the repository.</p>
        </div>
        <span className="live-data-pill"><span /> Static evidence</span>
      </div>

      <div className="metric-row">
        <MetricCard label="Files" value={files} icon={Files} />
        <MetricCard label="Lines" value={lines} icon={Rows3} />
        <MetricCard label="Functions" value={functions} icon={Braces} />
        <MetricCard label="Classes" value={classes} icon={FileCode2} />
      </div>

      {entries.length > 0 && (
        <div className="language-visual">
          <div className="language-title">
            <strong>Language distribution</strong>
            <span>{entries.length} detected</span>
          </div>

          <div className="language-bars">
            {entries.map((item, index) => {
              const percentage = totalLoc > 0 ? Math.round((item.loc / totalLoc) * 100) : 0;

              return (
                <div className="language-item" key={item.name}>
                  <div className="language-meta">
                    <span>{item.name}</span>
                    <span>{percentage}%</span>
                  </div>
                  <div className="language-track">
                    <div
                      className="language-fill language-fill-animated"
                      style={{
                        width: `${percentage}%`,
                        animationDelay: `${index * 90}ms`,
                      }}
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
