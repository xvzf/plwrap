# -*- coding: utf-8 -*-
"""
    plwrap.__init__
    ~~~~~~~~~~~~~~

    plwrap is a simple wrapper for mapping database queries to Python Dataclasses
    in places where an ORM is just overkill or explicitly not wanted

    :copyright: (c) 2019, Matthias Riegler <me@xvzf.tech>
    :license: GPLv3, see LICENSE.md for more details
"""

import logging
from dataclasses import dataclass
from functools import wraps

import asyncpg

logger = None
try:
    # Try to import sanic and use its logger but fallback to the python default
    # logging implementation
    from sanic.log import logger as sanic_logger
    logger = sanic_logger
except:
    import logging
    logger = logging.getLogger(__name__)


def query(Target: dataclass):
    """ Maps a SQL query to a list of dataclasses """
    def decorator(query):
        """ Decorator function """
        @wraps(query)
        async def wrapper(db: asyncpg.pool.Pool, *args, **kwargs) -> dataclass:
            """ Actual wrapper, args and kwargs are passed directly to
            the asyncpg fetch function

            @params db: asyncpg connection pool for running the query
            @params args: Passed on from original function call args
            @params kwargs: Passed on from original function call args
            """
            async with db.acquire() as conn:
                sql_query = await query(*args, **kwargs)
                logging.debug(f"Running SQL query: {sql_query}")
                # Looks dirty but the performance is best when using a list
                # comprehension
                #
                # Run SQL Query -> convert each result to a dictionary
                # -> map to dataclass
                return [Target(**dict(r)) for r in await conn.fetch(*sql_query)]
            # We should never get to here as the exception should be passed but
            # let's be sure :-)
            return None

        return wrapper

    return decorator


def one(query):
    """ Can be used in conjuction with `query` to separate an array of dataclasses
    to get just one
    """
    @wraps(query)
    async def wrapper(*args, **kwargs):
        """ Return vector is of length 1 e.g. when running a `limit 1` query  """
        res = await query(*args, **kwargs)
        return res[0] if res else None
    return wrapper
