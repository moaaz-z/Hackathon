CodeScope Interactive UI Update

Replace/add these files in your existing frontend:

frontend/src/App.jsx
frontend/src/styles.css
frontend/src/lib/api.js
frontend/src/hooks/useCountUp.js
frontend/src/components/RepoForm.jsx
frontend/src/components/HealthGauge.jsx
frontend/src/components/RepositoryVisuals.jsx
frontend/src/components/AuditVisuals.jsx
frontend/src/components/AnalysisPipeline.jsx
frontend/src/components/ArchitectureFlow.jsx
frontend/src/components/TechStack.jsx
frontend/src/components/Findings.jsx
frontend/src/components/ComponentsAndRecommendations.jsx
frontend/vite.config.js

Then run:
cd frontend
npm run build
npm run dev

No new npm packages are required beyond lucide-react, which the project already uses.
