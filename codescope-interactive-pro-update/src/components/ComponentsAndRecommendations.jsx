import { FileCode2, Lightbulb } from "lucide-react";

export function KeyComponents({ components = [] }) {
  return (
    <section className="panel interactive-panel">
      <div className="section-heading">
        <span className="eyebrow">Key components</span>
        <h2>Important project areas</h2>
      </div>

      <div className="stack-list">
        {components.length ? (
          components.map((item, index) => {
            const title = typeof item === "string" ? item : item?.name || item?.file || item?.path || "Component";
            const description = typeof item === "object" ? item?.description || item?.purpose || item?.role || "" : "";

            return (
              <article className="component-card" key={index}>
                <FileCode2 size={17} />
                <div>
                  <strong>{title}</strong>
                  {item?.file && <code>{item.file}</code>}
                  {description && <p>{description}</p>}
                </div>
              </article>
            );
          })
        ) : (
          <p className="muted">No key components returned.</p>
        )}
      </div>
    </section>
  );
}

export function Recommendations({ recommendations = [] }) {
  return (
    <section className="panel wide-panel recommendations-panel interactive-panel">
      <div className="section-heading">
        <span className="eyebrow">Action plan</span>
        <h2>Prioritized recommendations</h2>
      </div>

      <div className="recommendation-timeline">
        {recommendations.length ? (
          recommendations.map((item, index) => {
            const title = typeof item === "string" ? item : item?.title || "Recommendation";
            const description = typeof item === "object" ? item?.description || "" : "";

            return (
              <article className="recommendation-card recommendation-timeline-item" key={index}>
                <span className="recommendation-number">{index + 1}</span>
                <div className="recommendation-icon"><Lightbulb size={15} /></div>
                <div>
                  <strong>{title}</strong>
                  {item?.priority && <span className="priority-pill">{item.priority}</span>}
                  {description && <p>{description}</p>}
                </div>
              </article>
            );
          })
        ) : (
          <p className="muted">No recommendations returned.</p>
        )}
      </div>
    </section>
  );
}
