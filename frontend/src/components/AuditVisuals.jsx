import {
  AlertTriangle,
  CheckCircle2,
  FileWarning,
  TestTube2,
} from "lucide-react";


const order = [
  "critical",
  "high",
  "medium",
  "low",
];


export default function AuditVisuals({
  staticAnalysis = {},
  issues = [],
}) {
  const severity = order.reduce(
    (acc, level) => {
      acc[level] = issues.filter(
        (issue) =>
          String(
            issue?.severity || "medium"
          ).toLowerCase() === level
      ).length;

      return acc;
    },
    {}
  );

  const totalIssues = issues.length;

  const tests =
    staticAnalysis?.tests || {};

  const quality =
    staticAnalysis?.quality || {};

  const statistics =
    staticAnalysis?.statistics || {};

  const languages =
    statistics?.languages ||
    staticAnalysis?.languages ||
    {};

  const languageEntries =
    Object.entries(languages).sort(
      (a, b) =>
        Number(b?.[1]?.loc || 0) -
        Number(a?.[1]?.loc || 0)
    );

  const dominantLanguage =
    statistics?.dominant_language ||
    languageEntries[0]?.[0] ||
    "Unknown";

  const testRatio = Math.max(
    0,
    Math.min(
      1,
      Number(
        tests?.test_file_ratio || 0
      )
    )
  );

  const complexity =
    Number(
      quality?.average_python_function_complexity ||
      0
    );

  const pythonComplexityAvailable =
    Boolean(
      quality?.python_complexity_available
    );

  const todos =
    Number(
      quality?.todo_fixme_count || 0
    );

  const largeFiles =
    Number(
      quality?.large_file_count || 0
    );

  const criticalPct =
    totalIssues
      ? (
          severity.critical /
          totalIssues
        ) * 100
      : 0;

  const highPct =
    totalIssues
      ? (
          severity.high /
          totalIssues
        ) * 100
      : 0;

  const mediumPct =
    totalIssues
      ? (
          severity.medium /
          totalIssues
        ) * 100
      : 0;

  const stop1 = criticalPct;
  const stop2 =
    stop1 + highPct;
  const stop3 =
    stop2 + mediumPct;

  const donut =
    totalIssues
      ? `conic-gradient(
          #c85f64 0% ${stop1}%,
          #d28d58 ${stop1}% ${stop2}%,
          #caaa66 ${stop2}% ${stop3}%,
          #7eb794 ${stop3}% 100%
        )`
      : "conic-gradient(#2a2f2b 0% 100%)";

  const complexitySignal =
    dominantLanguage === "Python"
      ? {
          icon: CheckCircle2,
          label:
            "Avg. Python complexity",
          value:
            pythonComplexityAvailable
              ? complexity.toFixed(1)
              : "N/A",
          detail:
            pythonComplexityAvailable
              ? "Cyclomatic complexity average"
              : "No Python functions available",
        }
      : {
          icon: CheckCircle2,
          label: "Complexity analysis",
          value: "N/A",
          detail:
            `${dominantLanguage} complexity is not enabled yet`,
        };

  const signals = [
    {
      icon: TestTube2,
      label: "Test file ratio",
      value:
        `${Math.round(
          testRatio * 100
        )}%`,
      detail:
        `${tests?.test_file_count || 0} test files detected`,
    },
    complexitySignal,
    {
      icon: AlertTriangle,
      label: "TODO / FIXME",
      value: String(todos),
      detail: "Unresolved markers",
    },
    {
      icon: FileWarning,
      label: "Large files",
      value: String(largeFiles),
      detail:
        "Files above analyzer threshold",
    },
  ];

  return (
    <section className="panel audit-visuals wide-panel interactive-panel">
      <div className="section-heading">
        <span className="eyebrow">
          Engineering signals
        </span>

        <h2>
          Risk profile & quality signals
        </h2>
      </div>

      <div className="audit-visual-grid">
        <div className="risk-visual-card">
          <div
            className="risk-donut"
            style={{
              background: donut,
            }}
          >
            <div className="risk-donut-center">
              <strong>
                {totalIssues}
              </strong>

              <span>issues</span>
            </div>
          </div>

          <div className="risk-legend">
            {order.map(
              (level) => (
                <div
                  className="risk-legend-row"
                  key={level}
                >
                  <span
                    className={
                      `risk-dot ${level}`
                    }
                  />

                  <span>{level}</span>

                  <strong>
                    {severity[level]}
                  </strong>
                </div>
              )
            )}
          </div>
        </div>

        <div className="signal-grid">
          {signals.map(
            (
              {
                icon: Icon,
                label,
                value,
                detail,
              },
              index
            ) => (
              <article
                className="signal-card"
                key={label}
                style={{
                  animationDelay:
                    `${index * 70}ms`,
                }}
              >
                <div className="signal-icon">
                  <Icon size={16} />
                </div>

                <div>
                  <span>{label}</span>

                  <strong>
                    {value}
                  </strong>

                  <small>
                    {detail}
                  </small>
                </div>
              </article>
            )
          )}
        </div>
      </div>
    </section>
  );
}
