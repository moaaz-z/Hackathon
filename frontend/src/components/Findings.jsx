import {
  AlertTriangle,
  CheckCircle2,
  FileCode2,
  Lightbulb,
} from "lucide-react";

function getText(item, keys, fallback = "") {
  if (typeof item === "string") {
    return item;
  }

  for (const key of keys) {
    if (item?.[key]) {
      return item[key];
    }
  }

  return fallback;
}

export function Strengths({ strengths = [] }) {
  return (
    <section className="panel">
      <div className="section-heading">
        <span className="eyebrow">Strengths</span>
        <h2>What Looks Good</h2>
      </div>

      <div className="stack-list">
        {strengths.length > 0 ? (
          strengths.map((item, index) => (
            <article
              className="finding-card positive"
              key={index}
            >
              <CheckCircle2 size={19} />

              <div>
                <strong>
                  {getText(
                    item,
                    ["title", "name"],
                    "Strength"
                  )}
                </strong>

                <p>
                  {getText(
                    item,
                    ["description", "evidence", "detail"],
                    ""
                  )}
                </p>
              </div>
            </article>
          ))
        ) : (
          <p className="muted">
            No strengths returned.
          </p>
        )}
      </div>
    </section>
  );
}

export function Issues({ issues = [] }) {
  return (
    <section className="panel wide-panel">
      <div className="section-heading">
        <span className="eyebrow">Issues</span>
        <h2>Detected Risks</h2>
      </div>

      <div className="issues-grid">
        {issues.length > 0 ? (
          issues.map((issue, index) => {
            const severity = String(
              issue?.severity || "medium"
            ).toLowerCase();

            let evidence = issue?.evidence || "";

            if (Array.isArray(evidence)) {
              evidence = evidence.join(" • ");
            }

            return (
              <article
                className="issue-card"
                key={index}
              >
                <div className="issue-topline">
                  <span
                    className={`severity ${severity}`}
                  >
                    {severity}
                  </span>

                  {issue?.file && (
                    <span className="file-pill">
                      <FileCode2 size={13} />
                      {issue.file}
                    </span>
                  )}
                </div>

                <h3>
                  {issue?.title || "Detected Issue"}
                </h3>

                {issue?.description && (
                  <p>{issue.description}</p>
                )}

                {evidence && (
                  <div className="evidence-block">
                    <AlertTriangle size={15} />
                    <span>{evidence}</span>
                  </div>
                )}

                {issue?.recommendation && (
                  <div className="recommendation-inline">
                    <Lightbulb size={15} />
                    <span>
                      {issue.recommendation}
                    </span>
                  </div>
                )}
              </article>
            );
          })
        ) : (
          <p className="muted">
            No issues detected.
          </p>
        )}
      </div>
    </section>
  );
}