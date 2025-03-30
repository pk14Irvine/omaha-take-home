```mermaid
    sequenceDiagram
        actor us as User
        participant fe as Frontend
        participant be as Backend
        participant pg as Postgres

        us->>fe: refresh dashboard
        fe->>be: fetch data
        be->>pg: query for data
        pg-->>be: query response
        be-->>fe: return response
        fe-->>us: hydrate ui
```
