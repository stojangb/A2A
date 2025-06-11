# Employee Lookup Agent

This sample demonstrates a minimal A2A agent that queries a SQLite database of employees.
The database file is not included in the repository and will be generated locally.

## Setup

1. Install dependencies:
   ```bash
   pip install a2a-sdk uvicorn
   ```
2. Create the database (optional, the server will create it on first run):
   ```bash
   python create_db.py
   ```
3. Start the server:
   ```bash
   python -m employee_agent
   ```

The agent exposes its capabilities in `.well-known/agent.json` and listens on port `9999`.
