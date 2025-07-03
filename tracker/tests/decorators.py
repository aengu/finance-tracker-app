import time
from functools import wraps
from django.db import connection, reset_queries
from django.conf import settings

def query_debugger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not settings.DEBUG:
            # DEBUG=False이면 동작하지 않도록 안전 장치
            return func(*args, **kwargs)
        reset_queries()
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        total_time = end - start
        num_queries = len(connection.queries)

        print(f"\n🔍 Function: {func.__name__}")
        print(f"🕒 Time: {total_time:.4f}s")
        print(f"📦 Query Count: {num_queries}")

        # for i, query in enumerate(connection.queries, start=1):
        #     print(f"  {i}. {query['sql']} ({query['time']}s)")

        return result
    return wrapper