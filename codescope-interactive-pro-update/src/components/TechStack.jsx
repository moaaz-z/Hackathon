import { Cpu } from "lucide-react";

export default function TechStack({ technologies = [] }) {
  return (
    <section className="panel interactive-panel">
      <div className="section-heading">
        <span className="eyebrow">Technology stack</span>
        <h2>Detected technologies</h2>
      </div>

      <div className="tech-grid">
        {technologies.length ? (
          technologies.map((technology, index) => {
            const name =
              typeof technology === "string"
                ? technology
                : technology?.name || technology?.technology || technology?.framework || "Unknown";

            return (
              <div
                className="tech-badge tech-badge-animated"
                key={`${name}-${index}`}
                style={{ animationDelay: `${index * 55}ms` }}
              >
                <Cpu size={14} />
                <span>{name}</span>
                {technology?.category && <small>{technology.category}</small>}
              </div>
            );
          })
        ) : (
          <p className="muted">No technologies returned.</p>
        )}
      </div>
    </section>
  );
}
