import { GitBranch, Loader2, Search } from "lucide-react";

export default function RepoForm({ value, onChange, onSubmit, loading }) {
  return (
    <form className="repo-form" onSubmit={onSubmit}>
      <label className="repo-input-wrap">
        <GitBranch size={19} />
        <input
          type="url"
          required
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder="https://github.com/owner/repository"
          aria-label="GitHub repository URL"
        />
      </label>

      <button className="analyze-button" disabled={loading} type="submit">
        {loading ? (
          <Loader2 className="button-spinner" size={18} />
        ) : (
          <Search size={18} />
        )}
        {loading ? "Analyzing…" : "Analyze Repository"}
      </button>
    </form>
  );
}
