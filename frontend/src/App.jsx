import { useState } from "react";
import { Code2, GitBranch, Orbit, ShieldCheck, Sparkles } from "lucide-react";

import RepoForm from "./components/RepoForm.jsx";
import HealthGauge from "./components/HealthGauge.jsx";
import ArchitectureFlow from "./components/ArchitectureFlow.jsx";
import TechStack from "./components/TechStack.jsx";
import RepositoryVisuals from "./components/RepositoryVisuals.jsx";
import { Issues, Strengths } from "./components/Findings.jsx";
import {
  KeyComponents,
  Recommendations,
} from "./components/ComponentsAndRecommendations.jsx";

import {
  analyzeRepository,
  normalizeAnalysis,
} from "./lib/api.js";

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
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <header className="navbar">
        <a className="brand" href="/" aria-label="CodeScope home">
          <div className="brand-icon">
            <Orbit size={21} />
          </div>
          <div>
            <strong>CodeScope</strong>
            <span>AI Codebase Auditor</span>
          </div>
        </a>
      </header>

      <section className={`hero ${analysis ? "hero-compact" : ""}`}>
        <div className="hero-copy">
          <div className="hero-badge">
            <Sparkles size={14} />
            Repository intelligence
          </div>

          <h1>
            Understand the codebase.
            <span> See what matters.</span>
          </h1>

          <p>
            Paste a public GitHub repository to uncover its purpose,
            architecture, technology stack, health, risks, and the improvements
            that deserve attention first.
          </p>
        </div>

        <div className="search-stage">
          <span className="search-label">GitHub repository</span>
          <RepoForm
            value={repoUrl}
            onChange={setRepoUrl}
            onSubmit={handleSubmit}
            loading={loading}
          />
          <p className="search-hint">
            Example: https://github.com/owner/repository
          </p>
        </div>

        {error && <div className="error-banner">{error}</div>}

        {!analysis && !loading && (
          <div className="feature-strip">
            <div><Code2 size={16} /> Static analysis</div>
            <div><GitBranch size={16} /> Architecture mapping</div>
            <div><ShieldCheck size={16} /> Engineering risk review</div>
          </div>
        )}

        {loading && (
          <div className="loading-card">
            <div className="scanner">
              <div className="scanner-line" />
            </div>
            <div>
              <strong>Reading the repository…</strong>
              <p>
                Mapping files, extracting code signals, and preparing the AI review.
              </p>
            </div>
          </div>
        )}
      </section>

      {analysis && (
        <section className="dashboard">
          <section className="panel summary-panel">
            <div className="summary-kicker">Repository overview</div>
            <h2>{analysis.projectName}</h2>
            <p className="purpose">{analysis.purpose}</p>
            <p className="summary-text">{analysis.summary}</p>
          </section>

          <HealthGauge score={analysis.healthScore} />

          <RepositoryVisuals
            staticAnalysis={analysis.staticAnalysis}
            technologies={analysis.technologies}
          />

          <ArchitectureFlow architecture={analysis.architecture} />
          <TechStack technologies={analysis.technologies} />
          <Strengths strengths={analysis.strengths} />
          <KeyComponents components={analysis.components} />
          <Issues issues={analysis.issues} />
          <Recommendations recommendations={analysis.recommendations} />

          {analysis.finalAssessment && (
            <section className="panel final-assessment wide-panel">
              <div className="section-heading">
                <span className="eyebrow">AI conclusion</span>
                <h2>Final assessment</h2>
              </div>
              <p>{analysis.finalAssessment}</p>
            </section>
          )}
        </section>
      )}

      <footer>
        <span>CodeScope</span>
        <span>Static evidence + AI interpretation</span>
      </footer>
    </main>
  );
}