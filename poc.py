import asyncio
import asyncpg
from dataclasses import dataclass
from datetime import datetime
from functools import wraps


def map(Target):
    """ Maps SQL queries to dataclasses """
    def decorator(query):

        @wraps(query)
        async def wrapper(conn, *args, **kwargs):
            records = await conn.fetch(await query())
            return [Target(**dict(r)) for r in records]

        return wrapper

    return decorator


@dataclass
class Task:
    """ Container """
    id: int
    created: datetime
    deadline: datetime
    name: str
    description: str
    fulfilled: datetime
    project_stage: int
    team: int


class TaskDAO:
    """ Data access class """
    @map(Task)
    async def getall():
        return "select * from task"


async def run():
    conn = await asyncpg.connect(
        user="owlkeeper",
        password="owlkeeper",
        database="owlkeeper",
        host="127.0.0.1"
    )

    values = await TaskDAO.getall(conn)
    print(values)
    await conn.close()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


if __name__ == "__main__":
    main()
