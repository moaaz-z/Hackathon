import { useState } from "react";

import {
  Activity,
  Code2,
  GitBranch,
  Orbit,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import RepoForm from "./components/RepoForm.jsx";
import HealthGauge from "./components/HealthGauge.jsx";
import ArchitectureFlow from "./components/ArchitectureFlow.jsx";
import TechStack from "./components/TechStack.jsx";

import {
  Issues,
  Strengths,
} from "./components/Findings.jsx";

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
      setError("Please enter a GitHub repository URL.");
      return;
    }

    setError("");
    setLoading(true);
    setAnalysis(null);

    try {
      const payload = await analyzeRepository(
        repoUrl.trim()
      );

      console.log("Backend response:", payload);

      const normalized =
        normalizeAnalysis(payload);

      console.log(
        "Normalized analysis:",
        normalized
      );

      setAnalysis(normalized);

    } catch (err) {
      console.error(err);

      setError(
        err?.message ||
          "Could not analyze this repository."
      );

    } finally {
      setLoading(false);
    }
  }


  return (
    <main className="app-shell">

      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />


      {/* Navbar */}

      <header className="navbar">

        <a
          className="brand"
          href="/"
          aria-label="CodeScope home"
        >
          <div className="brand-icon">
            <Orbit size={22} />
          </div>

          <div>
            <strong>CodeScope</strong>
            <span>AI Repository Auditor</span>
          </div>
        </a>


        <div className="nav-status">
          <span className="status-dot" />
          Analyzer online
        </div>

      </header>


      {/* Hero */}

      <section className="hero">

        <div className="hero-copy">

          <div className="hero-badge">
            <Sparkles size={15} />

            AI-powered repository intelligence
          </div>


          <h1>
            Understand a codebase

            <span>
              {" "}before touching the code.
            </span>
          </h1>


          <p>
            Paste a public GitHub repository and
            get a technical audit covering
            architecture, technologies, code
            health, risks, and actionable
            improvements.
          </p>

        </div>


        {/* Repository input */}

        <RepoForm
          value={repoUrl}
          onChange={setRepoUrl}
          onSubmit={handleSubmit}
          loading={loading}
        />


        {/* Error */}

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}


        {/* Features before analysis */}

        {!analysis && !loading && (

          <div className="feature-strip">

            <div>
              <Code2 size={17} />
              Static analysis
            </div>

            <div>
              <GitBranch size={17} />
              Architecture mapping
            </div>

            <div>
              <ShieldCheck size={17} />
              Risk detection
            </div>

            <div>
              <Activity size={17} />
              Health scoring
            </div>

          </div>

        )}


        {/* Loading */}

        {loading && (

          <div className="loading-card">

            <div className="scanner">
              <div className="scanner-line" />
            </div>

            <div>
              <strong>
                Analyzing repository
              </strong>

              <p>
                Scanning files, extracting
                structure, and generating the
                AI audit…
              </p>
            </div>

          </div>

        )}

      </section>


      {/* Dashboard */}

      {analysis && (

        <section className="dashboard">


          {/* Summary */}

          <div className="summary-panel panel">

            <div className="summary-kicker">
              <span>
                Analysis complete
              </span>

              <span className="success-dot" />
            </div>


            <h2>
              {analysis.projectName}
            </h2>


            <p className="purpose">
              {analysis.purpose}
            </p>


            <p className="summary-text">
              {analysis.summary}
            </p>

          </div>


          {/* Health */}

          <HealthGauge
            score={analysis.healthScore}
          />


          {/* Technology */}

          <TechStack
            technologies={
              analysis.technologies
            }
          />


          {/* Architecture */}

          <ArchitectureFlow
            architecture={
              analysis.architecture
            }
          />


          {/* Strengths */}

          <Strengths
            strengths={
              analysis.strengths
            }
          />


          {/* Components */}

          <KeyComponents
            components={
              analysis.components
            }
          />


          {/* Issues */}

          <Issues
            issues={
              analysis.issues
            }
          />


          {/* Recommendations */}

          <Recommendations
            recommendations={
              analysis.recommendations
            }
          />


          {/* Final assessment */}

          {analysis.finalAssessment && (

            <section
              className="
                panel
                final-assessment
                wide-panel
              "
            >

              <div className="section-heading">

                <span className="eyebrow">
                  AI conclusion
                </span>

                <h2>
                  Final assessment
                </h2>

              </div>


              <p>
                {analysis.finalAssessment}
              </p>

            </section>

          )}

        </section>

      )}


      {/* Footer */}

      <footer>

        <span>
          CodeScope AI
        </span>

        <span>
          Static evidence + AI interpretation
        </span>

      </footer>

    </main>
  );
}