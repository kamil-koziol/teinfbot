from typing import List
from .models import User
from .db import get_connection


class UserRepository:
    def create(self, user: User) -> User:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO users (id)
                VALUES (?)
                """,
                (user.id,),
            )
            user.id = cursor.lastrowid
        return user

    def list_users(self) -> List[User]:
        query = """
            SELECT id
            FROM users
        """

        with get_connection() as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()

        return [
            User(
                id=row["id"],
            )
            for row in rows
        ]

    def list_users_by_ids(self, user_ids: List[int]) -> List[User]:
        if not user_ids:
            return []

        placeholders = ",".join("?" for _ in user_ids)

        query = f"""
            SELECT id
            FROM users
            WHERE id IN ({placeholders})
        """

        print(query)

        with get_connection() as conn:
            cursor = conn.execute(query, user_ids)
            rows = cursor.fetchall()

        return [
            User(
                id=row["id"],
            )
            for row in rows
        ]
