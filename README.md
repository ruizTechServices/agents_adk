graph TD
    subgraph "Project: ruiztechservices/agents_adk"
        A[giovanni_agent] --> B(Playwright Tools: navigate, click, etc.);
        C[multi_tool_agent] --> D(Data Tools: get_weather, get_current_time);
        E[Unused Services] --> F[grok_service.py];
        E --> G[openai_service.py];
    end