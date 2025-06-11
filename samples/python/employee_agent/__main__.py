import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from pathlib import Path

from .agent_executor import EmployeeAgentExecutor
from .create_db import DB_PATH, create_db


if __name__ == "__main__":
    skill = AgentSkill(
        id="employee_lookup",
        name="Lookup employees",
        description="Query employee records by country",
        tags=["employees"],
        examples=["Show employees from España"],
    )

    agent_card = AgentCard(
        name="Employee Lookup Agent",
        description="Returns employee info from a SQLite database",
        url="http://0.0.0.0:9999/",
        version="0.1.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    db_path = DB_PATH
    if not db_path.exists():
        create_db()
    request_handler = DefaultRequestHandler(
        agent_executor=EmployeeAgentExecutor(str(db_path)),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host="0.0.0.0", port=9999)
