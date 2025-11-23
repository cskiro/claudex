# MCP Capability Deep-Dives

## Tools: AI-Callable Functions

**When to use**: AI needs to perform actions or fetch computed data

### Structure
- **Name**: Descriptive verb (e.g., "search_docs", "create_ticket")
- **Description**: Clear explanation (AI uses this to decide when to call)
- **Schema**: Input parameters with types and descriptions
- **Handler**: Async function returning structured content

### Example Tool Types
- Data fetching: "get_user_data", "search_products"
- Computation: "calculate_metrics", "analyze_sentiment"
- Actions: "send_email", "create_issue", "update_status"
- External APIs: "search_web", "translate_text"

---

## Resources: Data Exposure

**When to use**: AI needs to read data without side effects

### Structure
- **URI**: Pattern like "scheme://path/{param}"
- **MIME type**: Helps AI understand content format
- **Handler**: Returns content (text, JSON, binary)

### Example Resource Types
- File contents: "file:///path/to/file.txt"
- Database records: "db://users/{user_id}"
- API responses: "api://endpoint/{id}"
- Search results: "search://query/{term}"

---

## Prompts: Specialized Workflows

**When to use**: Provide templates for common tasks

### Structure
- **Name**: Descriptive identifier
- **Description**: When to use this prompt
- **Arguments**: Parameters to customize
- **Template**: Pre-filled prompt text

### Example Prompt Types
- Code review: Pre-filled checklist
- Bug triage: Structured investigation steps
- Documentation: Template with sections

---

## Common Server Patterns

### Database Integration Server
**Tools**: query_database, get_schema, list_tables
**Resources**: db://tables/{table}/schema
**Example**: PostgreSQL, MySQL, MongoDB access

### API Wrapper Server
**Tools**: call_endpoint, search_api, get_resource
**Resources**: api://endpoints/{endpoint}
**Example**: Wrap REST APIs for AI consumption

### File System Server
**Resources**: file:///{path}
**Tools**: search_files, read_file, list_directory
**Example**: Secure file access with permissions

### Workflow Automation Server
**Tools**: trigger_workflow, check_status, get_results
**Prompts**: workflow_templates
**Example**: CI/CD, deployment, data pipelines
