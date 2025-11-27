# db.py
import os
import asyncpg
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definida. Veja .env.example")

_pool: Optional[asyncpg.pool.Pool] = None

async def init_db_pool(min_size: int = 1, max_size: int = 10):
    global _pool
    if _pool is None:
        # se precisar forçar SSL, passe ssl=ssl_ctx aqui
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=min_size, max_size=max_size)
    return _pool

async def close_db_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None

def _row_to_dict(rec: asyncpg.Record) -> Dict[str, Any]:
    d = dict(rec)
    for k, v in list(d.items()):
        if hasattr(v, "isoformat"):
            d[k] = v.isoformat()
        else:
            # jsonb já vem como dict/list; deixar como está
            d[k] = v
    return d

async def fetch_audit_logs(since_id: Optional[int] = None, limit: int = 100, order: str = "asc") -> List[Dict[str, Any]]:
    """
    Busca registros da tabela audit_logs.
    - since_id: retorna registros com id > since_id (incremental)
    - limit: máximo de registros
    - order: "asc" ou "desc"
    """
    pool = await init_db_pool()
    order_sql = "ASC" if order.lower() == "asc" else "DESC"

    if since_id is None:
        # caso sem since_id: usar $1 para LIMIT
        q = f"""
            SELECT id, timestamp, action, status, email, email_raw, ip,
                   user_agent, headers, request_body, threats, reason,
                   user_id, response_time, db_query_time, request_size,
                   method, protocol, user_exists, error_message, error_stack
            FROM audit_logs
            ORDER BY id {order_sql}
            LIMIT $1
        """
        params = (limit,)
    else:
        # caso com since_id: usar $1 = since_id, $2 = limit
        q = f"""
            SELECT id, timestamp, action, status, email, email_raw, ip,
                   user_agent, headers, request_body, threats, reason,
                   user_id, response_time, db_query_time, request_size,
                   method, protocol, user_exists, error_message, error_stack
            FROM audit_logs
            WHERE id > $1
            ORDER BY id {order_sql}
            LIMIT $2
        """
        params = (since_id, limit)

    async with pool.acquire() as conn:
        rows = await conn.fetch(q, *params)

    return [_row_to_dict(r) for r in rows]
