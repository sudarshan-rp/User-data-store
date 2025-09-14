import asyncpg
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()  # Load .env file if present

DB_HOST = os.getenv("POSTGRES_HOST", "db")  # Use localhost for local development and db for docker-compose
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "testdb")

pool: Optional[asyncpg.Pool] = None

async def connect_to_db():
    global pool
    pool = await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        min_size=1,
        max_size=5
    )
    print("✅ Database connection pool created")

async def disconnect_from_db():
    global pool
    if pool:
        await pool.close()
        print("🛑 Database connection pool closed")

async def create_tables():
    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
        """)

def get_db_pool() -> asyncpg.Pool:
    if not pool:
        raise RuntimeError("Database pool is not initialized")
    return pool

async def db_create_user(conn, name: str, email: str):
    query = "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email"
    return await conn.fetchrow(query, name, email)

async def db_get_user_by_id(conn, user_id: int):
    query = "SELECT id, name, email FROM users WHERE id=$1"
    return await conn.fetchrow(query, user_id)

async def db_list_users(conn):
    query = "SELECT id, name, email FROM users"
    return await conn.fetch(query)
