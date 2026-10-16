import asyncio
import json
from typing import AsyncIterator
from uuid import uuid4


class EventManager:
    def __init__(self):
        self._clients: dict[str, asyncio.Queue[dict]] = {}

    @property
    def clients(self) -> tuple[str, ...]:
        return tuple(self._clients)

    def is_connected(self, client_id: str) -> bool:
        return client_id in self._clients

    async def subscribe(self) -> AsyncIterator[str]:
        client_id = uuid4().hex
        queue: asyncio.Queue[dict] = asyncio.Queue()

        self._clients[client_id] = queue

        try:
            yield (
                "event: ready\n"
                f"data: {json.dumps({'client': client_id})}\n\n"
            )

            while True:
                try:
                    command = await asyncio.wait_for(
                        queue.get(),
                        timeout=20,
                    )

                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
                    continue

                yield f"data: {json.dumps(command)}\n\n"

        finally:
            self._clients.pop(client_id, None)

    async def send(self, client_id: str, command: str, **data) -> bool:
        queue = self._clients.get(client_id)

        if queue is None:
            return False

        await queue.put({
            "command": command,
            **data,
        })

        return True

    async def broadcast(self, command: str, **data) -> int:
        message = {
            "command": command,
            **data,
        }

        for queue in self._clients.values():
            await queue.put(message.copy())

        return len(self._clients)