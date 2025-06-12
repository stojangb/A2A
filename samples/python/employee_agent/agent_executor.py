from __future__ import annotations

import sqlite3
from typing import Iterable, Tuple

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


class EmployeeAgentExecutor(AgentExecutor):
    """Agent that queries a SQLite database."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _query_db(self, country: str | None) -> Iterable[Tuple[str, str, str]]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        if country:
            cur.execute(
                "SELECT nombre, pais, cargo FROM employees WHERE pais = ?",
                (country,),
            )
        else:
            cur.execute("SELECT nombre, pais, cargo FROM employees")
        results = cur.fetchall()
        conn.close()
        return results

    def _extract_country(self, text: str) -> str | None:
        lower = text.lower()
        if "espa" in lower:
            return "España"
        if "fran" in lower:
            return "Francia"
        return None

    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        content = context.message.content or ""
        country = self._extract_country(content)
        rows = self._query_db(country)
        if not rows:
            result = "No results found."
        else:
            result = "\n".join(f"{n} - {c} ({p})" for n, c, p in rows)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception("cancel not supported")
