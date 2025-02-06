21-Day Agent Series: Day 11 AGENT : AI Code Review & Issue Fixer

AI Code Review & Issue Fixer
This agent is part of the "A New AI Agent Every Day!" Series - Day 11/21 - AI Code Review & Issue Fixer 🛠🚀 This AI agent analyzes code repositories, detects potential security vulnerabilities, reviews code quality, and suggests fixes based on Sentry error logs using Sentry and GitHub MCP servers!

## Installation

### Prerequisites
- Python 3.9 or higher
- Git
- Virtual environment (recommended)

### Steps
Don't forget to download nodejs for MCP

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt

   ```

3. Create a `.env` file in the root directory and configure it as follows:

   ```env
   AZURE_OPENAI_ENDPOINT="your_azure_openai_endpoint"
   AZURE_OPENAI_API_VERSION="your_azure_openai_api_version"
   AZURE_OPENAI_API_KEY="your_azure_openai_api_key"
   GITHUB_PERSONAL_ACCESS_TOKEN="YOUR_GITHUB_TOKEN"
   SENTRY_AUTH_TOKEN="YOUR_SENTRY_TOKEN"
   ```

## Running the Application

Start the FastAPI server:

```bash
uvicorn upsonicai:app --reload
```

Open the UI in your browser:

```
http://127.0.0.1:8000/
```

## MCP Configuration

Modify your MCP configuration to include GitHub and Sentry:

```json
"mcpServers": {
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_TOKEN"
    }
  },
  "sentry": {
    "command": "python",
    "args": ["-m", "mcp_server_sentry", "--auth-token", "YOUR_SENTRY_TOKEN"]
  }
}
```

## How It Works
- Fetches recent commits from GitHub/GitLab repositories
- Analyzes code quality and detects security vulnerabilities
- Retrieves error logs from Sentry
- Provides actionable insights and fixes for detected issues

## API Documentation
Interactive API docs are available at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

