# CodeScope

CodeScope is an AI-powered GitHub repository analyzer that helps developers quickly understand unfamiliar codebases.

Paste a public GitHub repository URL and CodeScope will clone the repository, perform static code analysis, extract important technical information, and use Gemini to generate a structured technical review.

Instead of only summarizing the repository, CodeScope highlights architecture, technologies, code quality, risks, important components, and recommended improvements.

---

## Features

- Analyze public GitHub repositories
- Detect programming languages and frameworks
- Extract dependencies and project structure
- Detect functions, classes, imports, and important files
- Analyze Python code complexity
- Detect test files
- Count TODO and FIXME markers
- Identify large or complex files
- Generate an AI-powered project summary
- Explain the project architecture
- Identify key components
- Highlight strengths and weaknesses
- Detect engineering risks
- Generate prioritized recommendations
- Calculate a repository health score
- Visualize repository statistics and architecture

---

## How It Works

```text
GitHub Repository URL
        ↓
Clone Repository
        ↓
Static Code Analyzer
        ↓
Repository Facts
        ↓
Important File Selection
        ↓
Context Builder
        ↓
Gemini API
        ↓
Structured Technical Review
        ↓
React Dashboard
```

CodeScope separates static analysis from AI interpretation.

```text
Static Analyzer → What exists in the repository?
Gemini          → What does this information mean?
Frontend        → How should it be presented?
```

This approach makes the analysis more reliable because factual information such as file count, dependencies, complexity, and tests is calculated directly from the repository instead of being guessed by the AI model.

---

## Example Analysis

CodeScope can generate information such as:

```text
Project Purpose
E-commerce backend for managing users, products, orders, and payments.

Technology Stack
Python • FastAPI • SQLAlchemy • PostgreSQL • Pytest

Architecture
API Layer → Service Layer → Database Layer

Repository Health
76 / 100

High Priority Issue
services/payment.py

Reason:
process_payment() has high cyclomatic complexity.

Recommendation:
Split the payment workflow into smaller functions and add integration tests.
```

---

## Tech Stack

### Backend

- Python
- FastAPI
- Uvicorn
- GitPython
- Pydantic
- Radon
- Python AST
- Google GenAI SDK
- python-dotenv

### Frontend

- React
- Vite
- JavaScript
- CSS
- Lucide React

### AI

- Google Gemini API

---

## Static Analysis

The backend analyzes repository files without executing them.

It can extract:

- File count
- Directory structure
- Lines of code
- Programming languages
- Functions
- Classes
- Imports
- Dependencies
- Frameworks
- Test files
- TODO / FIXME markers
- Code complexity
- Important files
- Internal module relationships

For Python repositories, CodeScope uses Python's `ast` module to inspect the source code structure.

Cyclomatic complexity is calculated using `radon`.

---

## AI Analysis

After static analysis, the repository facts are converted into structured context and sent to Gemini.

Gemini generates:

- Project purpose
- Project summary
- Technology stack
- Architecture explanation
- Key components
- Strengths
- Weaknesses
- Risks
- Issues
- Recommendations
- Health score
- Final assessment

The AI is instructed to only use evidence extracted from the repository and avoid inventing unsupported information.

---

## Project Structure

```text
Hackathon/
│
├── src/
│   └── hackathon/
│       ├── main.py
│       ├── models/
│       │   └── schemas.py
│       ├── services/
│       │   ├── github_service.py
│       │   ├── scanner.py
│       │   ├── parser.py
│       │   ├── dependency_analyzer.py
│       │   ├── test_analyzer.py
│       │   ├── complexity_analyzer.py
│       │   ├── importance_analyzer.py
│       │   ├── context_builder.py
│       │   ├── analyzer.py
│       │   └── ai_service.py
│       └── ...
│
├── tests/
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── styles.css
│       ├── lib/
│       │   └── api.js
│       └── components/
│           ├── RepoForm.jsx
│           ├── HealthGauge.jsx
│           ├── ArchitectureFlow.jsx
│           ├── RepositoryVisuals.jsx
│           ├── TechStack.jsx
│           ├── Findings.jsx
│           └── ComponentsAndRecommendations.jsx
│
├── .env
├── pyproject.toml
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Hackathon
```

### 2. Backend Setup

Install Python dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model
```

Never commit your `.env` file.

Start the backend:

```bash
uv run uvicorn hackathon.main:app --reload --app-dir src
```

The API will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
```

Create:

```text
frontend/.env
```

Add:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## API

### Analyze Repository

```http
POST /repository/analyze
```

Request:

```json
{
  "url": "https://github.com/owner/repository"
}
```

Example response:

```json
{
  "repository_url": "https://github.com/owner/repository",
  "static_analysis": {},
  "ai_review": {
    "project_purpose": "...",
    "summary": "...",
    "technology_stack": [],
    "architecture": "...",
    "key_components": [],
    "strengths": [],
    "weaknesses": [],
    "risks": [],
    "recommendations": [],
    "issues": [],
    "health_score": 80,
    "final_assessment": "..."
  }
}
```

---

## Testing

Run the backend test suite with:

```bash
uv run pytest -q
```

Current test coverage includes:

- Repository API validation
- GitHub URL handling
- Static analyzer
- Python parsing
- Repository cleanup
- AI response validation
- Error handling

---

## Security

Repositories are treated as untrusted input.

CodeScope does **not** automatically:

- Execute repository source code
- Run shell scripts
- Install repository dependencies
- Run `npm install`
- Run `pip install`
- Execute binaries
- Run Dockerfiles
- Run repository tests

The analyzer only reads and parses repository files.

The Gemini API key is stored only in the backend `.env` file and is never exposed to the React frontend.

---

## Why CodeScope?

Understanding an unfamiliar repository can take hours.

Developers usually need to manually inspect:

- README files
- folder structure
- dependencies
- entry points
- services
- models
- tests
- architecture
- complex modules

CodeScope combines static analysis with AI interpretation to make this process faster.

Instead of asking:

> "What files are in this repository?"

CodeScope helps answer:

> "What does this project do, how is it structured, what are the important parts, and what should be improved?"

---

## Future Improvements

Possible future features include:

- Multi-language parsing with Tree-sitter
- Dependency graph visualization
- Code coupling analysis
- Test coverage integration
- GitHub OAuth
- Private repository analysis
- Change impact analysis
- Pull request analysis
- Security vulnerability detection
- Historical repository analysis
- CI/CD integration

---

## Team

Built during a hackathon by a 3-person team working on:

- Backend & GitHub integration
- Static code analysis
- AI integration & frontend

---

## License

Add your preferred license here.