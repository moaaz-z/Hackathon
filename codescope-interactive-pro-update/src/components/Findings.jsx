import { useMemo, useState } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  ChevronDown,
  FileCode2,
  Lightbulb,
} from "lucide-react";

function normalizeText(value, fallback = "") {
  if (typeof value === "string") return value;
  if (Array.isArray(value)) return value.join(" • ");
  return fallback;
}

export function Strengths({ strengths = [] }) {
  return (
    <section className="panel interactive-panel">
      <div className="section-heading">
        <span className="eyebrow">Strengths</span>
        <h2>What looks good</h2>
      </div>

      <div className="stack-list">
        {strengths.length ? (
          strengths.map((item, index) => {
            const title = typeof item === "string" ? item : item?.title || item?.name || "Positive finding";
            const description = typeof item === "object" ? item?.description || item?.evidence || "" : "";

            return (
              <article className="finding-card finding-positive" key={index}>
                <CheckCircle2 size={17} />
                <div>
                  <strong>{title}</strong>
                  {description && <p>{description}</p>}
                </div>
              </article>
            );
          })
        ) : (
          <p className="muted">No strengths returned.</p>
        )}
      </div>
    </section>
  );
}

export function Issues({ issues = [] }) {
  const [filter, setFilter] = useState("all");
  const [expanded, setExpanded] = useState(null);

  const counts = useMemo(() => {
    const result = { all: issues.length, critical: 0, high: 0, medium: 0, low: 0 };
    issues.forEach((issue) => {
      const severity = String(issue?.severity || "medium").toLowerCase();
      if (result[severity] !== undefined) result[severity] += 1;
    });
    return result;
  }, [issues]);

  const visible = filter === "all"
    ? issues
    : issues.filter((issue) => String(issue?.severity || "medium").toLowerCase() === filter);

  const filters = ["all", "critical", "high", "medium", "low"];

  return (
    <section className="panel wide-panel issues-panel interactive-panel">
      <div className="issues-heading-row">
        <div className="section-heading">
          <span className="eyebrow">Risk review</span>
          <h2>Issues & recommendations</h2>
        </div>

        <div className="issue-filters" role="group" aria-label="Filter issues by severity">
          {filters.map((level) => (
            <button
              type="button"
              className={`issue-filter ${filter === level ? "active" : ""}`}
              onClick={() => setFilter(level)}
              key={level}
            >
              {level}
              <span>{counts[level]}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="issues-grid">
        {visible.length ? (
          visible.map((issue, index) => {
            const severity = String(issue?.severity || "medium").toLowerCase();
            const evidence = normalizeText(issue?.evidence);
            const key = `${issue?.title || "issue"}-${index}`;
            const open = expanded === key;

            return (
              <article className={`issue-card issue-card-interactive ${open ? "expanded" : ""}`} key={key}>
                <div className="issue-topline">
                  <span className={`severity ${severity}`}>{severity}</span>
                  {issue?.file && (
                    <span className="file-pill"><FileCode2 size={12} />{issue.file}</span>
                  )}
                </div>

                <div className="issue-title-row">
                  <h3>{issue?.title || issue?.name || "Detected issue"}</h3>
                  <button
                    className="issue-toggle"
                    type="button"
                    onClick={() => setExpanded(open ? null : key)}
                    aria-expanded={open}
                    aria-label={open ? "Collapse issue details" : "Expand issue details"}
                  >
                    <ChevronDown size={16} />
                  </button>
                </div>

                {issue?.description && <p>{issue.description}</p>}

                <div className="issue-details" aria-hidden={!open}>
                  {evidence && (
                    <div className="evidence-block">
                      <AlertTriangle size={14} />
                      <span>{evidence}</span>
                    </div>
                  )}

                  {issue?.recommendation && (
                    <div className="recommendation-inline">
                      <Lightbulb size={14} />
                      <span>{issue.recommendation}</span>
                    </div>
                  )}
                </div>
              </article>
            );
          })
        ) : (
          <p className="muted">No issues in this severity level.</p>
        )}
      </div>
    </section>
  );
}
