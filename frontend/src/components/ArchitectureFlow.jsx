import {
  ArrowDown,
  BarChart3,
  Database,
  FileSpreadsheet,
  NotebookTabs,
  ServerCog,
  Boxes,
} from "lucide-react";

function getArchitectureSteps(architecture = {}) {
  const description =
    typeof architecture === "string"
      ? architecture
      : architecture?.description || "";

  const text = description.toLowerCase();

  // Data / analytics project
  if (
    text.includes("csv") ||
    text.includes("data file") ||
    text.includes("notebook") ||
    text.includes("analytics") ||
    text.includes("sql")
  ) {
    const steps = [];

    if (
      text.includes("csv") ||
      text.includes("data file")
    ) {
      steps.push({
        title: "Data Source",
        subtitle: "Repository data files",
        icon: "data",
      });
    }

    if (
      text.includes("notebook") ||
      text.includes("jupyter")
    ) {
      steps.push({
        title: "Notebook Analysis",
        subtitle: "Interactive exploration",
        icon: "notebook",
      });
    }

    if (text.includes("sql")) {
      steps.push({
        title: "SQL Queries",
        subtitle: "Structured data analysis",
        icon: "database",
      });
    }

    steps.push({
      title: "Insights / Output",
      subtitle: "Analysis results",
      icon: "chart",
    });

    return steps;
  }

  // API / backend project
  if (
    text.includes("api") ||
    text.includes("backend") ||
    text.includes("service")
  ) {
    return [
      {
        title: "Interface",
        subtitle: "User or client requests",
        icon: "interface",
      },
      {
        title: "Application Layer",
        subtitle: "Business logic",
        icon: "service",
      },
      {
        title: "Core Services",
        subtitle: "Processing and orchestration",
        icon: "service",
      },
      {
        title: "Data Layer",
        subtitle: "Persistence or external data",
        icon: "database",
      },
    ];
  }

  // General project
  return [
    {
      title: "Entry Point",
      subtitle: "Application start",
      icon: "interface",
    },
    {
      title: "Core Logic",
      subtitle: "Main project behavior",
      icon: "service",
    },
    {
      title: "Supporting Modules",
      subtitle: "Utilities and components",
      icon: "boxes",
    },
    {
      title: "Output",
      subtitle: "Project result",
      icon: "chart",
    },
  ];
}

function getArchitectureType(architecture = {}) {
  const description =
    typeof architecture === "string"
      ? architecture
      : architecture?.description || "";

  const text = description.toLowerCase();

  if (
    text.includes("notebook") ||
    text.includes("analytics") ||
    text.includes("csv")
  ) {
    return "Data Analytics";
  }

  if (
    text.includes("api") ||
    text.includes("backend")
  ) {
    return "Service Architecture";
  }

  if (text.includes("script")) {
    return "Script-Based";
  }

  if (text.includes("package")) {
    return "Modular Package";
  }

  return "Repository Structure";
}

function StepIcon({ type }) {
  const props = {
    size: 20,
    strokeWidth: 1.8,
  };

  switch (type) {
    case "data":
      return <FileSpreadsheet {...props} />;

    case "notebook":
      return <NotebookTabs {...props} />;

    case "database":
      return <Database {...props} />;

    case "chart":
      return <BarChart3 {...props} />;

    case "service":
      return <ServerCog {...props} />;

    case "boxes":
      return <Boxes {...props} />;

    default:
      return <Boxes {...props} />;
  }
}

export default function ArchitectureFlow({
  architecture = {},
}) {
  const description =
    typeof architecture === "string"
      ? architecture
      : architecture?.description || "";

  const steps =
    getArchitectureSteps(architecture);

  const architectureType =
    getArchitectureType(architecture);

  return (
    <section className="panel architecture-panel wide-panel">
      <div className="architecture-header">
        <div className="section-heading">
          <span className="eyebrow">
            Project architecture
          </span>

          <h2>
            How the codebase is structured
          </h2>
        </div>

        <span className="architecture-pattern">
          {architectureType}
        </span>
      </div>

      <div className="architecture-flow-vertical">
        {steps.map((step, index) => (
          <div
            className="architecture-flow-item"
            key={`${step.title}-${index}`}
          >
            <div className="architecture-node-clean">
              <div className="architecture-node-icon">
                <StepIcon type={step.icon} />
              </div>

              <div className="architecture-node-content">
                <span className="architecture-step-label">
                  Stage {index + 1}
                </span>

                <strong>
                  {step.title}
                </strong>

                <small>
                  {step.subtitle}
                </small>
              </div>
            </div>

            {index < steps.length - 1 && (
              <div className="architecture-arrow">
                <ArrowDown
                  size={18}
                  strokeWidth={1.7}
                />
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