# Mode Selection Examples

Real-world scenarios showing how the advisor helps choose between JSON outputs and strict tool use.

## Example 1: Invoice Data Extraction

**User Request:**
> "I need to extract invoice data from PDF documents and store it in our PostgreSQL database. The invoices contain line items, tax information, and customer details."

**Advisor Analysis:**
- **Goal:** Extract structured data from documents
- **Source:** PDF documents (unstructured)
- **Consumer:** PostgreSQL database (needs type-safe inserts)
- **Complexity:** Single-step extraction

**Recommended Mode:** JSON Outputs

**Reasoning:**
- This is a data extraction task (primary use case for JSON outputs)
- Single-step operation (extract → database)
- No multi-step agent workflow needed
- Schema compliance ensures database insert succeeds

**Next Step:**
Delegate to `json-outputs-implementer` to design invoice schema with line items, tax calculations, and customer info fields.

---

## Example 2: Travel Booking Agent

**User Request:**
> "Build an agent that can help users book complete travel itineraries. It should search for flights, compare options, book the chosen flight, find hotels near their destination, and book accommodation."

**Advisor Analysis:**
- **Goal:** Multi-step booking workflow
- **Source:** User conversation
- **Consumer:** Multiple external APIs (flights, hotels, booking systems)
- **Complexity:** Multi-tool agent workflow with sequential dependencies

**Recommended Mode:** Strict Tool Use

**Reasoning:**
- Multi-step workflow (search → compare → book → search → book)
- Multiple tools that need validated parameters
- Tool composition (flight booking influences hotel search location)
- Type-safe API calls are critical (booking with wrong parameters could charge cards incorrectly)

**Next Step:**
Delegate to `strict-tool-implementer` to design tool schemas for `search_flights`, `book_flight`, `search_hotels`, `book_hotel` with strict parameter validation.

---

## Example 3: Support Ticket Classification

**User Request:**
> "We receive thousands of support tickets daily. I need to automatically classify them by category (billing, technical, sales), priority level, and route them to the right team."

**Advisor Analysis:**
- **Goal:** Classification with routing
- **Source:** Support ticket text
- **Consumer:** Routing system + metrics dashboard
- **Complexity:** Single classification operation

**Recommended Mode:** JSON Outputs

**Reasoning:**
- Classification task (perfect for JSON outputs)
- Fixed output schema (category, priority, team, confidence)
- Single-step operation
- No tool execution needed (just classification output)

**Next Step:**
Delegate to `json-outputs-implementer` to design classification schema with enums for category/priority, confidence scoring, and routing metadata.

---

## Example 4: Database Query Agent

**User Request:**
> "I want an agent that can answer questions about our sales data. It should translate natural language questions into SQL, execute the queries safely, and return formatted results."

**Advisor Analysis:**
- **Goal:** Natural language → SQL query execution
- **Source:** User questions in natural language
- **Consumer:** Database + user (formatted results)
- **Complexity:** Tool execution with type-safe parameters + structured output

**Recommended Mode:** Both (Hybrid Approach)

**Reasoning:**
- Tool use for SQL execution: Need `execute_sql` tool with validated query parameters (prevent SQL injection)
- JSON outputs for response: Want structured results formatted consistently
- Two distinct phases: query generation/execution → result formatting

**Next Step:**
1. First: Delegate to `strict-tool-implementer` for `execute_sql` tool with strict validation
2. Then: Delegate to `json-outputs-implementer` for result formatting schema

---

## Example 5: Resume Parser

**User Request:**
> "Parse resumes in various formats (PDF, DOCX, plain text) and extract structured information: personal details, work experience, education, skills. Store in our ATS database."

**Advisor Analysis:**
- **Goal:** Extract structured data from documents
- **Source:** Resume documents (various formats)
- **Consumer:** ATS (Applicant Tracking System) database
- **Complexity:** Single extraction operation

**Recommended Mode:** JSON Outputs

