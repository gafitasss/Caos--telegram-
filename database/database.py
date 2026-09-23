import sqlite3
import os
from contextlib import contextmanager


DATABASE_FILE = os.getenv(
    "DATABASE_FILE",
    "caos.db"
)


@contextmanager
def connection():

    conn = sqlite3.connect(
        DATABASE_FILE
    )

    conn.row_factory = sqlite3.Row

    try:
        yield conn

        conn.commit()

    except Exception:

        conn.rollback()

        raise

    finally:

        conn.close()


def init_database():

    with connection() as conn:

        conn.executescript("""

        CREATE TABLE IF NOT EXISTS players (

            user_id INTEGER PRIMARY KEY,

            username TEXT,

            name TEXT NOT NULL,

            energy INTEGER DEFAULT 100,

            fragments INTEGER DEFAULT 0,

            score INTEGER DEFAULT 0,

            level INTEGER DEFAULT 1,

            experience INTEGER DEFAULT 0,

            actions INTEGER DEFAULT 0,

            wins INTEGER DEFAULT 0,

            created_at INTEGER
        );


        CREATE TABLE IF NOT EXISTS groups (

            chat_id INTEGER PRIMARY KEY,

            round INTEGER DEFAULT 0,

            event TEXT DEFAULT 'nothing',

            round_started INTEGER DEFAULT 0,

            round_ends INTEGER DEFAULT 0,

            world_energy INTEGER DEFAULT 50,

            chaos INTEGER DEFAULT 0,

            created_at INTEGER
        );


        CREATE TABLE IF NOT EXISTS group_players (

            chat_id INTEGER,

            user_id INTEGER,

            joined_at INTEGER,

            PRIMARY KEY (
                chat_id,
                user_id
            ),

            FOREIGN KEY (
                user_id
            )
            REFERENCES players(user_id),

            FOREIGN KEY (
                chat_id
            )
            REFERENCES groups(chat_id)
        );


        CREATE TABLE IF NOT EXISTS actions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            chat_id INTEGER,

            round INTEGER,

            user_id INTEGER,

            action TEXT,

            created_at INTEGER
        );


        CREATE INDEX IF NOT EXISTS
        idx_actions_round
        ON actions(
            chat_id,
            round
        );


        CREATE INDEX IF NOT EXISTS
        idx_group_players
        ON group_players(
            chat_id
        );

        """)


# ==========================================
# JUGADORES
# ==========================================


def create_player(
    user_id,
    username,
    name
):

    import time

    with connection() as conn:

        conn.execute(
            """
            INSERT OR IGNORE INTO players
            (
                user_id,
                username,
                name,
                created_at
            )

            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                name,
                int(time.time())
            )
        )


def get_player(user_id):

    with connection() as conn:

        row = conn.execute(
            """
            SELECT *
            FROM players
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        return dict(row) if row else None


def update_player(
    user_id,
    energy_delta=0,
    fragments_delta=0,
    score_delta=0,
    action_delta=0
):

    with connection() as conn:

        conn.execute(
            """
            UPDATE players

            SET
                energy = MAX(
                    0,
                    energy + ?
                ),

                fragments = MAX(
                    0,
                    fragments + ?
                ),

                score = score + ?,

                actions = actions + ?

            WHERE user_id = ?
            """,
            (
                energy_delta,
                fragments_delta,
                score_delta,
                action_delta,
                user_id
            )
        )


# ==========================================
# GRUPOS
# ==========================================


def create_group(chat_id):

    import time

    with connection() as conn:

        conn.execute(
            """
            INSERT OR IGNORE INTO groups
            (
                chat_id,
                created_at
            )

            VALUES (?, ?)
            """,
            (
                chat_id,
                int(time.time())
            )
        )


def get_group(chat_id):

    with connection() as conn:

        row = conn.execute(
            """
            SELECT *
            FROM groups
            WHERE chat_id = ?
            """,
            (chat_id,)
        ).fetchone()

        return dict(row) if row else None


def update_group(
    chat_id,
    **values
):

    if not values:
        return

    allowed = {
        "round",
        "event",
        "round_started",
        "round_ends",
        "world_energy",
        "chaos"
    }

    values = {
        key: value
        for key, value in values.items()
        if key in allowed
    }

    if not values:
        return

    columns = ", ".join(
        f"{key} = ?"
        for key in values
    )

    params = list(
        values.values()
    )

    params.append(chat_id)

    with connection() as conn:

        conn.execute(
            f"""
            UPDATE groups

            SET {columns}

            WHERE chat_id = ?
            """,
            params
        )


def join_group(
    chat_id,
    user_id
):

    import time

    with connection() as conn:

        conn.execute(
            """
            INSERT OR IGNORE INTO
            group_players
            (
                chat_id,
                user_id,
                joined_at
            )

            VALUES (?, ?, ?)
            """,
            (
                chat_id,
                user_id,
                int(time.time())
            )
        )


# ==========================================
# ACCIONES
# ==========================================


def action_exists(
    chat_id,
    round_number,
    user_id
):

    with connection() as conn:

        row = conn.execute(
            """
            SELECT id

            FROM actions

            WHERE
                chat_id = ?
                AND round = ?
                AND user_id = ?

            LIMIT 1
            """,
            (
                chat_id,
                round_number,
                user_id
            )
        ).fetchone()

        return row is not None


def save_action(
    chat_id,
    round_number,
    user_id,
    action
):

    import time

    with connection() as conn:

        conn.execute(
            """
            INSERT INTO actions
            (
                chat_id,
                round,
                user_id,
                action,
                created_at
            )

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                chat_id,
                round_number,
                user_id,
                action,
                int(time.time())
            )
        )


def action_count(
    chat_id,
    round_number
):

    with connection() as conn:

        row = conn.execute(
            """
            SELECT COUNT(*) AS total

            FROM actions

            WHERE
                chat_id = ?
                AND round = ?
            """,
            (
                chat_id,
                round_number
            )
        ).fetchone()

        return row["total"]


# ==========================================
# RANKING
# ==========================================


def ranking(chat_id):

    with connection() as conn:

        rows = conn.execute(
            """
            SELECT
                p.user_id,
                p.name,
                p.username,
                p.score,
                p.level,
                p.fragments

            FROM players p

            INNER JOIN group_players gp

                ON gp.user_id = p.user_id

            WHERE gp.chat_id = ?

            ORDER BY
                p.score DESC

            LIMIT 20
            """,
            (chat_id,)
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]


def group_player_count(chat_id):

    with connection() as conn:

        row = conn.execute(
            """
            SELECT COUNT(*) AS total

            FROM group_players

            WHERE chat_id = ?
            """,
            (chat_id,)
        ).fetchone()

        return row["total"]
