from fastmcp import FastMCP
 
# Create MCP server
mcp = FastMCP("Jira MCP Server")
 
@mcp.tool()
def jira_create_issue(
    summary: str,
    description: str = "",
    issue_type: str = "Task",
    project_key: str = "CHAT"
) -> str:
    """
    Create a Jira issue.
 
    Args:
        summary: Issue title/summary
        description: Issue description
        issue_type: Type of issue (Task, Bug, Story, etc.)
        project_key: The Jira project key (default: KAN)
    """
    import httpx
    import os
 
    jira_host = os.environ.get("JIRA_HOST", "https://deepakjohnart.atlassian.net")
    jira_email = os.environ.get("JIRA_EMAIL")
    jira_token = os.environ.get("JIRA_API_TOKEN")
 
    if not jira_email or not jira_token:
        return "Error: Missing JIRA_EMAIL or JIRA_API_TOKEN environment variables"
 
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        }
    }
 
    response = httpx.post(
        f"{jira_host}/rest/api/2/issue",
        json=payload,
        auth=(jira_email, jira_token),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 201:
        data = response.json()
        return f"Created issue {data['key']}: {jira_host}/browse/{data['key']}"
    else:
        return f"Error: {response.status_code} - {response.text}"
 
# Export for FastMCP Cloud - try http_app method
app = mcp.http_app()
