# PLWRAP - asyncpg

`PLWRAP` is an easy to use wrapper for Postgresql orientend on `jdbi`. It is **not an ORM**, instead it allows to run SQL queries and dump the result into consistent Python Objects (Dataclasses are prefered)

> **SQL is awesome. Try to remember! :-)**

## Sanic integration
When used together with sanic, `plwrap` uses the sanic logging framework for debugging queries


## Examples
```python
import asyncio
from dataclasses import dataclass
import asyncpg
from plwrap import query, one

@dataclass
class User:
    """ User store """
    id: str
    email: str
    pwhash: str


class UserDAO:
    """ some sort of database access object """
    @staticmethod
    @one
    @query(User)
    async def get_by_email(email: str) -> User:
        """ Tries to get a user based on its email (unique) """
        return "select id, email, pwhash from users where email = $1", email


async def main():
    db_pool = await asyncpg.create_pool(database="what", user="ever")

    user = await UserDAO.get_by_email(db_pool, "me@xvzf.tech")
    print(user)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
```