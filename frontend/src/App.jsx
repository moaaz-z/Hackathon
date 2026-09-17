import { useState } from "react";
import {
  ArrowRight,
  BrainCircuit,
  Code2,
  ExternalLink,
  GitBranch,
  Orbit,
  ScanSearch,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import RepoForm from "./components/RepoForm.jsx";
import HealthGauge from "./components/HealthGauge.jsx";
import ArchitectureFlow from "./components/ArchitectureFlow.jsx";
import TechStack from "./components/TechStack.jsx";
import RepositoryVisuals from "./components/RepositoryVisuals.jsx";
import AuditVisuals from "./components/AuditVisuals.jsx";
import AnalysisPipeline from "./components/AnalysisPipeline.jsx";
import BackgroundEffects from "./components/BackgroundEffects.jsx";
import { Issues, Strengths } from "./components/Findings.jsx";
import {
  KeyComponents,
  Recommendations,
} from "./components/ComponentsAndRecommendations.jsx";

import { analyzeRepository, normalizeAnalysis } from "./lib/api.js";

const engineSteps = [
  { icon: GitBranch, title: "Repository", subtitle: "Public GitHub source" },
  { icon: ScanSearch, title: "Static facts", subtitle: "Structure & code signals" },
  { icon: BrainCircuit, title: "AI review", subtitle: "Evidence interpretation" },
  { icon: ShieldCheck, title: "Engineering audit", subtitle: "Risks & actions" },
];

export default function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [analysis, setAnalysis] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!repoUrl.trim()) {
      setError("Enter a public GitHub repository URL.");
      return;
    }

    setError("");
    setLoading(true);
    setAnalysis(null);

    try {
      const payload = await analyzeRepository(repoUrl.trim());
      setAnalysis(normalizeAnalysis(payload));
    } catch (err) {
      setError(err?.message || "Could not analyze this repository.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <BackgroundEffects />

      <header className="navbar">
        <a className="brand" href="/" aria-label="CodeScope home">
          <div className="brand-icon"><Orbit size={20} /></div>
          <div><strong>CodeScope</strong><span>Repository Auditor</span></div>
        </a>

        {analysis && (
          <button
            className="new-analysis-button"
            type="button"
            onClick={() => {
              setAnalysis(null);
              setError("");
              window.scrollTo({ top: 0, behavior: "smooth" });
            }}
          >
            New analysis
          </button>
        )}
      </header>

      <section className={`hero ${analysis ? "hero-compact" : ""}`}>
        <div className="hero-copy hero-enter">
          <div className="hero-badge"><Sparkles size={14} />Repository intelligence</div>
          <h1>Understand the codebase.<span> See what matters.</span></h1>
          <p>
            Turn an unfamiliar GitHub repository into a clear engineering audit —
            architecture, code signals, risks, and the improvements that deserve attention first.
          </p>
        </div>

        <div className="search-stage search-stage-pro">
          <div className="search-stage-topline">
            <span className="search-label">GitHub repository</span>
            <span className="secure-label"><ShieldCheck size={12} /> static inspection</span>
          </div>

          <RepoForm
            value={repoUrl}
            onChange={setRepoUrl}
            onSubmit={handleSubmit}
            loading={loading}
          />

          <p className="search-hint">Example: https://github.com/owner/repository</p>
        </div>

        {error && <div className="error-banner">{error}</div>}

        {!analysis && !loading && (
          <>
            <div className="feature-strip">
              <div><Code2 size={16} />Static analysis</div>
              <div><GitBranch size={16} />Architecture mapping</div>
              <div><ShieldCheck size={16} />Engineering risk review</div>
            </div>

            <div className="engine-map" aria-label="CodeScope analysis workflow">
              {engineSteps.map(({ icon: Icon, title, subtitle }, index) => (
                <div className="engine-map-wrap" key={title}>
                  <div className="engine-node">
                    <div className="engine-icon"><Icon size={18} /></div>
                    <div><strong>{title}</strong><span>{subtitle}</span></div>
                  </div>
                  {index < engineSteps.length - 1 && (
                    <div className="engine-connector"><span /><ArrowRight size={15} /></div>
                  )}
                </div>
              ))}
            </div>
          </>
        )}

        {loading && <AnalysisPipeline />}
      </section>

      {analysis && (
        <section className="results-shell">
          <section className="dashboard">
            <section className="panel summary-panel wide-panel interactive-panel summary-pro">
              <div className="summary-topline">
                <div className="summary-kicker">Repository overview</div>
                {analysis.repositoryUrl && (
                  <a
                    className="repo-link"
                    href={analysis.repositoryUrl}
                    target="_blank"
                    rel="noreferrer"
                  >
                    View repository <ExternalLink size={13} />
                  </a>
                )}
              </div>
              <h2>{analysis.projectName}</h2>
              <p className="purpose">{analysis.purpose}</p>
              <p className="summary-text">{analysis.summary}</p>
            </section>

            <HealthGauge score={analysis.healthScore} />
            <TechStack technologies={analysis.technologies} />

            <RepositoryVisuals staticAnalysis={analysis.staticAnalysis} />

            <AuditVisuals
              staticAnalysis={analysis.staticAnalysis}
              issues={analysis.issues}
              healthScore={analysis.healthScore}
            />

            <ArchitectureFlow architecture={analysis.architecture} />
            <Strengths strengths={analysis.strengths} />
            <KeyComponents components={analysis.components} />
            <Issues issues={analysis.issues} />
            <Recommendations recommendations={analysis.recommendations} />

            {analysis.finalAssessment && (
              <section className="panel final-assessment wide-panel interactive-panel">
                <div className="section-heading">
                  <span className="eyebrow">Conclusion</span>
                  <h2>Final assessment</h2>
                </div>
                <p>{analysis.finalAssessment}</p>
              </section>
            )}
          </section>
        </section>
      )}

      <footer>
        <span>CodeScope</span>
        <span>Static evidence + AI interpretation</span>
      </footer>
    </main>
  );
}
