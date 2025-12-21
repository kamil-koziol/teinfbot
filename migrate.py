#!/usr/bin/env python3
import sqlite3
import os
import re
import argparse

parser = argparse.ArgumentParser(description="Run migrations on a SQLite database.")

parser.add_argument(
    "--migrations",
    default="migrations",
    help="Path to the migrations folder (default: 'migrations')",
)


parser.add_argument(
    "--db",
    default="database.db",
    help="Path to the SQLite database file. (default: database.db)",
)

args = parser.parse_args()

print(f"Database path: {args.db}")
print(f"Migrations folder: {args.migrations}")

# Ensure migrations folder exists
if not os.path.isdir(args.migrations):
    print(f"Error: migrations folder '{args.migrations}' does not exist.")
    exit(1)

# Ensure database file exists
if not os.path.exists(args.db):
    open(args.db, "a").close()
    print(f"Created database file: {args.db}")


# Connect to it
conn = sqlite3.connect(args.db)
cur = conn.cursor()

# Ensure migrations table
cur.execute("""
CREATE TABLE IF NOT EXISTS migrations (
    last_applied INTEGER DEFAULT 0
)
""")

cur.execute("""
INSERT INTO migrations(last_applied)
SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM migrations)
""")

conn.commit()


# Get the last applied migration
cur.execute("SELECT last_applied FROM migrations LIMIT 1")
last_applied = cur.fetchone()[0]
print(f"Last applied migration: {last_applied}")

migrations = sorted(f for f in os.listdir(args.migrations) if f.endswith(".sql"))

for migration_file in migrations:
    # Extract leading number from filename
    match = re.match(r"^(\d+)", migration_file)
    if not match:
        print(f"Skipping {fname}: no leading number")
        continue

    num = int(match.group(1).lstrip("0") or "0")
    if num <= last_applied:
        # Skip if already applied
        continue

    # Apply it
    path = os.path.join(args.migrations, migration_file)
    print(f"Applying {migration_file}...")
    with open(path, "r") as f:
        sql = f.read()
        cur.executescript(sql)

    # Update the counter
    cur.execute("UPDATE migrations SET last_applied=?", (num,))
    conn.commit()

print("Migrations complete.")
conn.close()
