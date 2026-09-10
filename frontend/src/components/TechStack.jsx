import { Cpu } from "lucide-react";

export default function TechStack({ technologies = [] }) {
  return (
    <section className="panel">
      <div className="section-heading">
        <span className="eyebrow">Technology Stack</span>
        <h2>Detected Technologies</h2>
      </div>

      <div className="tech-grid">
        {technologies.length > 0 ? (
          technologies.map((tech, index) => {
            const name =
              typeof tech === "string"
                ? tech
                : tech?.name ||
                  tech?.technology ||
                  "Unknown";

            return (
              <div className="tech-badge" key={index}>
                <Cpu size={15} />
                <span>{name}</span>

                {typeof tech === "object" &&
                  tech?.category && (
                    <small>{tech.category}</small>
                  )}
              </div>
            );
          })
        ) : (
          <p className="muted">
            No technologies detected.
          </p>
        )}
      </div>
    </section>
  );
}