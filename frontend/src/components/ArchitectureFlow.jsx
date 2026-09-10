import { ArrowRight, Boxes } from "lucide-react";

export default function ArchitectureFlow({ architecture }) {
  let steps = [];

  if (Array.isArray(architecture)) {
    steps = architecture;
  } else if (Array.isArray(architecture?.flow)) {
    steps = architecture.flow;
  } else if (Array.isArray(architecture?.layers)) {
    steps = architecture.layers;
  } else if (architecture?.type) {
    steps = [architecture.type];
  }

  if (!steps.length) {
    steps = ["Frontend", "API", "Services", "Database"];
  }

  return (
    <section className="panel">
      <div className="section-heading">
        <span className="eyebrow">Architecture</span>
        <h2>Project Architecture</h2>
      </div>

      <div className="architecture-flow">
        {steps.map((step, index) => (
          <div className="architecture-item" key={index}>
            <div className="architecture-node">
              <Boxes size={18} />
              <span>{String(step)}</span>
            </div>

            {index < steps.length - 1 && (
              <ArrowRight
                className="architecture-arrow"
                size={20}
              />
            )}
          </div>
        ))}
      </div>

      {architecture?.description && (
        <p className="muted">
          {architecture.description}
        </p>
      )}
    </section>
  );
}