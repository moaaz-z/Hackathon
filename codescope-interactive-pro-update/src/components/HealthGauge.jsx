import { Activity } from "lucide-react";
import useCountUp from "../hooks/useCountUp.js";

export default function HealthGauge({ score = 0 }) {
  const safeScore = Math.max(0, Math.min(100, Number(score) || 0));
  const animated = useCountUp(safeScore, 900);

  const label =
    safeScore >= 85
      ? "Excellent"
      : safeScore >= 70
        ? "Good"
        : safeScore >= 50
          ? "Fair"
          : "Needs work";

  return (
    <section className="panel health-panel interactive-panel">
      <div className="section-heading">
        <span className="eyebrow">Repository health</span>
        <h2>Engineering health</h2>
      </div>

      <div
        className="health-gauge"
        style={{ "--score": `${safeScore * 3.6}deg` }}
        aria-label={`Engineering health ${safeScore} out of 100`}
      >
        <div className="health-gauge-inner">
          <Activity className="health-gauge-icon" size={17} />
          <strong>{Math.round(animated)}</strong>
          <span>/ 100</span>
        </div>
      </div>

      <div className="health-label">{label}</div>
      <p className="muted center health-caption">
        Maintainability, structure, testing, and risk signals.
      </p>
    </section>
  );
}
