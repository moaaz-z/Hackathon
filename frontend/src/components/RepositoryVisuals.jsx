export default function RepositoryVisuals({
  staticAnalysis = {},
  technologies = [],
}) {
  const statistics =
    staticAnalysis?.statistics || {};

  const python =
    staticAnalysis?.python || {};

  const files =
    statistics?.total_files ?? 0;

  const lines =
    statistics?.total_loc ?? 0;

  const functions =
    Array.isArray(python?.functions)
      ? python.functions.length
      : 0;

  const classes =
    Array.isArray(python?.classes)
      ? python.classes.length
      : 0;

  const languages =
    statistics?.languages ||
    staticAnalysis?.languages ||
    {};

  const languageEntries =
    Object.entries(languages);

  const totalLanguageLoc =
    languageEntries.reduce(
      (sum, [, data]) =>
        sum + Number(data?.loc || 0),
      0
    );

  return (
    <section className="panel repository-visuals">
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

      <div className="metric-row">
        <MetricCard
          label="Files"
          value={files}
        />

        <MetricCard
          label="Lines"
          value={lines}
        />

        <MetricCard
          label="Functions"
          value={functions}
        />

        <MetricCard
          label="Classes"
          value={classes}
        />
      </div>

      {languageEntries.length > 0 && (
        <div className="language-visual">
          <div className="language-title">
            <strong>
              Language distribution
            </strong>

            <span>
              Top {languageEntries.length}
            </span>
          </div>

          <div className="language-bars">
            {languageEntries.map(
              ([language, data]) => {
                const loc =
                  Number(data?.loc || 0);

                const percentage =
                  totalLanguageLoc > 0
                    ? Math.round(
                        (loc /
                          totalLanguageLoc) *
                          100
                      )
                    : 0;

                return (
                  <div
                    className="language-item"
                    key={language}
                  >
                    <div className="language-meta">
                      <span>{language}</span>

                      <span>
                        {percentage}%
                      </span>
                    </div>

                    <div className="language-track">
                      <div
                        className="language-fill"
                        style={{
                          width: `${percentage}%`,
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

function MetricCard({
  label,
  value,
}) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}