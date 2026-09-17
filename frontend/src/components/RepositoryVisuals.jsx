import {
  Braces,
  FileCode2,
  Files,
  Languages,
  Rows3,
} from "lucide-react";
import useCountUp from "../hooks/useCountUp.js";


function MetricCard({
  label,
  value,
  icon: Icon,
}) {
  const animated = useCountUp(value, 800);

  return (
    <div className="metric-card metric-card-animated">
      <div className="metric-icon">
        <Icon size={16} />
      </div>

      <span>{label}</span>

      <strong>
        {Math.round(animated).toLocaleString()}
      </strong>
    </div>
  );
}


export default function RepositoryVisuals({
  staticAnalysis = {},
}) {
  const statistics =
    staticAnalysis?.statistics || {};

  const python =
    staticAnalysis?.python || {};

  const c =
    staticAnalysis?.c || {};

  const languages =
    statistics?.languages ||
    staticAnalysis?.languages ||
    {};

  const entries = Object.entries(languages)
    .map(([name, data]) => ({
      name,
      loc: Number(data?.loc || 0),
      files: Number(data?.files || 0),
    }))
    .sort(
      (a, b) => b.loc - a.loc
    );

  const dominantLanguage =
    statistics?.dominant_language ||
    entries[0]?.name ||
    "Unknown";

  const files =
    Number(
      statistics?.total_files ?? 0
    );

  const lines =
    Number(
      statistics?.source_loc ??
      statistics?.total_loc ??
      0
    );

  const pythonFunctions =
    Array.isArray(python?.functions)
      ? python.functions.length
      : Number(
          statistics?.python_function_count ?? 0
        );

  const pythonClasses =
    Array.isArray(python?.classes)
      ? python.classes.length
      : Number(
          statistics?.python_class_count ?? 0
        );

  const cFunctions =
    Array.isArray(c?.functions)
      ? c.functions.length
      : Number(
          statistics?.c_function_count ?? 0
        );

  const cHeaders =
    Number(
      c?.header_file_count ??
      statistics?.c_header_count ??
      0
    );

  let metrics;

  if (dominantLanguage === "Python") {
    metrics = [
      {
        label: "Files",
        value: files,
        icon: Files,
      },
      {
        label: "Source lines",
        value: lines,
        icon: Rows3,
      },
      {
        label: "Functions",
        value: pythonFunctions,
        icon: Braces,
      },
      {
        label: "Classes",
        value: pythonClasses,
        icon: FileCode2,
      },
    ];
  } else if (dominantLanguage === "C") {
    metrics = [
      {
        label: "Files",
        value: files,
        icon: Files,
      },
      {
        label: "Source lines",
        value: lines,
        icon: Rows3,
      },
      {
        label: "C functions",
        value: cFunctions,
        icon: Braces,
      },
      {
        label: "Header files",
        value: cHeaders,
        icon: FileCode2,
      },
    ];
  } else {
    metrics = [
      {
        label: "Files",
        value: files,
        icon: Files,
      },
      {
        label: "Source lines",
        value: lines,
        icon: Rows3,
      },
      {
        label: "Languages",
        value: entries.length,
        icon: Languages,
      },
      {
        label: "Source files",
        value: Number(
          statistics?.source_files ?? 0
        ),
        icon: FileCode2,
      },
    ];
  }

  const totalLoc = entries.reduce(
    (sum, item) => sum + item.loc,
    0
  );

  return (
    <section className="panel repository-visuals interactive-panel">
      <div className="visuals-heading-row">
        <div className="section-heading">
          <span className="eyebrow">
            Repository at a glance
          </span>

          <h2>Codebase footprint</h2>

          <p className="muted">
            Static signals extracted directly
            from the repository.
          </p>
        </div>

        <span className="live-data-pill">
          <span />
          {dominantLanguage} dominant
        </span>
      </div>

      <div className="metric-row">
        {metrics.map(
          ({
            label,
            value,
            icon,
          }) => (
            <MetricCard
              key={label}
              label={label}
              value={value}
              icon={icon}
            />
          )
        )}
      </div>

      {entries.length > 0 && (
        <div className="language-visual">
          <div className="language-title">
            <strong>
              Language distribution
            </strong>

            <span>
              {entries.length} detected
            </span>
          </div>

          <div className="language-bars">
            {entries.map(
              (item, index) => {
                const percentage =
                  totalLoc > 0
                    ? Math.round(
                        (
                          item.loc /
                          totalLoc
                        ) * 100
                      )
                    : 0;

                return (
                  <div
                    className="language-item"
                    key={item.name}
                  >
                    <div className="language-meta">
                      <span>
                        {item.name}
                      </span>

                      <span>
                        {percentage}%
                      </span>
                    </div>

                    <div className="language-track">
                      <div
                        className="language-fill language-fill-animated"
                        style={{
                          width:
                            `${percentage}%`,
                          animationDelay:
                            `${index * 90}ms`,
                        }}
                      />
                    </div>
                  </div>
                );
              }
            )}
          </div>
        </div>
      )}
    </section>
  );
}
