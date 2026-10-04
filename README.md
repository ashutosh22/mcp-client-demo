# mcp-client-demo

[ FRONTEND LAYER ]          ➡   [ MIDDLEWARE / ORCHESTRATION LAYER ] ➡ [ CAPABILITY LAYER ]
-----------------                -----------------------------------     --------------------
  User Interface                  AI Client Router    LLM Gateway          MCP Server (Docker)
(React / Web / App)              (Python / FastAPI)   (Ollama / OpenAI)    (Data Utility Cluster)
        │                                 │                   │                      │
        ▼                                 ▼                   ▼                      ▼
 ┌──────────────┐                 ┌───────────────┐   ┌───────────────┐      ┌───────────────┐
 │ Custom Chat  │  ───(HTTPS)───► │  LangGraph /  │◄─►│ Enterprise    │      │ Weather/Data  │
 │  Dashboard   │                 │ Custom Client │   │ AI Model Mesh │      │  MCP Service  │
 └──────────────┘                 └───────────────┘   └───────────────┘      └───────────────┘
                                          │                                          ▲
                                          └───────(Secure HTTP / SSE Stream)─────────┘