**Reasoning:**
- Data extraction from unstructured documents
- Well-defined output schema (resume has standard sections)
- No tool execution needed
- Database insertion requires type-safe data

**Next Step:**
Delegate to `json-outputs-implementer` to design resume schema with nested objects for work experience, education, and skills arrays.

---

## Example 6: API Response Formatter

**User Request:**
> "Our API needs to return consistent JSON responses. Sometimes Claude generates the response data, and I need it formatted exactly to our API spec with status, data, errors, and metadata fields."

**Advisor Analysis:**
- **Goal:** Format API responses consistently
- **Source:** Claude-generated content
- **Consumer:** API clients (web/mobile apps)
- **Complexity:** Response formatting

**Recommended Mode:** JSON Outputs

**Reasoning:**
- Response formatting task
- Fixed API schema that must be followed exactly
- No tool execution
- Consistency is critical for API clients

**Next Step:**
Delegate to `json-outputs-implementer` to design API response schema matching the spec, with proper error handling structure.

---

## Example 7: Research Assistant Agent

**User Request:**
> "Build an agent that researches topics by searching the web, reading articles, extracting key facts, cross-referencing sources, and generating a comprehensive research report."

**Advisor Analysis:**
- **Goal:** Multi-step research workflow
- **Source:** Web (via search tools, article fetchers)
- **Consumer:** User (research report)
- **Complexity:** Multi-tool workflow with sequential and parallel steps + structured output

**Recommended Mode:** Both (Hybrid Approach)

**Reasoning:**
- Research phase: Need tools (`search_web`, `fetch_article`, `extract_facts`) with strict validation
- Report phase: Need structured report output (JSON outputs)
- Complex workflow with multiple stages

**Next Step:**
1. First: Delegate to `strict-tool-implementer` for research tools
2. Then: Delegate to `json-outputs-implementer` for final report schema

---

## Example 8: Form Data Extraction

**User Request:**
> "Users upload scanned forms (insurance claims, applications, etc.). Extract all form fields into a structured format for processing."

**Advisor Analysis:**
- **Goal:** Extract form data
- **Source:** Scanned form images
- **Consumer:** Processing system
- **Complexity:** Single extraction

**Recommended Mode:** JSON Outputs

**Reasoning:**
- Image data extraction
- Form has known structure (predefined fields)
- No tool execution
- Type-safe data needed for downstream processing

**Next Step:**
Delegate to `json-outputs-implementer` to design form schema matching the expected fields with proper types.

---

## Decision Patterns Summary

| Scenario Type | Recommended Mode | Key Indicator |
|---------------|------------------|---------------|
| Data extraction | JSON Outputs | "Extract X from Y" |
| Classification | JSON Outputs | "Classify/categorize X" |
| API formatting | JSON Outputs | "Format response as X" |
| Report generation | JSON Outputs | "Generate report with X structure" |
| Multi-tool workflow | Strict Tool Use | "Search, then book, then..." |
| Agent with tools | Strict Tool Use | "Agent that can call X, Y, Z" |
| Type-safe function calls | Strict Tool Use | "Validate parameters for X" |
| Complex agents | Both | "Research then report" / "Query then format" |

---

## Common Misconceptions

### ❌ "I need reliable JSON, so I should use strict tool use"

**Correction:** Use JSON outputs for reliable JSON responses. Strict tool use is for tool **parameters**, not Claude's response format.

### ❌ "My agent just needs one tool, so I should use JSON outputs"

**Correction:** Even a single-tool agent benefits from strict tool use if the tool needs parameter validation. Mode choice is about **what** you're validating, not **how many** tools.

### ❌ "I can use both modes for the same thing"

**Correction:** Each mode has a specific purpose:
- JSON outputs: Claude's response format
- Strict tool use: Tool input validation

They solve different problems and can be combined when you need both.

---

**See Also:**
- [JSON Outputs Implementer Examples](../../json-outputs-implementer/examples/)
- [Strict Tool Implementer Examples](../../strict-tool-implementer/examples/)
