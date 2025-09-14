# services/user_service.py
from backend.models.user import UserCreate, UserRead
from backend.db.database import get_db_pool, db_create_user, db_get_user_by_id, db_list_users
from typing import List

class UserService:
    async def create_user(self, user: UserCreate) -> UserRead:
        pool = get_db_pool()
        async with pool.acquire() as conn:
            row = await db_create_user(conn, user.name, user.email)
            return UserRead(id=row["id"], name=row["name"], email=row["email"])

    async def get_user(self, user_id: int) -> UserRead | None:
        pool = get_db_pool()
        async with pool.acquire() as conn:
            row = await db_get_user_by_id(conn, user_id)
            if row:
                return UserRead(id=row["id"], name=row["name"], email=row["email"])
            return None

    async def list_users(self) -> list[UserRead]:
        pool = get_db_pool()
        async with pool.acquire() as conn:
            rows = await db_list_users(conn)
            return [UserRead(id=r["id"], name=r["name"], email=r["email"]) for r in rows]