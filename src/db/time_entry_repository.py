from .models import TimeEntry
from .db import get_connection


class TimeEntryRepository:
    def create(self, time_entry: TimeEntry) -> TimeEntry:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO time_entries (user_id, created_at)
                VALUES (?, ?)
                """,
                (time_entry.user_id, time_entry.created_at),
            )
            time_entry.id = cursor.lastrowid
        return time_entry

    def get_top_users_by_time_entry_count(self, limit: int = 10):
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT user_id, COUNT(*) as total
                FROM time_entries
                GROUP BY user_id
                ORDER BY total DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [{"user_id": row["user_id"], "total": row["total"]} for row in rows]

    def get_user_time_entry_count(self, user_id: int) -> int:
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT user_id, COUNT(*) as total
                FROM time_entries
                WHERE user_id=?
                LIMIT 1
                """,
                (user_id,),
            ).fetchone()

        return row["total"]
