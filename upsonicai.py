import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from upsonic import Agent, Task, ObjectResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Code Review & Issue Fixer")

# Initialize the AI agent
code_review_agent = Agent("AI Code Review & Issue Fixer", model="azure/gpt-4o", reflection=True)

# MCP Server Configurations
class GitHubMCP:
    command = "npx"
    args = ["-y", "@modelcontextprotocol/server-github"]
    env = {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")}

class SentryMCP:
    command = "python"
    args = ["-m", "mcp_server_sentry", "--auth-token", os.getenv("SENTRY_AUTH_TOKEN")]

# Define response format
class CodeReviewResponse(ObjectResponse):
    repository: str
    issues: list[str]
    recommendations: list[str]

class SentryIssuesResponse(ObjectResponse):
    sentry_issues: list[str]
    recommended_fixes: list[str]

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Code Review & Issue Fixer</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            #result {
                max-height: 300px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body class="bg-gray-100 flex justify-center items-center h-screen">
        <div class="bg-white p-8 rounded-lg shadow-lg w-96">
            <h1 class="text-2xl font-bold text-center mb-4">🚀 AI Code Review & Issue Fixer</h1>
            <input id="repo_url" type="text" placeholder="GitHub Repository URL" class="w-full p-2 border rounded mb-4">
            <button onclick="reviewCode()" class="bg-blue-500 text-white px-4 py-2 rounded w-full">Analyze Code</button>
            <button onclick="analyzeSentry()" class="bg-red-500 text-white px-4 py-2 rounded w-full mt-2">Analyze Sentry Logs</button>
            <div id="result" class="mt-4 text-sm"></div>
        </div>
        <script>
            async function reviewCode() {
                const repoUrl = document.getElementById("repo_url").value;
                if (!repoUrl) {
                    alert("Please enter a repository URL.");
                    return;
                }
                const response = await fetch(`/review_code?repo_url=${repoUrl}`);
                const data = await response.json();
                document.getElementById("result").innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }
            async function analyzeSentry() {
                const response = await fetch(`/analyze_sentry`);
                const data = await response.json();
                document.getElementById("result").innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }
        </script>
    </body>
    </html>
    """


@app.get("/review_code")
async def review_code(repo_url: str):
    """Analyze a GitHub repository for code quality issues and security vulnerabilities."""
    review_task = Task(
        f"Analyze the repository {repo_url} for potential issues and security vulnerabilities.",
        tools=[GitHubMCP],
        response_format=CodeReviewResponse
    )
    code_review_agent.do(review_task)
    response = review_task.response
    
    if not response:
        return {"error": "Failed to analyze the repository."}
    
    return {
        "repository": response.repository,
        "issues": response.issues,
        "recommendations": response.recommendations
    }

@app.get("/analyze_sentry")
async def analyze_sentry():
    """Retrieve Sentry error logs and suggest fixes."""
    sentry_task = Task(
        "Retrieve and analyze recent Sentry error logs, providing recommended fixes.",
        tools=[SentryMCP],
        response_format=SentryIssuesResponse
    )
    code_review_agent.do(sentry_task)
    response = sentry_task.response
    
    if not response:
        return {"error": "Failed to analyze Sentry logs."}
    
    return {
        "sentry_issues": response.sentry_issues,
        "recommended_fixes": response.recommended_fixes
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
