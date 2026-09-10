import { GitBranch, Search } from "lucide-react";

export default function RepoForm({
  value,
  onChange,
  onSubmit,
  loading,
}) {
  return (
    <form className="repo-form" onSubmit={onSubmit}>
      <div className="repo-input-wrap">
        <GitBranch size={20} aria-hidden="true" />

        <input
          type="url"
          placeholder="https://github.com/owner/repository"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          required
          aria-label="GitHub repository URL"
        />
      </div>

      <button className="analyze-button" disabled={loading}>
        <Search size={18} aria-hidden="true" />
        {loading ? "Analyzing…" : "Analyze Repository"}
      </button>
    </form>
  );
}