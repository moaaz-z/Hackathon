import { useEffect, useState } from "react";
import { BrainCircuit, GitBranch, ScanSearch, Sparkles } from "lucide-react";

const steps = [
  { label: "Clone", detail: "Repository", icon: GitBranch },
  { label: "Scan", detail: "Static facts", icon: ScanSearch },
  { label: "Reason", detail: "Code signals", icon: BrainCircuit },
  { label: "Review", detail: "AI audit", icon: Sparkles },
];

export default function AnalysisPipeline() {
  const [active, setActive] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setActive((current) => (current + 1) % steps.length);
    }, 1150);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="analysis-pipeline" aria-label="Repository analysis in progress">
      <div className="pipeline-heading">
        <div>
          <strong>Analyzing repository</strong>
          <p>Collecting evidence and preparing the engineering review.</p>
        </div>
        <span className="pipeline-live"><span /> working</span>
      </div>

      <div className="pipeline-track">
        <div className="pipeline-progress" style={{ width: `${((active + 1) / steps.length) * 100}%` }} />
      </div>

      <div className="pipeline-steps">
        {steps.map(({ label, detail, icon: Icon }, index) => (
          <div className={`pipeline-step ${index === active ? "active" : ""} ${index < active ? "done" : ""}`} key={label}>
            <div className="pipeline-icon"><Icon size={16} /></div>
            <div><strong>{label}</strong><span>{detail}</span></div>
          </div>
        ))}
      </div>
    </div>
  );
}
