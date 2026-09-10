import {
  ArrowRight,
  Boxes,
  Database,
  Globe2,
  ServerCog,
  Workflow,
} from "lucide-react";

function getSteps(architecture) {
  if (Array.isArray(architecture)) {
    return architecture;
  }

  if (Array.isArray(architecture?.flow) && architecture.flow.length) {
    return architecture.flow;
  }

  if (Array.isArray(architecture?.layers) && architecture.layers.length) {
    return architecture.layers;
  }

  const description =
    architecture?.description ||
    architecture?.type ||
    architecture?.pattern ||
    "";

  if (description) {
    const normalized = description
      .replace(/[→>-]/g, "|")
      .split("|")
      .map((item) => item.trim())
      .filter(Boolean);

    if (normalized.length >= 2 && normalized.length <= 8) {
      return normalized;
    }
  }

  return ["Entry / Interface", "Application Logic", "Core Services", "Data / Storage"];
}

function iconForStep(step, index) {
  const value = String(step).toLowerCase();

  if (
    value.includes("frontend") ||
    value.includes("client") ||
    value.includes("ui") ||
    value.includes("interface")
  ) {
    return <Globe2 size={20} />;
  }

  if (
    value.includes("database") ||
    value.includes("storage") ||
    value.includes("data")
  ) {
    return <Database size={20} />;
  }

  if (
    value.includes("service") ||
    value.includes("backend") ||
    value.includes("server") ||
    value.includes("api")
  ) {
    return <ServerCog size={20} />;
  }

  return index === 0 ? <Boxes size={20} /> : <Workflow size={20} />;
}

export default function ArchitectureFlow({ architecture = {} }) {
  const steps = getSteps(architecture);

  const pattern =
    architecture?.type ||
    architecture?.pattern ||
    (typeof architecture === "string" ? architecture : "");

  const description =
    typeof architecture === "object"
      ? architecture?.description || ""
      : "";

  return (
    <section className="panel architecture-panel wide-panel">
      <div className="architecture-header">
        <div className="section-heading">
          <span className="eyebrow">Project architecture</span>
          <h2>How the codebase is structured</h2>
        </div>

        {pattern && (
          <span className="architecture-pattern">
            {pattern}
          </span>
        )}
      </div>

      <div className="architecture-flow">
        {steps.map((step, index) => (
          <div className="architecture-step" key={`${step}-${index}`}>
            <div className="architecture-node">
              <div className="architecture-icon">
                {iconForStep(step, index)}
              </div>

              <div>
                <span className="architecture-index">
                  Step {index + 1}
                </span>

                <strong>{String(step)}</strong>
              </div>
            </div>

            {index < steps.length - 1 && (
              <div className="architecture-connector">
                <div className="connector-line" />
                <ArrowRight size={18} />
              </div>
            )}
          </div>
        ))}
      </div>

      {description && (
        <div className="architecture-note">
          <span>Architecture note</span>
          <p>{description}</p>
        </div>
      )}
    </section>
  );
}