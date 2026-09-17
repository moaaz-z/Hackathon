const API_BASE_URL = "https://hackathon-production-cb4d.up.railway.app";
function getErrorMessage(detail) {
  if (!detail) return "Request failed.";
  if (typeof detail === "string") return detail;

  if (Array.isArray(detail)) {
    return detail
      .map((item) => (typeof item === "string" ? item : item?.msg || JSON.stringify(item)))
      .join(", ");
  }

  if (typeof detail === "object") return detail?.msg || JSON.stringify(detail);
  return "Request failed.";
}

export async function analyzeRepository(repoUrl) {
  const response = await fetch(`${API_BASE_URL}/repository/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: repoUrl }),
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    throw new Error(
      getErrorMessage(payload?.detail) || `Request failed with status ${response.status}`,
    );
  }

  return payload;
}

function getRepositoryName(repositoryUrl) {
  if (!repositoryUrl) return "";
  try {
    const url = new URL(repositoryUrl);
    return url.pathname.split("/").filter(Boolean).at(-1) || "";
  } catch {
    return "";
  }
}

export function normalizeAnalysis(payload) {
  const ai = payload?.ai_review || {};
  const staticAnalysis = payload?.static_analysis || {};

  return {
    repositoryUrl: payload?.repository_url || "",
    staticAnalysis,
    projectName:
      staticAnalysis?.repository?.name ||
      staticAnalysis?.name ||
      getRepositoryName(payload?.repository_url) ||
      "Repository Analysis",
    purpose: ai.project_purpose || "Purpose not provided.",
    summary: ai.summary || "No summary returned.",
    technologies: Array.isArray(ai.technology_stack) ? ai.technology_stack : [],
    architecture: { description: ai.architecture || "" },
    healthScore: Number(ai.health_score ?? 0),
    strengths: Array.isArray(ai.strengths) ? ai.strengths : [],
    weaknesses: Array.isArray(ai.weaknesses) ? ai.weaknesses : [],
    risks: Array.isArray(ai.risks) ? ai.risks : [],
    issues: Array.isArray(ai.issues) ? ai.issues : [],
    components: Array.isArray(ai.key_components) ? ai.key_components : [],
    recommendations: Array.isArray(ai.recommendations) ? ai.recommendations : [],
    finalAssessment: ai.final_assessment || "",
  };
}
